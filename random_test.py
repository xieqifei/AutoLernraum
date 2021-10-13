from myclass import *

'''
在变量buchung中,需要修改的数据如下：you need to change the following values in 'buchung':
kursnr:你想预定的课程的课程编号。在图书馆的预定系统中，很容易就可以找到。lernraum number, here u can find it.https://buchung.hsz.rwth-aachen.de/angebote/aktueller_zeitraum/_Lernraumbuchung.html
email:你的邮箱。ur email
sex:性别。男：M；女:W                       male:M  female:W
vorname:名字。首字母大写                    first name. Initial capital
name:姓。首字母大写                         last name. Initial capital
strasse:街道和号码                          street and number.
ort:邮编和地址，务必注意格式是52076 Aachen.   zip code and city name. format must be: 52074 Aachen
matnr:六位学号                              six-figure student number
telefon:带前缀的手机号                          phone number
time:自习室开放时间，格式必须为8.00 - 16.30。   lernraum open time. format must be :8.00 - 16.30
    开放时间即为程序开始运行抢座的时间，
    在此之前程序会进入倒计时。
    因此务必保证开放时间的准确。                                      
其余内容可不修改.                           other values dont need to change
'''

#只修改info下的信息为自己的就可以了，不知道的可以不用管。
buchung = {'info': {'id': 0, 'username': 'suiyi', 'email': 'example@email.com', 'sex': 'M', 'vorname': 'Feieie', 'name': 'Xu', 'strasse': 'Ponttorstr.1','ort': '52074  Aachen', 'status': 'S-RWTH', 'matnr': '404093', 'telefon': '00491799860915'}, 
            'id': 0, 'username': 'suiyi', 'ort': 'suiyi', 'kursnr': '08511007'}

# 要约哪个自习室和时间，就将哪行的switch改为1.
# switch=1，预定。0不预定。
#  让后运行程序就可以了

lernraumList = [
    # {'switch':1,'ort':'Semi90','kursnr':"08411027",'time':'08:00-14:00'},
    # {'switch':1,'ort':'SemiTemp','kursnr':"08411031",'time':'08:00-14:00'},
    {'switch': 1, 'ort': 'Bib1', 'kursnr': "08511007", 'time': '08:00-14:00'},
    {'switch': 0, 'ort': 'Bib2', 'kursnr': "08611004", 'time': '08:00-14:00'},

    # {'switch':0,'ort':'Semi90','kursnr':"08411028",'time':'14:00-20:00'},
    # {'switch':0,'ort':'SemiTemp','kursnr':"08411032",'time':'14:00-20:00'},
    {'switch': 0, 'ort': 'Bib1', 'kursnr': "08511008", 'time': '14:00-20:00'},
    {'switch': 0, 'ort': 'Bib2', 'kursnr': "08611005", 'time': '14:00-20:00'}
]

stop_thread_flag = False

def doRandom():
    buchungList = []
    for lr in lernraumList:
        if(lr['switch'] == 1):
            buchungBuffer = buchung.copy()
            buchungBuffer['kursnr'] = lr['kursnr']
            buchungBuffer['ort'] = lr['ort']
            print(lr['ort']+":"+lr['time'])
            buchungList.append(buchungBuffer)
    if(buchungList):
        threads = []
        for bc in buchungList:
            t = RandomThreading(bc)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()


class RandomThreading(threading.Thread):
    def __init__(self, buchung):
        threading.Thread.__init__(self)
        self.buchung = buchung

    def run(self):
        global stop_thread_flag
        is_not_bucht = True

        while is_not_bucht and stop_thread_flag == False:
            is_not_bucht = not (LernraumInfo().random_buchen(self.buchung))
        print(self.buchung['ort']+',预定成功')
        stop_thread_flag = True


doRandom()
