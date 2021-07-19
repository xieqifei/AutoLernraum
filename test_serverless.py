# -*- encoding: utf-8 -*-
'''
@file_name    :test_serverless.py
@description  :适用于云函数，可定时运行，实现定时抢座
@time         :2021/07/19 23:30:34
@author       :Qifei
@version      :1.0
'''


from myclass import *

'''
在变量buchung中,需要修改的数据如下：
kursnr:你想预定的课程的课程编号。在图书馆的预定系统中，很容易就可以找到。https://buchung.hsz.rwth-aachen.de/angebote/aktueller_zeitraum/_Lernraumbuchung.html
email:你的邮箱。
sex:性别。男：M；女:W
vorname:名字。首字母大写
name:姓。首字母大写
strasse:街道和号码
ort:邮编和地址，务必注意格式是52076 Aachen.
matnr:六位学号
telefon:带前缀的手机号
其余内容可不修改
'''

def main_handler(event,context):
    buchung = {'ort': 'Semi90', 'kursnr': '08411027','info':{ 'username': '', 'email': 'example@gmail.com', 'sex': 'M', 'vorname': 'Ivan', 'name': 'Natanael', 'strasse': 'Pontstr.23', 'ort': '52076  Aachen', 'status': 'S-RWTH', 'matnr': '468389', 'telefon': '00491748068847'}}
    LernraumInfo().buchen_platz_via_requests(buchung)