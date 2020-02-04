from bs4 import BeautifulSoup
import sys, requests


def authtrial(url,username=None,password=None,proxies=None,headers=None):
    login = [ 'login','auth','authentication']

    if any( word for word in login if word in url):
        res = requests.get(url,proxies=proxies,verify=False)
        soup = BeautifulSoup(res.text,'lxml')
        form=soup.find(name='form')
        action=form['action']
        data = {}
        for input in form('input'):
            data[input['name']] = input['value']

        usertags = [ 'user' , 'username' , 'nickname' , 'id' , 'email' , 'useremail' ]
        passwordtags = [ 'pass', 'password', 'credentials', 'secret' ]

        for word in usertags:
            if word in data:
                data[word]=username

        for word in passwordtags:
            if word in data:
                data[word]=password

        res=requests.post(url,data=data,proxies=proxies,verify=False,cookies=res.cookies,headers=headers)

        return res

    else:
        return False



