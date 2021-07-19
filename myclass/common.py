# -*- encoding: utf-8 -*-
'''
@file_name    :common.py
@description  :配合预定网站+数据库使用的预定系统通用文件。批量预定程序
@time         :2021/07/19 23:25:31
@author       :Qifei
@version      :1.0
'''

import json
from .db import *
from .lernraum import *
import hashlib
from urllib import parse
import datetime
import threading
#响应类，返回一个http响应格式字典
class Response:
    #错误相应
    def error(self, msg):
        return {
            "isBase64Encoded": False,
            "statusCode": 400,
            "headers": {'Content-Type': 'application/json'},
            "body": '{"error":1,"msg":"'+msg+'}'
        }

    #返回一个html页面
    def html(self, html):
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {'Content-Type': 'text/html'},
            "body": html
        }
    #返回json格式数据
    def json(self, jsonObj):
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {'Content-Type': 'application/json','Access-Control-Allow-Origin':'*'},
            "body": json.dumps(jsonObj)
        }

class Operation():
    def __init__(self):
        pass
    
    #开始预定程序
    def start_buchen(self):
        morgen=datetime.date.today()+datetime.timedelta(days=1)
        morgen_str = morgen.strftime('%d.%m.%Y')
        buchungen = BuchenListApi().get_buchungen_from_tag(morgen_str)
        users=set()
        ready_to_buchen = []
        #查找user的信息模板，并插入到buchung中
        if(buchungen):
            for item in buchungen:
                users.add(item['username'])
            infos = TempletApi().get_templets(users)
            if(infos):
                for i in range(len(buchungen)):
                    for info in infos:
                        if(buchungen[i]['username'] == info['username']):
                            buchungen[i]['info'] = info
                            if(buchungen[i]['status'] != '预定成功'):
                                ready_to_buchen.append(buchungen[i])
        if(ready_to_buchen):
            print(ready_to_buchen)
            threads = []
            for buchung in ready_to_buchen:
                t = BuchungThreading(buchung)
                threads.append(t)
                t.start()
            for t in threads:
                t.join()
            print('启动预定程序成功')
            return Response().json({'msg':'启动预定程序成功'})
        else:
            print('没有需要预定的位置')
            return Response().json({'msg':"没有需要预定的位置"})
                
#单个预定进程
class BuchungThreading(threading.Thread):
    def __init__(self,buchung):
        threading.Thread.__init__(self)
        self.buchung = buchung
    
    def run(self):
        print("正在执行预定程序线程"+self.buchung['username'])
        result = LernraumInfo().buchen_platz_via_requests(self.buchung)
        # result = LernraumInfo().buchen_platz_via_selenium(self.buchung)
        if(result):
            BuchenListApi().update_buchung_status(self.buchung,'预定成功')
        else:
            BuchenListApi().update_buchung_status(self.buchung,'预定失败')
