#!/usr/bin/env python
# coding:utf8
# author: broono
# email: tosven.broono@gmail.com
# ::database model class

from utils import Utils
from self import self


class DBModel(object):

    def __init__(self):
        self.util = Utils()
        self.connection = self.util.getConnection()
        self.cursor = self.util.getCursor()
        self.initSQL = []
        assert self.initdb() is True

    def initdb(self):
        initSQL1 = "create table if not exists userinfo (" +\
            "userid integer primary key,username varchar," +\
            "userurl varchar,married boolean," +\
            "constellations varchar,job varchar," +\
            "hometown varchar,uptime integer," +\
            "fans integer,interests integer," +\
            "posts integer,criticisms integer," +\
            "smiles integer)"
        self.initSQL.append(initSQL1)
        initSQL2 = "create table if not exists userlist (" +\
            "userid integer primary key," +\
            "userurl varchar," +\
            "done boolean)"
        self.initSQL.append(initSQL2)
        initSQL3 = "create table if not exists article (" +\
            "articleid integer primary key,anonymous boolean," +\
            "userid integer,articletext varchar," +\
            "haspic boolean,picurl varchar)"
        self.initSQL.append(initSQL3)
        try:
            for sql in self.initSQL:
                self.cursor.execute(sql)
            self.connection.commit()
            return True
        except Exception, e:
            print e
            return False

    def formatdb(self):
        self.reinitSQL = []
        for tname in ["userinfo", "userlist", "article"]:
            sql = "drop table if exists %s" % tname
            self.reinitSQL.append(sql)
        try:
            for sql in self.reinitSQL:
                self.cursor.execute(sql)
            self.connection.commit()
            return True
        except Exception, e:
            print e
            return False

    def reinitdb(self):
        assert self.formatdb() is True
        assert self.initdb() is True
        return True

    def close(self):
        try:
            if self.cursor is not None:
                self.cursor.close()
            if self.connection is not None:
                self.connection.close()
        except Exception, e:
            raise e


class UserInfo(DBModel):

    # userid, username, userurl, married, constellations, job, hometown,
    # uptime, fans, interests, posts, criticisms, smiles
    def __init__(self, userid, username, userurl, married, constellations, job, hometown, uptime, fans, interests, posts, criticisms, smiles):
        DBModel.__init__(self)
        self.fields = ["userid", "username", "userurl",
                       "married", "constellations", "job",
                       "hometown", "uptime", "fans",
                       "interests", "posts", "criticisms",
                       "smiles"]
        self.userid = userid
        self.username = username
        self.userurl = userurl
        self.married = married
        self.constellations = constellations
        self.job = job
        self.hometown = hometown
        self.uptime = uptime
        self.fans = fans
        self.interests = interests
        self.posts = posts
        self.criticisms = criticisms
        self.smiles = smiles

    @self
    def store(self):
        try:
            esql = "select * from userinfo where userid=%s" % self.userid
            self.cursor.execute(esql)
            rs = self.cursor.fetchall()
            sql = ""
            if self.cursor.rowcount == 0:
                sql = "insert into userinfo (userid,username,userurl," +\
                    "married,constellations,job,hometown,uptime,fans," +\
                    "interests,posts,criticisms,smiles) " +\
                    "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                print "Storing userinfo of: {}".format(self.userid)
            else:
                sql = "update userinfo set userid=%s, username=%s, " +\
                    "userurl=%s, married=%s, constellations=%s, job=%s, " +\
                    "hometown=%s, uptime=%s, fans=%s, interests=%s, " +\
                    "posts=%s, criticisms=%s, smiles=%s " +\
                    "where userid=%s"
                print "Updating userinfo of: {}".format(self.userid)
            self.cursor.execute(sql, (self.userid, self.username,
                                      self.userurl, self.married,
                                      self.constellations, self.job,
                                      self.hometown, self.uptime,
                                      self.fans, self.interests,
                                      self.posts, self.criticisms,
                                      self.smiles))
            self.connection.commit()
            print "Userinfo of userid {} success.".format(self.userid)
        except Exception, e:
            self.connection.rollback()
            print e

    @self
    def init(self):
        assert DBModel.initdb(self) is True

    @self
    def reinit(self):
        assert DBModel.reinitdb(self) is True


class ArticleDB(DBModel):

    # articleid, anonymous, userid, articletext, haspic, picurl
    def __init__(self, articleid, anonymous, userid, articletext, haspic, picurl):
        DBModel.__init__(self)
        self.fields = ["articleid", "anonymous",
                       "userid", "articletext",
                       "haspic", "picurl"]
        self.articleid = articleid
        self.anonymous = anonymous
        self.userid = userid
        self.articletext = articletext
        self.haspic = haspic
        self.picurl = picurl

    @self
    def store(self):
        try:
            esql = "select * from article where articleid=%s and userid=%s" % (
                self.articleid, self.userid)
            self.cursor.execute(esql)
            rs = self.cursor.fetchall()
            if self.cursor.rowcount == 0:
                sql = "insert into article (articleid,anonymous,userid," +\
                    "articletext,haspic,picurl) values (%s,%s,%s,%s,%s,%s)"
                self.cursor.execute(sql, (self.articleid, self.anonymous,
                                          self.userid, self.articletext,
                                          self.haspic, self.picurl))
                self.connection.commit()
                print "Stored article: {} into articledb".format(self.articleid)
            else:
                print "Article {} already exists in articledb.".format(self.articleid)
        except Exception, e:
            self.connection.rollback()
            print e

    @self
    def init(self):
        assert DBModel.initdb(self) is True

    @self
    def reinit(self):
        assert DBModel.reinitdb(self) is True


class UserList(DBModel):

    # userid,userurl,done
    def __init__(self, userid, userurl, done=False):
        DBModel.__init__(self)
        self.fields = ["userid", "userurl", "done"]
        self.userid = userid
        self.userurl = userurl
        self.done = done

    @self
    def store(self):
        try:
            esql = "select * from userlist where userid=%s" % self.userid
            self.cursor.execute(esql)
            rs = self.cursor.fetchall()
            if self.cursor.rowcount == 0:
                sql = "insert into userlist (userid,userurl,done)" + \
                    " values (%s,%s,%s)"
                self.cursor.execute(
                    sql, (self.userid, self.userurl, self.done))
                self.connection.commit()
                print "Stored user: {} into userlist".format(self.userid)
            else:
                print "User {} already exists in userlist.".format(self.userid)
        except Exception, e:
            self.connection.rollback()
            print e

    @self
    def init(self):
        assert DBModel.initdb(self) is True

    @self
    def reinit(self):
        assert DBModel.reinitdb(self) is True
