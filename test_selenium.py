# -*- encoding: utf-8 -*-
'''
@file_name    :test_selenium.py
@description  :利用selenium库浏览器自动化预定。占用内存较大，效率较低，可靠性更高。
@time         :2021/07/19 23:29:40
@author       :Qifei
@version      :1.0
'''


from myclass import *

'''
在变量buchung中,需要修改的数据如下：            you need to change the following values in 'buchung':
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
请在自习室开放时间之前运行
'''

# 在需要预定的自习室前，将switch设置为1，其余设置为0。当且仅有一个1。
lernraum = [
    {'switch':1,'ort':'Bib1','time':'08.00 - 14.02','kursnr':'08511007',"button":"BS_Kursid_181911"},
    {'switch':0,'ort':'Bib1','time':'14.00 - 22.00','kursnr':'08511008',"button":"BS_Kursid_181912"},
    {'switch':0,'ort':'Bib2','time':'08.00 - 14.00','kursnr':'08611004',"button":"BS_Kursid_181913"},
    {'switch':0,'ort':'Bib2','time':'14.00 - 22.00','kursnr':'08611005',"button":"BS_Kursid_181914"},
]


buchung = {'info':{ 'username': '', 'email': 'example@gmail.com', 'sex': 'M', 'vorname': 'Ivan', 'name': 'Natanael', 'strasse': 'Pontstr.23', 'ort': '52076  Aachen', 'status': 'S-RWTH', 'matnr': '468389', 'telefon': '00491748068847'}}

for raum in lernraum:
    if(raum['switch']):
        buchung.update(raum)
        break

LernraumInfo().buchen_platz_via_selenium(buchung)