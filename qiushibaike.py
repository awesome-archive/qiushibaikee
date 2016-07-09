#!/usr/bin/env python
# coding:utf8
# author: broono
# email: tosven.broono@gmail.com
#  ::simple qiushibaike.com crawler

import re
import time
import requests
from freexici import freexici
from utils import Utils
from dbtool import ArticleDB, UserInfo, UserList
from utils import MobileUA
from bs4 import BeautifulSoup
from autouseragents.autouseragents import AutoUserAgents


class Qiushibaike(object):

    def __init__(self):
        self.urls = {"8hr": "http://www.qiushibaike.com/8hr/page/",
                     "hot": "http://www.qiushibaike.com/hot/page/",
                     "imgrank": "http://www.qiushibaike.com/imgrank/page/",
                     "text": "http://www.qiushibaike.com/text/page/",
                     #  history category is not stable so we'll just ignore
                     # "history": "http://www.qiushibaike.com/history/page/",
                     "pic": "http://www.qiushibaike.com/pic/page/",
                     "textnew": "http://www.qiushibaike.com/textnew/page/"}
        self.mua = MobileUA()
        self.ua = AutoUserAgents()
        self.session = None

    def closeSession(self):
        if self.session:
            try:
                self.session.close()
            except Exception, e:
                raise e

    def getSession(self):
        if self.session:
            return self.session
        return requests.session()

    def getProxy(self):
        proxies = freexici.randomProxy(many=1)
        proxyList = []
        for proxy in proxies:
            proxyList.append(proxy)
        proxy = proxyList[0]
        p = proxy.split("://")[0]
        proxy = {p: proxy}
        print "Using proxy ", proxy
        return proxy

    def crawl(self, url, mobile=True, proxy=False, callback=None):
        session = self.getSession()
        headers = {}
        if mobile:
            headers["User-Agent"] = self.mua.random()
        else:
            headers["User-Agent"] = self.ua.random_agent()
        if proxy:
            proxy = self.getProxy()
            print "with proxy: {}".format(proxy)
        try:
            response = session.get(url, headers=headers)
            assert response.status_code == 200
        except Exception, e:
            print e
            time.sleep(1)
            return self.crawl(url, True, True, callback)

        time.sleep(1)
        html = response.content

        if callback:
            print "Callback is executing."
            if not isinstance(callback, list):
                callback = [callback]
            cblen = len(callback)
            for i in range(cblen):
                ret = eval("self." + callback[i])(html)
                assert ret is True
        session.close()
        return True

    def exUserInfo(self, html):
        soup = BeautifulSoup(html, "lxml")
        datas = soup.find(
            "div", class_="user-data").findAll("ul", "user-data-block-list")

        user = soup.find("link", rel="canonical")
        userurl = user["href"][:-1]
        userid = userurl.split("/")[-1]
        print "userid:", userid
        print "userurl:", userurl

        usernametag = soup.find("div", class_="user-header-name")
        username = usernametag.getText().strip()
        print "username:", username

        valueList = []
        for block in datas:
            items = block.findAll("li")
            for item in items:
                values = item.findAll("span", class_="right")
                for value in values:
                    valueList.append(value.getText().strip())

        assert len(valueList) == 10
        marriedStr = valueList[5]
        married = None
        if marriedStr == "single":
            married = False
        if marriedStr == "married":
            married = True
        print "married: ", married

        constellationStr = valueList[6]
        constellations = None
        if constellationStr:
            constellations = constellationStr
        print "constellations: ", constellations

        jobStr = valueList[8]
        job = None
        if jobStr:
            job = jobStr
        print "job: ", job

        homeStr = valueList[7]
        hometown = None
        if homeStr:
            hometown = homeStr
        print "hometown: ", hometown

        uptimeStr = valueList[9]
        uptime = None
        if uptimeStr:
            utS = ""
            for e in uptimeStr:
                if e.isdigit():
                    utS += e
            assert utS.isdigit()
            uptime = int(utS)
        print "uptime: ", uptime

        fanStr = valueList[0]
        fans = None
        if fanStr:
            fans = int(fanStr)
        print "fans: ", fans

        interestStr = valueList[1]
        interests = None
        if interestStr:
            interests = int(interestStr)
        print "interests: ", interests

        postStr = valueList[2]
        posts = None
        if postStr:
            posts = int(postStr)
        print "posts: ", posts

        criticismStr = valueList[3]
        criticisms = None
        if criticismStr:
            criticisms = int(criticismStr)
        print "criticisms: ", criticisms

        smileStr = valueList[4]
        smiles = None
        if smileStr:
            smiles = int(smileStr)
        print "smiles: ", smiles

        self.insertUserInfo(userid, username, userurl,
                            married, constellations,
                            job, hometown, uptime,
                            fans, interests, posts,
                            criticisms, smiles)

        navs = soup.find("ul", class_="user-header-nav").findAll("a")
        navList = []
        for nav in navs:
            navList.append(nav["href"].strip())
        prefix = "http://qiushibaike.com"
        articleurl = prefix + navList[1] if len(navList) == 4 else None
        commentsurl = prefix + navList[2] if len(navList) == 4 else None
        liaisonsurl = prefix + \
            navList[3] if len(navList) == 4 else prefix + navList[1]
        print "articleurl:", articleurl
        if articleurl:
            ret = self.crawl(articleurl, True, False, callback="exArticle")
            assert ret is True
        print "commentsurl:", commentsurl
        if commentsurl:
            ret = self.crawl(commentsurl, True, False, callback="exUserList")
            assert ret is True
        print "liaisonsurl:", liaisonsurl
        if liaisonsurl:
            ret = self.crawl(liaisonsurl, True, False, callback="exUserList")
            assert ret is True

        return True

    def exUserList(self, html):
        soup = BeautifulSoup(html, "lxml")
        tags = soup.findAll("a", href=re.compile(r"/users/\d+?/$"))
        print len(tags)
        for tag in tags:
            usertag = tag["href"]
            userid = usertag.split("/")[-2]
            userurl = "http://www.qiushibaike.com" + usertag[:-1]
            self.insertUserList(userid=userid, userurl=userurl)
        return True

    def exArticle(self, html):
        ret = self.exFromBrowse(html)
        assert ret is True
        return True

    def exFromBrowse(self, html):
        soup = BeautifulSoup(html, "lxml")
        items = soup.findAll("article", id=re.compile(r"^article_\d+?"))
        for item in items:
            attrs = item.attrs
            for attr in attrs:
                if attr not in ["id", "class"]:
                    items.remove(item)
        for item in items:
            assert item is not None
            print
            articleid = item["id"].split("_")[-1]
            assert articleid.isdigit()
            articleid = int(articleid)
            print "articleid", articleid
            avatar = item.find("img", class_=re.compile(r"avatar"))
            userid, userurl, anonymous = -1, None, True
            if avatar:
                avatar = avatar["src"]
                if avatar.endswith(".jpg"):
                    userid = avatar.split("/")[-3]
                    base = "http://www.qiushibaike.com/users/"
                    userurl = base + userid
                    userid = int(userid)
                    anonymous = False
            else:
                userid = -1
                anonymous = True
            print "userid", userid
            print "userurl", userurl
            print "anonymous", anonymous
            username = None
            user = item.find("span", class_=re.compile(r"touch-user-name"))
            if user:
                username = user.getText().strip()
            print "username", username
            articletext = item.find("div", class_=re.compile(r"content-text"))
            if articletext:
                articletext = articletext.getText().strip()
            else:
                articletext = None
            print "articletext", articletext
            picture = item.find("img", class_=re.compile(r"w-xl"))
            if picture:
                haspic = True
                picurl = picture["src"]
            else:
                haspic = False
                picurl = None
            print "haspic", haspic
            print "picurl", picurl

            self.insertUserList(userid=userid, userurl=userurl)
            self.insertArticleDB(articleid=articleid, anonymous=anonymous,
                                 userid=userid, articletext=articletext,
                                 haspic=haspic, picurl=picurl)
        return True

    def insertArticleDB(self, articleid, anonymous, userid, articletext, haspic, picurl):
        articledb = ArticleDB(articleid, anonymous, userid,
                              articletext, haspic, picurl)
        articledb.store().close()

    def insertUserList(self, userid, userurl):
        userlist = UserList(userid, userurl)
        userlist.store().close()

    def insertUserInfo(self, userid, username, userurl, married, constellations, job, hometown, uptime, fans, interests, posts, criticisms, smiles):
        userinfo = UserInfo(userid, username, userurl,
                            married, constellations,
                            job, hometown, uptime, fans,
                            interests, posts, criticisms, smiles)
        userinfo.store().close()

    def doSingle(self, category, pages=3, callback=None):
        assert category in self.urls.keys()
        if pages > 35:
            pages = 35
        baseurl = self.urls[category]
        for i in range(1, pages + 1):
            url = baseurl + str(i)
            print "Scraping page: {}".format(url)
            ret = self.crawl(url, True, False, callback)
            assert ret is True
            print "Scraping page done."
            yield True

    def doMulti(self, categories, pages=3, callback=None):
        assert isinstance(categories, list)
        for i in range(len(categories)):
            category = categories[i]
            print "Scraping category: {}".format(category)
            assert category in self.urls.keys()
            rets = self.doSingle(category, pages, callback)
            print "Scraping category done."
            for ret in rets:
                assert ret is True
            yield True

    def doAll(self, pages=35, callback=None):
        rets = self.doMulti(self.urls.keys(), pages, callback)
        for ret in rets:
            assert ret is True

    def exploreUser(self, url):
        pass

    def expandUsers(self):
        myutil = Utils()
        connection = myutil.getConnection()
        cursor = myutil.getCursor()
        sql = "select * from userlist where userid<>-1 and done=false"
        cursor.execute(sql)
        newusers = cursor.fetchall()
        if cursor.rowcount != 0:
            for user in newusers:
                userid = user[0]
                userurl = user[1]
                callback = ["exUserInfo", "exArticle", "exUserList"]
                callback = "exUserInfo"
                ret = self.crawl(userurl, True, False, callback=callback)
                assert ret is True
                csql = "update userlist set done=%s where userid=%s"
                cursor.execute(csql, (True, userid))
                connection.commit()
        myutil.close()


if __name__ == '__main__':
    qb = Qiushibaike()
    qb.doAll(pages=35, callback="exFromBrowse")
    qb.expandUsers()
