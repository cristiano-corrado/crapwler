# crapwler

crapwler as the name states is a crawler written in a crappy coding in python.

it has few features though that might make it nice to use :

* mongodb support by default 127.0.0.1:27017 
* multithreaded 
* you can retrieve from db the links where they where firstly originated.

## Let's dig inside command line 

```
usage: crapwler.py [-h] --domain DOMAIN [--uas UAS] [--threads THREADS]
                   [--proxy PROXY]

A Python program that crawls a website and recursively checks links to map all
internal and external links. Written by ccc.

optional arguments:
  -h, --help            show this help message and exit
  --domain DOMAIN, -d DOMAIN
                        domain name of website you want to map. i.e.
                        "https://www.example.com"
  --uas UAS, -u UAS     random user agent selector
  --threads THREADS, -t THREADS
                        Set the amount of threads used for crawling
  --proxy PROXY, -p PROXY
                        Set proxy Eg: 127.0.0.1:8080

```

you can use different style of scanning : 

<code>-u</code> : random user agent selection from the list already nicely packed in csv folder in root project
 
<code>-p</code> : you can select proxies to connect to to perform the crawling check out [squidtor](https://www.github.com/urand0m/squidtor "squidtor project")

<code>-t</code> : select the amount of threads to spawn

[TODO]

* add option to connect to select the mongodb database
* add checks for hashes changes and reporting 

## Command line example usage :

```
python3 crapwler.py -t 30 -d https://www.example.com  -u csv/all.csv
``` 

### Output :

```
start crawling domain: http://testphp.vulnweb.com/ with threads: 1
http://testphp.vulnweb.com/ 200 0.22353720664978027
http://testphp.vulnweb.com/images/logo.gif 200 0.24135875701904297
http://testphp.vulnweb.com/index.php 200 0.6746737957000732
http://testphp.vulnweb.com/categories.php 200 0.5507657527923584
http://testphp.vulnweb.com/artists.php 200 0.5706148147583008
http://testphp.vulnweb.com/disclaimer.php 200 0.34359192848205566
http://testphp.vulnweb.com/cart.php 200 0.5393469333648682
http://testphp.vulnweb.com/guestbook.php 200 1.3796169757843018
http://testphp.vulnweb.com/AJAX/index.php 200 0.2960216999053955
http://testphp.vulnweb.com/login.php 200 0.2893509864807129
```

From far left you can see it prints for easy of understanding the link , the status code of the http response and the time to execute and receive response combined.

## Under the hood of the mongo database

Every request of the crawler will be stored in mongo as mentioned multiple times so far, but what does it look like ?

you need to have basic mongodb query skills.

every time you scan a different website a new collection will be created eg :

```
> db.getCollectionNames()
[
        "10.184.103.42:8001",
        "community.giffgaff.com",
        "http:",
        "labs.giffgaff.com",
        "testphp.vulnweb.com",
        "www.giffgaff.com",
        "www.libero.it"
]

``` 

if you want to query the content of a collection :

```
> db.www.giffgaff.com.find().limit(1).pretty()
{
        "_id" : ObjectId("5e37e160adb6b453469542bc"),
        "url" : "https://www.giffgaff.com",
        "transfer_time" : 1.164355993270874,
        "data" : {
                "sha256" : "dae368849cb3933f740564e1405789d9733bc9527c8ba575943c876040d7c35a",
                "comment" : "Can Follow",
                "http_code" : 200
        },
        "local_links" : [
                "https://www.giffgaff.com/",
                "https://www.giffgaff.com/boiler-plate/accessibility",
                "https://www.giffgaff.com/offer",
                "https://www.giffgaff.com/mobile-phones",
                "https://www.giffgaff.com/mobile-phones/apple",
                "https://www.giffgaff.com/mobile-phones/samsung",
                "https://www.giffgaff.com/mobile-phones/sony",
                "https://www.giffgaff.com/mobile-phones/huawei",
                "https://www.giffgaff.com/mobile-phones/compare",
                "https://www.giffgaff.com/mobile-phones/nokia",
                "https://www.giffgaff.com/mobile-phones/marketplace",
                "https://www.giffgaff.com/mobile-phones/refurbished",
                "https://www.giffgaff.com/mobile-phones/sell-my-phone",
                "https://www.giffgaff.com/sim-only-plans",
                "https://www.giffgaff.com/how-much-data-do-i-need",
                "https://www.giffgaff.com/orders/free-sim",
                "https://www.giffgaff.com/activate",
                "https://www.giffgaff.com/pricing",
                "https://www.giffgaff.com/international",
                "https://www.giffgaff.com/roaming-charges",
                "https://www.giffgaff.com/payback",
                "https://www.giffgaff.com/blog",
                "https://www.giffgaff.com/blog/categories/apps/",
                "https://www.giffgaff.com/blog/categories/gaming/",
                "https://www.giffgaff.com/blog/categories/giffgaff-news/",
                "https://www.giffgaff.com/blog/categories/phones/",
                "https://www.giffgaff.com/blog/categories/tech-news/",
                "https://www.giffgaff.com/help",
                "https://www.giffgaff.com/free-sim-cards",
                "https://www.giffgaff.com/help/articles/how-do-i-activate-my-sim",
                "https://www.giffgaff.com/unlock",
                "https://www.giffgaff.com/help/articles/how-do-i-keep-my-current-mobile-number-when-i-join-giffgaff",
                "https://www.giffgaff.com/coverage-and-service",
                "https://www.giffgaff.com/help/articles/difference-between-goodybags-and-credit",
                "https://www.giffgaff.com/help/articles/whats-a-goodybag",
                "https://www.giffgaff.com/help/articles/why-do-i-need-credit",
                "https://www.giffgaff.com/help/articles/buy-a-goodybag-with-a-voucher",
                "https://www.giffgaff.com/help/articles/usingyourmobileabroad",
                "https://www.giffgaff.com/help/articles/how-do-i-get-onto-my-voicemail",
                "https://www.giffgaff.com/help/articles/internet-apn-settings-guide",
                "https://www.giffgaff.com/help/articles/my-sim-is-broken",
                "https://www.giffgaff.com/support/lost",
                "https://www.giffgaff.com/profile/details",
                "https://www.giffgaff.com/support/puk",
                "https://www.giffgaff.com/support/ask",
                "https://www.giffgaff.com/support/questions",
                "https://www.giffgaff.com/dashboard",
                "https://www.giffgaff.com/profile/payment-details",
                "https://www.giffgaff.com/profile/my-loans",
                "https://www.giffgaff.com/first-steps",
                "https://www.giffgaff.com/spread",
                "https://www.giffgaff.com/profile/payback",
                "https://www.giffgaff.com/spread/recruits",
                "https://www.giffgaff.com/orders/mgm",
                "https://www.giffgaff.com/spread/advertise",
                "https://www.giffgaff.com/auth/login",
                "https://www.giffgaff.com/buy",
                "https://www.giffgaff.com/top-up",
                "https://www.giffgaff.com/boiler-plate/cookies",
                "https://www.giffgaff.com/help/articles/traffic-flow-policy",
                "https://www.giffgaff.com/mobile-phones/promo/huawei/huawei-p30-pro",
                "https://www.giffgaff.com/mobile-phones/apple/apple-iphone-11/phone-details",
                "https://www.giffgaff.com/mobile-phones/sony/sony-xperia-10/phone-details",
                "https://www.giffgaff.com/mobile-phones/apple/apple-iphone-xs/phone-details",
                "https://www.giffgaff.com/mobile-phones/pre-owned/apple/apple-iphone-x/phone-details",
                "https://www.giffgaff.com/mobile-phones/pre-owned/apple/apple-iphone-7/phone-details",
                "https://www.giffgaff.com/mobile-phones/pre-owned/samsung/samsung-galaxy-s9/phone-details",
                "https://www.giffgaff.com/refurbished",
                "https://www.giffgaff.com/about-us",
                "https://www.giffgaff.com/boiler-plate/affiliates",
                "https://www.giffgaff.com/index/mobile-app",
                "https://www.giffgaff.com/boiler-plate/contact",
                "https://www.giffgaff.com/terms",
                "https://www.giffgaff.com/boiler-plate/privacy",
                "https://www.giffgaff.com/modern-slavery-statement"
        ],
        "foreign_links" : [
                "https://w.usabilla.com",
                "https://googleads.g.doubleclick.net",
                "https://www.dwin1.com",
                "https://adservice.google.com",
                "https://ampcid.google.com",
                "https://collector-1167.tvsquared.com",
                "https://connect.facebook.net",
                "https://bat.bing.com",
                "https://www.googleadservices.com",
                "https://community.giffgaff.com/tags",
                "https://community.giffgaff.com/tags",
                "https://community.giffgaff.com/t/announcements",
                "https://community.giffgaff.com/t/service-updates",
                "https://community.giffgaff.com/t/help-and-support",
                "https://community.giffgaff.com/t/contribute",
                "https://community.giffgaff.com/t/welcome-and-join",
                "https://community.giffgaff.com/t/tips-and-guides",
                "https://community.giffgaff.com/t/general-discussion",
                "https://labs.giffgaff.com",
                "https://labs.giffgaff.com/idea/submit",
                "https://labs.giffgaff.com/browse",
                "https://labs.giffgaff.com/how",
                "https://community.giffgaff.com/t5/Help-Support/bd-p/QA1",
                "https://community.giffgaff.com/t5/Hub/ct-p/hub",
                "https://labs.giffgaff.com",
                "https://community.giffgaff.com/t5/Help-Support/bd-p/QA1",
                "https://giffgaff.com/free-sim-cards?bundleSKU=BD032",
                "https://giffgaff.com/free-sim-cards?bundleSKU=BD033",
                "https://giffgaff.com/free-sim-cards?bundleSKU=BD036",
                "https://giffgaff.com/free-sim-cards?bundleSKU=BD037",
                "https://giffgaff.com/free-sim-cards?bundleSKU=BD038",
                "https://giffgaff.com/free-sim-cards?bundleSKU=BD034",
                "https://giffgaff.com/free-sim-cards?bundleSKU=BD035",
                "https://community.giffgaff.com/t5/Contribute/bd-p/Improvements_suggestionbox",
                "https://twitter.com/giffgaff",
                "https://www.facebook.com/giffgaffmobile",
                "https://www.linkedin.com/company/giffgaff",
                "https://www.youtube.com/user/giffgaffTV",
                "https://instagram.com/giffgaffmobile",
                "https://www.giffgaff.io/jobs",
                "https://www.youtube.com/iframe_api"
        ],
        "broken_url" : [ ],
        "files" : [
                "https://www.giffgaff.com/styleguide/images/optimised-assets/homepage-new-visitors/styles/styles-2.css",
                "https://www.giffgaff.com/styleguide/css/home-static-v2.min.css?v=20200103",
                "https://static.giffgaff.com/fonts/1.0.0/giffgaff-regular.woff2",
                "https://static.giffgaff.com/fonts/1.0.0/giffgaff-medium.woff2",
                "https://static.giffgaff.com/fonts/1.0.0/giffgaff-bold.woff2",
                "https://static.giffgaff.com/fonts/1.0.0/font.css",
                "https://www.giffgaff.com/favicon-gg.ico?v=1",
                "https://www.giffgaff.com/gfx/icons/iphone-icon.png",
                "https://static.giffgaff.com/images/phones/promotions/HuaweiGTWatch_Feb20/HP--desktop.png",
                "https://static.giffgaff.com/images/phones/promotions/HuaweiGTWatch_Feb20/HP--mobile.png",
                "https://static.giffgaff.com/optimise-test-assets/the-voice/2020/voice-quote.png",
                "https://www.giffgaff.com/styleguide/images/optimised-assets/homepage-new-visitors/sally.png",
                "https://www.giffgaff.com/styleguide/js/vendor/jquery.min.js",
                "https://www.giffgaff.com/styleguide/js/static-home-page.min.js"
        ]
}

```
