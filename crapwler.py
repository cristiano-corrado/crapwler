import re
import sys
import csv
import time
import argparse
import pymongo
import hashlib
import random
import requests
import requests.exceptions
import urllib3
from urllib.parse import urlsplit
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from collections import deque
from threads import ThreadPool
import authenticator

urllib3.disable_warnings()


# a set of urls that we have already crawled
processed_urls = []
# a set of domains inside the target website
local_urls = set([])
# a set of domains outside the target website
foreign_urls = []
# a set of broken urls
broken_urls = []
tags_urls = set([])
listuas = []


def hasher(request):
    sha256 = hashlib.sha256(request)
    return sha256.hexdigest()


def filedetector(urllink):
    urllink = urlparse(urllink)
    #urllink = urllink.netloc+urllink.path
    filetypes = ["css", "js", "woff", "xls", "xlsx",
                 "doc", "pdf", "jpg", "svg", "ico", "woff2","png","JPG","jpeg"]
    for files in filetypes:
        if re.search(".*?."+files+".*", urllink.path):
            return True


def extractlinks(response, url, endtime, ggsha256, domain):
    blacklist = re.compile("javascript:|.*Incapsula.|mailto:|data:image")

    tags = ['a', 'script', 'link','img']
    crawldomain = urlsplit(domain)

    mapLinks = {
        "url": url,
        "transfer_time": endtime,
        "data": {"sha256": ggsha256,
                 "comment": "",
                 "http_code": ""},
        "local_links": [],
        "foreign_links": [],
        "broken_url": [],
        "files": []
    }

    mapLinks['data']['http_code'] = response.status_code


    if re.search("We couldn't find that page", response.text):
        mapLinks['data']['comment'] = 'Not Found'
    else:
        mapLinks['data']['comment'] = 'Can Follow'
    # extract base url to resolve relative links

    parts = urlsplit(url)
    base = "{0.netloc}".format(parts)
    strip_base = base.replace("www.", "")
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    path = url[:url.rfind('/')+1] if '/' in parts.path else url

    # create a beutiful soup for the html document
    soup = BeautifulSoup(response.text, "lxml")

    for links in soup.find_all(tags):

        anchor = ''

        if 'src' in links.attrs and not blacklist.search(links.attrs['src']):
            anchor = links.attrs["src"]

        if 'href' in links.attrs and not blacklist.search(links.attrs['href']):
            anchor = links.attrs["href"]

        # extract link url from the anchor

        if 'http' in anchor and ( urlsplit(anchor).netloc == crawldomain.netloc ) :
            local_link = anchor

        elif 'http' in anchor and ( urlsplit(anchor).netloc != crawldomain.netloc ) and not filedetector(anchor):
            mapLinks['foreign_links'].append(anchor)

        elif blacklist.search(url):
            continue

        elif anchor.startswith("../") and (anchor.split('/')[1] == urlsplit(url).path.split("/")[-1]):
            continue

        elif anchor.startswith("../") and not (anchor.split('/')[1] == urlsplit(url).path.split("/")[-1]):
            # the idea here is to take url eg :
            # /mobile-phones/apple/apple-iphone-11-pro-max/phone-details and the ../ is ..//apple-iphone-11-pro/phone-plans
            # take original path split it remove
            anchor = anchor.replace("..", "")
            split = urlsplit(url)
            path = split.path
            netloc = split.netloc
            scheme = split.scheme
            path = "/".join(path.split('/')[:-2])
            local_link = '{}://{}{}{}'.format(scheme,netloc,path+anchor)


        elif filedetector(anchor):
            if not crawldomain.netloc in anchor and anchor.startswith("/"):
                anchor = domain+anchor
            mapLinks['files'].append(anchor)

        elif re.search('#.*', anchor):
            continue

        elif (anchor.startswith('//') and not crawldomain.netloc in anchor):
            mapLinks['foreign_links'].append('https:'+anchor)

        elif (anchor.startswith("/") and crawldomain.netloc in anchor):
            local_link = "https:"+anchor

        elif anchor.startswith(crawldomain.netloc.replace('www.', "")):
            local_link = "https://www.{}".format(anchor)

        elif anchor.startswith("/"):
            local_link = base_url + anchor

        elif not anchor.startswith('http'):
            local_link = path + anchor

        else:
            mapLinks['foreign_links'].append(anchor)

        try :
            local_urls.add(local_link)

            for sites in list(dict.fromkeys(local_urls)):
                if not sites in new_urls and not sites in processed_urls:
                    mapLinks['local_links'].append(sites)
                    new_urls.append(sites)
        except UnboundLocalError:

            continue

        local_urls.clear()

    mongostore(mapLinks)

    print(mapLinks['url'], mapLinks['data']['http_code'], endtime, flush=True)


