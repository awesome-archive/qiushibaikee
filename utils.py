#!/usr/bin/env python
# coding:utf8
# author: broono
# email: tosven.broono@gmail.com
# ::database utils class

import psycopg2
# import random


class Utils(object):
    """A utils class which will be used later."""

    def __init__(self):
        # demonstrate a class level connection and cursor field
        self.connection = None
        self.cursor = None

    # return database connection object
    # return self.connection if utils class has a connection
    # else return a new connection
    def getConnection(self):
        if self.connection is None:
            self.connection = psycopg2.connect(
                "dbname=test user=test password=123456 host=127.0.0.1")
        return self.connection

    # return database cursor object
    # return self.cursor if utils class has a cursor
    # else return a new cursor with self.connection
    def getCursor(self):
        if self.connection is None:
            self.connection = self.getConnection()
        self.cursor = self.connection.cursor()
        return self.cursor

    # close database cursor and connection object if there is one
    def close(self):
        try:
            if self.cursor is not None:
                self.cursor.close()
            if self.connection is not None:
                self.connection.close()
        except Exception, e:
            raise e


class MobileUA(object):

    """A MobileUA class to randomly generate mobile-ua strings."""

    # initialize several mobile user-agents
    def __init__(self):
        self.UA = ["Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
                   "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
                   # "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
                   "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
                   "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
                   "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
                   "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
                   # "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
                   "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
                   # "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
                   "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)"
                   ]

    # intended to randomly generate UA strings but qiushibaike server
    # seems to render html pages in different structures, so we use a fixed one
    def random(self):
        # return random.choice(self.UA)
        return self.UA[-1]

if __name__ == '__main__':
    pass
