# RWTH自习室自动化程序2

[中文](https://github.com/xieqifei/AutoLernraum)|[Deutsch](https://github.com/xieqifei/AutoLernraum/blob/main/README_DE.md)(Here finden Sie Readme auf Deutsch)

## 1.开篇

抢座程序分为两种，基于selenium的浏览器自动化程序，和基于requests库的http模拟请求程序。

为了成功运行程序，请确保你的计算机安装了Python。如何安装Python可自行网上搜索。两种程序命中率均比较高。可任选一种运行。程序会不定期进行更新，请注意关注。

## 2.基于Selenium库的浏览器自动化程序（推荐，比较稳定）

顾名思义，你除了需要在你的电脑中安装Python以外，还要在你的电脑里安装Chrome浏览器。之所以使用自动化，是因为它可能会比模拟http请求更加可靠。

1. 安装Python环境
2. 安装任意版本Chrome浏览器
3. 打开`test_selenium.py`文件，修改`buchung`变量里的个人信息和需要预定的自习室信息

```python
buchung = {'time': '08.00 - 16.30', 'kursnr': '08411027','info':{ 'username': '', 'email': 'example@gmail.com', 'sex': 'M', 'vorname': 'Ivan', 'name': 'Natanael', 'strasse': 'Pontstr.23', 'ort': '52076  Aachen', 'status': 'S-RWTH', 'matnr': '468389', 'telefon': '00491748068847'}}
```

> 在变量buchung中,需要修改的数据如下：
>
> kursnr:你想预定的自习室的编号。例如08411027为Semi90。在图书馆的预定系统中，很容易就可以找到。图书馆系统链接：https://buchung.hsz.rwth-aachen.de/angebote/aktueller_zeitraum/_Lernraumbuchung.html
>
> time:自习室开门时间 - 关门时间。开门时间将用作程序加载预定网页的时间。
>
> email:你的邮箱。
>
> sex:性别。男：M；女:W
>
> vorname:名字。首字母大写
>
> name:姓。首字母大写
>
> strasse:街道和号码
>
> ort:邮编和地址，务必注意格式是52076 Aachen.邮编和地址以空格隔开
>
> matnr:六位学号
>
> telefon:带前缀的手机号
>
> 其余内容可不修改。务必注意在每个字符串两边都有单引号

4. 保存文件，用Python运行`test_selenium.py`。
5. 同样的，如果你预定的程序8点开抢，那么建议你在7:59以前运行它。程序会自动进入倒计时，直到8点开始加载预定网页。并自动实现预定流程。

## 3.基于Requests库的预定程序（测试中）

1. 安装Python环境
2. 点击网页上面那个绿色的`Code`按钮，选择下载为zip，将整个程序文件从github下载到本地并解压。
3. 使用任意编辑器打开`test_requests.py`，修改变量buchung

```python
buchung = {'time': '08.00 - 16.30', 'kursnr': '08411027','info':{ 'username': '', 'email': 'example@gmail.com', 'sex': 'M', 'vorname': 'Ivan', 'name': 'Natanael', 'strasse': 'Pontstr.23', 'ort': '52076  Aachen', 'status': 'S-RWTH', 'matnr': '468389', 'telefon': '00491748068847'}}
```

> 在变量buchung中,需要修改的数据如下：
>
> kursnr:你想预定的自习室的编号。例如08411027为Semi90。在图书馆的预定系统中，很容易就可以找到。图书馆系统链接：https://buchung.hsz.rwth-aachen.de/angebote/aktueller_zeitraum/_Lernraumbuchung.html
>
> time:自习室开门时间 - 关门时间。开门时间将用作程序加载预定网页的时间。
>
> email:你的邮箱。
>
> sex:性别。男：M；女:W
>
> vorname:名字。首字母大写
>
> name:姓。首字母大写
>
> strasse:街道和号码
>
> ort:邮编和地址，务必注意格式是52076 Aachen.邮编和地址以空格隔开
>
> matnr:六位学号
>
> telefon:带前缀的手机号
>
> 其余内容可不修改。务必注意在每个字符串两边都有单引号

3. 保存文件，并用python运行`test_requests.py`文件。若你不知道如何运行python文件，建议上网查询。
4. 运行后，程序会在两分钟之内，以2秒为间隔刷新，直到发现你指定的自习室可以预定并完成预定，或两分钟后依然没有发现可以预定的位置为止。如果你需要抢的自习室在8点开始，那么建议你在7点59的时候开始运行程序。。程序结束5分钟后，你将收到来自学校邮箱的，预定成功邮件。若没有收到，那么抢座失败。

## 4.定时运行

也许你想早起的时候睡个懒觉。那么，你可以试试使用计算机定时运行python程序。

Windows和mac系统的定时运行方法，你可以自行谷歌搜索。因为我用到过树莓派和云函数进行定时抢座，所以这里只讲Linux和基于腾讯云函数的定时方法。

**Linux系统下的定时运行**：

你需要用到linux自带的定时软件crontab。非常简单，

1. 输入指令,开始编辑时间表

```shell
crontab -e
```

2. 按下`i`开始编辑,编辑内容如下

```shell
0,30 8 * * * python -u /home/***/test_requests.py >result.log 2>&1
```

将上述`/home/***/test_requestes.py`改为你放置该文件的地址即可。

此行代码表示。将在每日的8点和八点半执行python此程序，并将python的输出保存到定时程序文件夹里的result.log文件里

3. 按下`:wq`保存退出

**利用腾讯云函数**

腾讯云函数，有非常充足的免费运行空间。可以直接把程序放到上面执行，应该很少有人会用到吧，所以简单讲讲。

1. 建立一个新函数，将完整的程序上传。
2. 新建定时触发器，自定义触发周期如下，因为定时器是以北京时间为准，所以需要考虑时差问题。

```shell
0 0,30 14 * * *
```

3. 函数入口为`test_serverless.main_handler`

## 5.结尾

如果你对程序的运行原理感兴趣，那么你可以看看`/myclass/lernraum.py`文件，所有的抢座程序都在这个文件中，因为文件经过了多次修改，所以看起来可能有点杂乱无章。

注意：请不要尝试修改现有代码，尤其是延时代码，修改可能会对学校服务器造成冲击！

# 6.更新

## 25.07.2021 

1. 修改刷新方式，刷新出buchen按钮的时间减少8-10秒
2. 减少了Request库程序，页面等待延时时长。
3. 删除了Random_buchen方法。
4. 添加了预定成功页面和预定位置已分发完的页面判断，并提供相应输出。
5. 删除了不重要信息日志



## 29.07.2021

1. 在buchung字典中添加了time键值对，用于确认自习室开始分发的时间。
2. selenium库的程序中，可以在预定当天提前更久运行程序。自动判断是否到达分发时间。