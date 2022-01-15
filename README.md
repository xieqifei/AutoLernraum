# RWTH自习室自动化程序

[中文](https://github.com/xieqifei/AutoLernraum)|[Deutsch](https://github.com/xieqifei/AutoLernraum/blob/main/README_DE.md)

![image-20211117182444929](https://i.loli.net/2021/11/18/FoOYsD5hGQMcrIA.png)

## 1.快速开始

1. 安装Chrome浏览器
2. 安装python3.9及以上版本
3. 点击绿色的Code按钮，下载zip包，并解压
4. 使用编辑器打开文件目录下的random_test.py，修改email、sex、vorname、name、strasse、ort、matnr、telefon。注意格式保持一致。格式错误抢座会失败。

```python
buchung = {'info': {'id': 0, 'username': 'suiyi', 'email': 'example@email.com', 'sex': 'M', 'vorname': 'Feieie', 'name': 'Xu', 'strasse': 'Ponttorstr.1','ort': '52074  Aachen', 'status': 'S-RWTH', 'matnr': '404093', 'telefon': '00491799860915'}, 
'id': 0, 'username': 'suiyi', 'ort': 'suiyi', 'kursnr': '08511007'}
```

5. 选择要预定的位置，分了图一和图二，以及上午和下午。要抢哪个，就把哪行switch改为1，可以选择多个。自习室信息在学校预定网页都可以找到，如果没有你要的自习室，自行添加一行就可以了。区分自习室的只是kursnr。

```python
lernraumList = [
    {'switch': 1, 'ort': 'Bib1', 'kursnr': "08511007", 'time': '08:00-14:00'},
    {'switch': 0, 'ort': 'Bib2', 'kursnr': "08611004", 'time': '08:00-14:00'},

    {'switch': 0, 'ort': 'Bib1', 'kursnr': "08511008", 'time': '14:00-20:00'},
    {'switch': 0, 'ort': 'Bib2', 'kursnr': "08611005", 'time': '14:00-20:00'}
]
```

6. 使用pyhton运行random_test.py。

7. 程序每20秒刷新一次，只要有位置就预定，不会自动停止，直到把所有要抢的自习室都预定到了位置为止。。主要用处还是挂机捡漏。。不会后台运行，需要保持电脑不待机。测试环境，仅windows。

8. 出现refresh page时，表示程序正常运行。

   ![image-20211117180309698](https://i.loli.net/2021/11/18/Xkz2CUGAlWbupqw.png)

## 2.定时抢座

1. 打开test_selenium.py
2. 修改lernraum变量里的switch，将想抢的自习室地点时间那行的switch值修改为1，其余置0。每次运行前都需要更改。
3. 按照程序注释，修改buchung变量中的值为个人信息。
4. 运行test_selenium.py
5. 抢座程序只能在开始抢座之前20分钟内运行，比如8.00-14.00点的座，最早的运行时间是13:40，那么之后程序会开始倒计时，14点准时进入网页抢座。你可以将lernraum变量中time变量中的14.00设置为离你较近的一个时间进行测试，来了解程序运行的原理。
6. 出现倒计时时程序正常运行
7. 若出现buchen success则预定一定成功，如果出现buchen failed，预定不一定失败，以邮件为准。

![image-20211117180736738](https://i.loli.net/2021/11/18/BbOo1FpGwiJjrWS.png)

## 3.注意事项

1. 长时间运行random_test.py程序可导致你的家庭网络IP被buchung网站封禁，重新启动你的路由器可恢复访问。建议使用vpn或者在校园网运行。
2. 由于预定网页经常发生变化，如果正常运行一段时间后报错，可以到github上重新下载最新的版本。如果我更新不及时，可以提交issue。

