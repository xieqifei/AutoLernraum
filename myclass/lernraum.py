# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
from .db import BuchenListApi
import time
import datetime
import traceback
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import threading


raums = []
threadLock = threading.Lock()

class LernraumInfo():
    def __init__(self):
        self.url1 = "https://buchung.hsz.rwth-aachen.de/angebote/aktueller_zeitraum/_Lernraumbuchung.html"
        self.url2 = "https://buchung.hsz.rwth-aachen.de/cgi/anmeldung.fcgi"
        self.raums = []
        self.url_fh ="https://buchung.hsz.rwth-aachen.de/angebote/aktueller_zeitraum/_Lernplatzbuchung_FHB.html"
        self.buchung={}
    # 计算content_length
    def __get_content_length(self, data):
        length = len(data.keys()) * 2 - 1
        total = ''.join(list(data.keys()) + list(data.values()))
        length += len(total)
        return str(length)

    #打印日志信息
    def __log(self,msg):
        if('username' in self.buchung):
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+', user '+self.buchung['username']+'`s log:'+msg)
        else:
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+': '+msg)

    #验证预定时间和当前时间是否接近
    def __is_time_close(self,timestr):
        try:
            buchungTimeHour = int(timestr.split('-')[0].split('.')[0])
            buchungTimeMinute = int(timestr.split('-')[0].split('.')[1])
            diffirenzBuchtimeToNull = buchungTimeHour*3600+buchungTimeMinute*60
            utcTime = datetime.datetime.now(datetime.timezone.utc)
            berlinTime = utcTime + datetime.timedelta(hours=2)
            berlinTimeHour = berlinTime.hour
            berlinTimeMinute = berlinTime.minute
            berlinTimeSecond = berlinTime.second
            diffirenzBerlintimeToNull = berlinTimeHour*3600+berlinTimeMinute*60+berlinTimeSecond
            diffirenz =diffirenzBerlintimeToNull-diffirenzBuchtimeToNull 
            if(diffirenz>=0 and diffirenz<20):
                self.__log('booking start')
                return True
            elif(diffirenz < 0):
                self.__log('countdown to booking start: '+str(-diffirenz)+' Sceconds')
                return False
            else:
                self.__log('ur booking out of time, please check ur booking time '+timestr)
                return False
        except Exception as e:
            traceback.print_exc()
            self.__log('Error: format of time in "buchung" Variable is error, right format：8.30 - 16.30')
        
    #判断是否为预定成功的返回页面
    def __is_buchung_successful(self,page_html):
        if "kostenfrei" in str(page_html):
            self.__log('booking success. you will get a email from Uni in 10 minutes')
            return True
        else:
            self.__log('Schade, booking failed.')
            return False

    #判断是否位置已被分发完
    def __is_ausgebucht(self,page_html):
        if("ausgebucht" in str(page_html)):
            self.__log('booking failed, ausgebucht.')
            return True
        else:
            self.__log('noch nicht ausgebucht')
            return False
    
    def get_raum_list_temp(self):
        return self.__get_raum_list()
        
    # 爬取所有的自习室信息
    def __get_raum_list(self):
        rep = requests.get(self.url1)
        if(rep.status_code == 200):
            raums_temp = BuchenListApi().get_kurs()
            try:
                soup = BeautifulSoup(rep.text, "html.parser")
                raums = soup.find_all(name="tr", attrs={"class" :["bs_odd","bs_even"]})
                for i in range(len(raums)):
                    ort = raums[i].select("td.bs_sort")[0].text
                    tag = raums[i].select("td.bs_stag")[0].text
                    zeit = raums[i].select("td.bs_szeit")[0].text
                    kursnr = raums[i].select("td.bs_sknr")[0].text
                    code = soup.find(attrs={"name": "BS_Code"}).get("value")
                    try:
                        kursid = raums[i].select("td.bs_sbuch > input")[
                            0].get("name")
                        kursvalue = raums[i].select("td.bs_sbuch > input")[
                            0].get("value")
                        self.raums.append({"ort": ort, "tag": tag, "zeit": zeit, "code": code,
                                        "kursid": kursid, "kursvalue": kursvalue, 'kursnr': kursnr})
                    except:
                        for raum in raums_temp:
                            if(kursnr == raum['kursnr']):
                                self.raums.append(raum)
                # 更新数据库
                print('从网站获取到自习室列表')
                self.__log(str(self.raums))
                BuchenListApi().update_kurs(self.raums)
            except Exception as e:
                print('从数据库获取到自习室列表')
                traceback.print_exc()
                self.raums = raums_temp
        else:
            print("请求buchen连接失败")
            return False
        return True

    def __get_a_raum(self,i):
        global raums
        global threadLock
        raum = raums[i]
        data = {
            'BS_Code': raum['code'],
            raum['kursid']: raum['kursvalue']
        }
        headers = {
            'Host': 'buchung.hsz.rwth-aachen.de',
            'Origin': 'https://buchung.hsz.rwth-aachen.de',
            'Referer': 'https://buchung.hsz.rwth-aachen.de/angebote/aktueller_zeitraum/_Lernraumbuchung.html',
            'Content-Length': self.__get_content_length(data),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        resp = requests.request(
            "POST", self.url2, headers=headers, data=data)
        if(resp.status_code == 200):
            try:
                soup = BeautifulSoup(resp.text, 'html.parser')
                zeit_list = soup.select_one(
                    "#bs_form_main > div > div.bs_etvg").contents
                termins = []
                for zeit in zeit_list:
                    if(hasattr(zeit, 'select')):
                        week = zeit.select_one("div.bs_tag.alr").text
                        tag = zeit.select_one(
                            "div.bs_text_bold.pointer").text
                        time = zeit.select_one("div.bs_time").text
                        if(zeit.select_one("input")):
                            if(str(zeit.select_one("input").get("value")) == "Warteliste"):
                                status = 2
                            else:
                                status = 1
                        else:
                            status = 0
                        if(status == 0):
                            termins.append(
                                {"week": week, 'tag': tag, 'time': time, 'status': status, 'kursnr': raum['kursnr'], 'ort': raum['ort']})
                threadLock.acquire()
                raums[i]['termins'] = termins
                threadLock.release()
            except:
                print("爬取预定时间报错")
                return False
        else:
            print("请求预定时间链接失败")
            return False

    # 爬取自习室预定时间
    def get_raums(self):
        global raums
        raums = self.raums
        threads = []
        if(self.__get_raum_list()):
            for i in range(len(self.raums)):
                t=threading.Thread(target=self.__get_a_raum,args=(i,))
                threads.append(t)
                t.start()
                time.sleep(0.1)
            for t in threads:
                t.join()
        else:
            print("没有获取到自习室信息")
            return False
        return raums

    # 获取bscode和kursid
    def __get_kurs_code_and_id(self, kursnr):
        rep = requests.get(self.url1,timeout=60)
        if(rep.status_code == 200):
            try:
                soup = BeautifulSoup(rep.text, "html.parser")
                kurs = soup.find(name="td", attrs={
                                 'class': 'bs_sknr'}, text=kursnr).parent
                if(kurs.select("td.bs_sbuch > input")[0].get("value")):
                    code = soup.find(attrs={"name": "BS_Code"}).get("value")
                    kursid = kurs.select("td.bs_sbuch > input")[0].get("name")
                    return {"code": code, "kursid": kursid}
                else:
                    return False
            except Exception as e:
                traceback.print_exc()
                return False

    # 获取fid
    def __get_fid(self, code_id_dic):
        data = {
            'BS_Code': code_id_dic['code'],
            code_id_dic['kursid']: 'buchen'
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': self.__get_content_length(data),
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'buchung.hsz.rwth-aachen.de',
            'Origin': 'https://buchung.hsz.rwth-aachen.de',
            'Referer': self.url1,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        }
        resp = requests.request("POST", self.url2, headers=headers, data=data,timeout=300)
        soup = BeautifulSoup(resp.text, 'html.parser')
        try:
            if(soup.select_one('#bs_form_main input[value=buchen]')):
                pass
            else:
                self.__log('ausgebucht')
                return False
            self.__log('found buchen btn')
            fid = soup.select_one(
                "body > form > input[type=hidden]").get("value")
            self.__log("get fid:"+fid)
            return fid
        except Exception as e:
            return False

    # 获取表单
    def __get_form_list(self, fid):
        morgen = datetime.date.today()+datetime.timedelta(days=1)
        termin = morgen.strftime("%Y-%m-%d")
        data = {
            'fid': fid,
            'BS_Termin_'+termin: 'buchen'
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': self.__get_content_length(data),
            'Content-Type': 'application/x-www-form-urlencoded',
            'DNT': '1',
            'Host': 'buchung.hsz.rwth-aachen.de',
            'Origin': 'https://buchung.hsz.rwth-aachen.de',
            'Pragma': 'no-cache',
            'Referer': 'https://buchung.hsz.rwth-aachen.de/cgi/anmeldung.fcgi',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        }
        resp = requests.request("POST", self.url2, headers=headers, data=data,timeout=300)
        if(resp.status_code == 200):
            # self.__log("表单页面代码"+resp.text)
            return resp.text
        return False
    # 提交预定，获取formdata

    def __get_formdata(self, fid, info):
        # termin = time.strftime("%Y-%m-%d", time.localtime())
        morgen = datetime.date.today()+datetime.timedelta(days=1)
        termin = morgen.strftime("%Y-%m-%d")
        #填写表单
        data = {
            'fid': fid,
            'Termin': termin,
            'pw_email': '',
            'pw_pwd_'+fid: '',
            'sex': info['sex'],
            'vorname': info['vorname'],
            'name': info['name'],
            'strasse': info['strasse'],
            'ort': info['ort'],
            'statusorig': info['status'],
            'matnr': info['matnr'],
            'email': info['email'],
            'telefon': info['telefon'],
            'tnbed': '1'
        }
        self.__log("发送的表单数据："+str(data))
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': self.__get_content_length(data),
            'Content-Type': 'application/x-www-form-urlencoded',
            'DNT': '1',
            'Host': 'buchung.hsz.rwth-aachen.de',
            'Origin': 'https://buchung.hsz.rwth-aachen.de',
            'Pragma': 'no-cache',
            'Referer': 'https://buchung.hsz.rwth-aachen.de/cgi/anmeldung.fcgi',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        }
        resp = requests.request("POST", self.url2, headers=headers, data=data,timeout=300)
        # print(resp.text)
        if(resp.status_code == 200):
            try:
                soup = BeautifulSoup(resp.text, 'html.parser')
                formdata = soup.find(name='input', attrs={
                                     'name': '_formdata'}).get('value')
                # self.__log('返回的确认提交页面'+resp.text)
                return {'formdata':formdata,'html':resp.text}
            except Exception as e:
                self.__is_ausgebucht(resp.text)
                return False

    # 确定预定信息
    def __confirm_buchung(self, fid, info, formdata,html):
        morgen = datetime.date.today()+datetime.timedelta(days=1)
        termin = morgen.strftime("%Y-%m-%d")
        #判断是否包含邮件重新输入的input
        soup = BeautifulSoup(html, 'html.parser')
        inputs = soup.find_all('input')
        data = {}
        for input in inputs:
            if(str(input.get('type')) != 'submit' and str(input.get('type')) !="reset"):
                data[str(input.get('name'))] = input.get('value')
            if("email_check" in str(input.get('name'))):
                data[str(input.get('name'))] = info['email']
                self.__log("检测到需要重新输入email")
        self.__log('最后确认提交表单'+str(data))
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': self.__get_content_length(data),
            'Content-Type': 'application/x-www-form-urlencoded',
            'DNT': '1',
            'Host': 'buchung.hsz.rwth-aachen.de',
            'Origin': 'https://buchung.hsz.rwth-aachen.de',
            'Pragma': 'no-cache',
            'Referer': 'https://buchung.hsz.rwth-aachen.de/cgi/anmeldung.fcgi',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        }
        resp = requests.request("POST", self.url2, headers=headers, data=data,timeout=300)
        # self.__log("确认后返回页面"+resp.text)
        self.__is_ausgebucht(resp.text)
        return self.__is_buchung_successful(resp.text)

    # requests预定一个位置
    def buchen_platz_via_requests(self, buchung):
        for value in buchung['info'].values():
            if(value == ""):
                self.__log("用户'"+buchung['username']+"'的信息不完整")
                return False
        code_id_dic = self.__get_kurs_code_and_id(buchung['kursnr'])
        self.__log(str(code_id_dic))
        if(code_id_dic):
            i=0
            while i<90:
                fid=self.__get_fid(code_id_dic)
                if(fid):
                    break
                else:
                    self.__log('requests refresh page')
                    time.sleep(2)
        else:
            self.__log('获取预定主页信息失败')
            return False
        if(fid):
            form_html = self.__get_form_list(fid)
            if(form_html):
                time.sleep(7)
                formAndHtml = self.__get_formdata(fid, buchung['info'])
                if(formAndHtml):
                    return self.__confirm_buchung(fid, buchung['info'], formAndHtml['formdata'],formAndHtml['html'])
                else:
                    self.__log('未获取到再次确认提交页面')
                    return False
            else:
                self.__log('未获取到信息表单页面')
                return False
        else:
            self.__log('刷新超时，在3分钟之内没有找到可以预定的座位。可尝试再次运行程序')
            return False
       
    #selenium实现代码
    # selenium点击buchen按钮
    def __click_buchen_btn(self, buchung, driver):
        try:
            second_buchen_btn = driver.find_element_by_xpath(
                '//input[@value="buchen"]')
            second_buchen_btn.click()
            self.__log('found available booking button')
            return True
        except Exception as e:
            print(driver.page_source)
            traceback.print_exc()
            return False

    # selenium填写表单
    def __fill_form(self, urinfo, driver):
        fill_form_script = "bsform.sex.value='{sex}';bsform.vorname.value='{vorname}';bsform.name.value='{name}';bsform.strasse.value='{strasse}';bsform.ort.value='{ort}';bsform.statusorig.value='{status}';bsform.bemerkung.value='Schwarz';bsform.tnbed.checked=true;".format(
            sex=urinfo['sex'], vorname=urinfo['vorname'], name=urinfo['name'], strasse=urinfo['strasse'], ort=urinfo['ort'], status=urinfo['status'])
        matnr_fill_script = "bsform.matnr.value='{matnr}';bsform.email.value='{email}';bsform.telefon.value='{telefon}';bsform.submit()".format(matnr=urinfo['matnr'], email=urinfo['email'], telefon=urinfo['telefon'])
        try:
            #等待填写表单页面加载
            form_fill_page_finished = WebDriverWait(driver, 9).until(           
        EC.presence_of_element_located((By.NAME,'sex')))
            self.__log('inject JS Code into web page')
            status = Select(driver.find_element_by_name('statusorig'))
            status.select_by_value(urinfo['status'])
            # js注入填写表单
            driver.execute_script(fill_form_script)
            time.sleep(6)
            driver.execute_script(matnr_fill_script)
            
            confirm_page_finished = WebDriverWait(driver, 30).until(           
        EC.text_to_be_present_in_element((By.CLASS_NAME,'bs_text_red'),'überprüfen'))
            try:
                email2 = driver.find_element_by_xpath(
                    '//input[starts-with(@name,"email_check")]')
                email2.send_keys(urinfo['email'])
            except:
                self.__log('email comfired')
            confirm_submit_btn = driver.find_element_by_xpath(
                '//input[@type="submit"]')
            confirm_submit_btn.click()
            return True
        except Exception as e:
            print(driver.page_source)
            traceback.print_exc()
            return False

    def buchen_platz_via_selenium(self, buchung):
        self.buchung = buchung
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        prefs = {"profile.managed_default_content_settings.images": 2}
        option.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=option,executable_path=ChromeDriverManager().install())
        driver.set_page_load_timeout(300)
        driver.set_script_timeout(90)
        i = 0
        clear_black_script = "document.querySelector('#bs_content > form').setAttribute('target','_self')"
        while True:
            if(self.__is_time_close(buchung['time'])):
                break
            else:
                time.sleep(1)
        while i<60:
            driver.get(self.url1)
            i=i+1
            self.__log('refresh page')
            try:
                driver.execute_script(clear_black_script)
                first_buchen_btn = driver.find_element_by_xpath(
                    '//td[contains(text(), "'+buchung['kursnr']+'")]/following-sibling::td[@class="bs_sbuch"]')
                # # buchen_click = driver.find_element_by_xpath(
                # #     '//td[contains(text(), "08411029")]/following-sibling::td[@class="bs_sbuch"]')
                first_buchen_btn.click()
                second_buchen_btn = driver.find_element_by_xpath(
                '//input[@value="buchen"]')
                break
            except Exception as e:
                time.sleep(1)
        if(self.__click_buchen_btn(buchung, driver)):
            if(self.__fill_form(buchung['info'], driver)):
                if(self.__is_buchung_successful(driver.page_source)):
                    self.__log('success')
                    return True
                else:
                    self.__log('failed')
                    print(driver.page_source)
                    driver.quit()
                    return False
            else:
                self.__log('filling form failed')
                driver.quit()
                return False
        else:
            self.__log('not found available button, may out of booking')
            driver.quit()
            return False

    #随机预定位置
    def random_buchen(self, buchung):
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        prefs = {"profile.managed_default_content_settings.images": 2}
        option.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=option,executable_path=ChromeDriverManager().install())
        driver.set_page_load_timeout(300)
        driver.set_script_timeout(90)
        clear_black_script = "document.querySelector('#bs_content > form').setAttribute('target','_self')"
        while True:
            driver.get(self.url1)
            self.__log('refresh page')
            try:
                driver.execute_script(clear_black_script)
                first_buchen_btn = driver.find_element_by_xpath(
                    '//td[contains(text(), "'+buchung['kursnr']+'")]/following-sibling::td[@class="bs_sbuch"]')
                # # buchen_click = driver.find_element_by_xpath(
                # #     '//td[contains(text(), "08411029")]/following-sibling::td[@class="bs_sbuch"]')
                first_buchen_btn.click()
                second_buchen_btn = driver.find_element_by_xpath(
                '//input[@value="buchen"]')
                break
            except Exception as e:
                time.sleep(20)
        if(self.__click_buchen_btn(buchung, driver)):
            if(self.__fill_form(buchung['info'], driver)):
                if(self.__is_buchung_successful(driver.page_source)):
                    self.__log('success')
                    return True
                else:
                    self.__log('failed')
                    print(driver.page_source)
                    driver.quit()
                    return False
            else:
                self.__log('filling form failed')
                driver.quit()
                return False
        else:
            self.__log('not found available button, may out of booking')
            driver.quit()
            return False

