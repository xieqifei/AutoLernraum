# -*- encoding: utf-8 -*-
'''
@file_name    :db.py
@description  :数据库接口文件
@time         :2021/07/19 23:27:25
@author       :Qifei
@version      :1.0
'''


import pymysql.cursors


#数据库API
class DBApi():
    def __init__(self):
        self.HOST = ""
        self.DBNAME = "rwthbuchen"
        self.USER = "rwthbuchen"
        self.PASSWORD = ""

    #操作数据库
    def execute_sql(self,sql):
        connection = pymysql.connect(host=self.HOST,
                             user=self.USER,
                             password=self.PASSWORD,
                             database=self.DBNAME,
                             cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(sql)
                    boo = True
                except :
                    boo=False
            connection.commit()
        return boo


    #查询数据库
    def select_sql(self,sql):
        connection = pymysql.connect(host=self.HOST,
                             user=self.USER,
                             password=self.PASSWORD,
                             database=self.DBNAME,
                             cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(sql)
                    result = cursor.fetchall()
                except :
                    result=False
            connection.commit()
        return result
#用户API
class UserApi():
    def __init__(self):
        self.db = DBApi()

    #添加新用户
    def add_user(self,username,password):
        sql = "INSERT INTO `rwthbuchen`.`rw_users` (`id`, `username`, `password`) VALUES (NULL, '"+username+"', '"+password+"')"
        return self.db.execute_sql(sql)
    
    #更新新用户
    def update_user(self,username,password):
        sql = "UPDATE `rwthbuchen`.`rw_users` SET `password` = '"+password+"' WHERE `rw_users`.`username` = '"+username+"';"
        return self.db.execute_sql(sql)
    
    #验证用户
    def validate_user(self,username,password):
        sql = "SELECT `id`, `username`, `password` FROM `rw_users` WHERE `username`='"+username+"' AND `password` = '"+password+"'"
        re = self.db.select_sql(sql)
        if(re):
            return True
        else:
            return False

    #用户名是否已有
    def is_username_used(self,username):
        sql = "SELECT `id`, `username` FROM `rw_users` WHERE `username`='"+username+"' "
        re = self.db.select_sql(sql)
        if(re):
            return True
        else:
            return False

    #删除用户
    def delete_user(self,username):
        sql = "DELETE FROM `rwthbuchen`.`rw_users` WHERE `rw_users`.`username` = '"+username+"';"
        return self.db.execute_sql(sql)

#用户信息模板
class TempletApi():
    def __init__(self):
        self.db = DBApi()
    
    #更新插入
    def update_and_insert_templet(self,dic):
        if(self.is_templet_created(dic['username'])):
            return self.update_templet(dic)
        else:
            return self.insert_templet(dic)
        
    #插入信息模板
    def insert_templet(self,dic):
        sql = "INSERT INTO `rwthbuchen`.`rw_templet` (`id`, `username`, `email`, `sex`, `vorname`, `name`, `strasse`, `ort`, `matnr`, `telefon`) VALUES (NULL, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(dic['username'],dic['email'],dic['sex'],dic['vorname'],dic['name'],dic['strasse'],dic['ort'],dic['matnr'],dic['telefon'])
        return self.db.execute_sql(sql)
    
    #更新模板
    def update_templet(self,dic):
        sql = "UPDATE `rw_templet` SET `email`='{}',`sex`='{}',`vorname`='{}',`name`='{}',`strasse`='{}',`ort`='{}',`matnr`='{}',`telefon`='{}' WHERE `username`='{}'".format(dic['email'],dic['sex'],dic['vorname'],dic['name'],dic['strasse'],dic['ort'],dic['matnr'],dic['telefon'],dic['username'])
        return self.db.execute_sql(sql)
    
    #验证模板是否存在
    def is_templet_created(self,username):
        sql = "SELECT * FROM `rw_templet` WHERE `username`='{}'".format(username)
        re = self.db.select_sql(sql)
        if(re):
            return True
        else:
            return False
    
    #获取模板，返回字典
    def get_templet(self,username):
        sql = "SELECT * FROM `rw_templet` WHERE `username`='{}'".format(username)
        re = self.db.select_sql(sql)
        if(re):
            return re[0]
        else:
            return False

    #获取多个信息模板
    def get_templets(self,usernames):
        sql = "SELECT * FROM `rw_templet` WHERE"
        sql_list = []
        if(len(usernames)):
            for username in usernames:
                sql_list.append(" `username`='{}' ".format(username))
            sql += 'OR'.join(sql_list)
            return self.db.select_sql(sql)
        else:
            return False

    
    #删除模板
    def delete_templet(self,username):
        sql = "DELETE FROM `rwthbuchen`.`rw_templet` WHERE `rw_templet`.`username` = '{}'".format(username)
        return self.db.execute_sql(sql)

class BuchenListApi():
    def __init__(self):
        self.db = DBApi()
    
    #获取自习室信息
    def get_kurs(self):
        sql = "SELECT * FROM `rw_kurs`"
        return self.db.select_sql(sql)

    #更新自习室信息
    def update_kurs(self,raums):
        if(len(raums)):
            ready_to_add = []
            result = self.get_kurs()
            if(result):
                for i in raums:
                    is_unique = True
                    for j in result:
                        if(i['kursnr'] == j['kursnr']):
                            is_unique = False
                    if(is_unique):
                        ready_to_add.append(i)
            else:
                ready_to_add = raums
            if(len(ready_to_add)):
                sql = "INSERT INTO `rwthbuchen`.`rw_kurs` (`id`, `kursnr`, `kursid`, `code`, `ort`, `zeit`, `tag`, `kursvalue`) VALUES "
                sql_list = []
                for kurs in ready_to_add:
                    sql_list.append("(NULL,'{}','{}','{}','{}','{}','{}','{}')".format(kurs['kursnr'],kurs['kursid'],kurs['code'],kurs['ort'],kurs['zeit'],kurs['tag'],kurs['kursvalue']))
                sql += ','.join(sql_list)
                self.db.execute_sql(sql)
            else:
                return False
        return False

    #添加预定列表
    def add_buchungen(self,buchungen):
        #提出相同的列表
        if(len(buchungen)):
            ready_to_add = []
            result = self.get_buchungen(buchungen[0]['username'])
            if(result):
                for i in buchungen:
                    is_unique = True
                    for j in result:
                        if(i['tag'] == j['tag'] and i['ort'] == j['ort']):
                            is_unique = False
                    if(is_unique):
                        ready_to_add.append(i)
            else:
                ready_to_add = buchungen
            if(len(ready_to_add)):
                sql = "INSERT INTO `rw_buchenlist`(`id`, `username`, `tag`, `time`, `ort`, `week`, `kursnr`, `status`) VALUES "
                sql_list = []
                for buchung in ready_to_add:
                    sql_list.append("(NULL,'{}','{}','{}','{}','{}','{}','{}')".format(buchung['username'],buchung['tag'],buchung['time'],buchung['ort'],buchung['week'],buchung['kursnr'],"队列中"))
                sql += ','.join(sql_list)
                return self.db.execute_sql(sql)
            else:
                return False
        return False

    #预定是否存在
    def is_buchung_created(self,buchung):
        sql = "SELECT * FROM `rw_buchenlist` WHERE `username`='{}' AND `tag`='{}' AND `kursnr`='{}'".format(buchung['username'],buchung['tag'],buchung['kursnr'])
        if(self.db.select_sql(sql)):
            return True
        else:
            return False

    #获取预定列表
    def get_buchungen(self,username):
        sql = "SELECT * FROM `rw_buchenlist` WHERE `username`='{}'".format(username)
        re = self.db.select_sql(sql)
        if(re):
            return re
        else:
            return False

    #删除预定列表
    def delete_buchungen(self,buchungen):
        sql_list = []
        for buchung in buchungen:
            sql_list.append("(`ort` = '{}'AND`tag`='{}')".format(buchung['ort'],buchung['tag'])) 
        if(len(sql_list)):
            sql = "DELETE FROM `rw_buchenlist` WHERE `username` = '{}' AND ".format(buchungen[0]['username'])
            sql += ("("+'OR'.join(sql_list)+")")
            return self.db.execute_sql(sql)
        else:
            return False
    
    #根据日期获取buchung
    def get_buchungen_from_tag(self,tag):
        sql = "SELECT * FROM `rw_buchenlist` WHERE `tag`='{}'".format(tag)
        re = self.db.select_sql(sql)
        if(re):
            return re
        else:
            return False

    #更新预定状态
    def update_buchung_status(self,buchung,status):
        sql = "UPDATE `rw_buchenlist` SET `status`='{}' WHERE `kursnr` = '{}' AND `tag` = '{}'AND `username` ='{}'".format(status,buchung['kursnr'],buchung['tag'],buchung['username'])
        return self.db.execute_sql(sql)