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
在变量buchung中,需要修改的数据如下：            you need to change the following values in 'buchung':
kursnr:你想预定的课程的课程编号。               lernraum number, here u can find in in booking website, site url is in following.
        在图书馆的预定系统中，很容易就可以找到。  https://buchung.hsz.rwth-aachen.de/angebote/aktueller_zeitraum/_Lernraumbuchung.html
email:你的邮箱。                               email to receive Bestaetigung
sex:性别。男：M；女:W                           male:M  female:W
vorname:名字。首字母大写                        first name. Initial capital
name:姓。首字母大写                             last name. Initial capital
strasse:街道和号码                              street and number.
ort:邮编和地址，务必注意格式是52076 Aachen.      zip code and city name. format must be: 52074 Aachen
matnr:六位学号                                 six-figure student number
telefon:带前缀的手机号                          phone number
time:自习室开放时间，格式必须为8.00 - 16.30。    lernraum open time. format must be :8.00 - 16.30
    开放时间即为程序开始运行抢座的时间，
    在此之前程序会进入倒计时。
    因此务必保证开放时间的准确。                                      
其余内容可不修改.                               other values dont need to change
'''

def main_handler(event,context):
    buchung = {'time': '08.00 - 16.30', 'kursnr': '08411027','info':{ 'username': '', 'email': 'example@gmail.com', 'sex': 'M', 'vorname': 'Ivan', 'name': 'Natanael', 'strasse': 'Pontstr.23', 'ort': '52076  Aachen', 'status': 'S-RWTH', 'matnr': '468389', 'telefon': '00491748068847'}}
    LernraumInfo().buchen_platz_via_requests(buchung)