def mongostore(maplinks):
    try:
        mycol.insert_one(maplinks)

    except pymongo.errors.DuplicateKeyError as duplicates:
        print(duplicates)
        sys.exit()


def crawler(domain, proxies, uas=None):

    if proxies:
        proxies = {'http': proxies, 'https': proxies}

    if uas:
        headers = {'User-Agent': randomua(uas)}
    else:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; rv:49.0) Gecko/20100101 Firefox/49.0'}

    # move next url from the queue to the set of processed urls
    url = new_urls.popleft()
    processed_urls.append(url)

    try:
        try:
            start = time.time()
            response = requests.get(
                url, headers=headers, verify=False, proxies=proxies, allow_redirects=False,cookies=None)
            endtime = time.time() - start
            ggsha256 = hasher(response.text.encode('utf-8'))
            extractlinks(response, url, endtime, ggsha256, domain)
        except (requests.exceptions.MissingSchema,
                requests.exceptions.ConnectionError,
                requests.exceptions.InvalidURL,
                requests.exceptions.InvalidSchema):
            # add broken urls to it's own set, then continue
            broken_urls.append(url)
    except KeyboardInterrupt:
        sys.exit()


def randomua(list):

    if not len(listuas) > 1:
        with open(list, 'r') as uas:
            reader = csv.reader(uas, delimiter=',', quoting=csv.QUOTE_NONE)
            for row in reader:
                if not row == '':
                    listuas.append(
                        "".join(row[:-2]).replace("\"", "").rstrip())

    randomua = random.randrange(0, len(listuas))
    return listuas[randomua]


def main(argv):
    global new_urls
    global mycol
    # define the program description
    text = 'A Python program that crawls a website and recursively checks links to map all internal and external links. Written by ccc.'
    # initiate the parser with a description
    parser = argparse.ArgumentParser(description=text)
    parser.add_argument('--domain', '-d', required=True,
                        help='domain name of website you want to map. i.e. "https://www.example.com"')
    parser.add_argument('--uas', '-u', required=False,
                        help='random user agent selector')
    parser.add_argument('--threads', '-t', required=False,
                        help='Set the amount of threads used for crawling')
    parser.add_argument('--proxy', '-p', required=False,
                        default=None, help='Set proxy Eg: 127.0.0.1:8080')
    parser.parse_args()

    # read arguments from the command line
    args = parser.parse_args()
    domain = args.domain
    uas = args.uas
    proxies = args.proxy

    try:


        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["mapsite"]
        mycol = mydb[urlsplit(domain).netloc]
        mycol.create_index("sha256")

    except pymongo.errors.ServerSelectionTimeoutError:
        print("The mongo server selected is not reachable.")
        sys.exit()

    if args.threads and (int(args.threads) > 1):
        threads = int(args.threads)
    else:
        threads = 1

    if proxies:
        try:
            proxies.split(":")[1]
        except (IndexError, AttributeError):
            print("Proxy option is not in the right format, Eg: 127.0.0.1:8080")
            sys.exit()

    if (domain or uas):

        print("start crawling domain: {} with threads: {}".format(domain, threads))

        pool = ThreadPool(threads)
        new_urls = deque([domain])
        try:
            while len(new_urls):
                if len(new_urls) <= 2:
                    crawler(domain, proxies, uas=uas)
                else:
                    pool.add_task(crawler, domain, proxies, uas=uas)

        except KeyboardInterrupt:

            print("Pressed CTRL+C, waiting for processes to close. process number {}".format(ThreadPool.count(pool)))
            ThreadPool.wait_completion(pool)
            mycol.drop()


if __name__ == "__main__":
    main(sys.argv[1:])
