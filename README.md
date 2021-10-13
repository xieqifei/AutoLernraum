# RWTH自习室自动化程序2

[中文](https://github.com/xieqifei/AutoLernraum)|[Deutsch](https://github.com/xieqifei/AutoLernraum/blob/main/README_DE.md)(Here finden Sie Readme auf Deutsch)

## 1.快速开始

1. 安装Chrome浏览器
2. 安装python3.9及以上版本
3. 点击绿色的Code按钮，下载zip包，并解压
4. 使用编辑器打开文件目录下的random_test.py，修改email、sex、vorname、name、strasse、ort、matnr、telefon。注意格式保持一直。格式错误抢座会失败。

```python
buchung = {'info': {'id': 0, 'username': 'suiyi', 'email': 'example@email.com', 'sex': 'M', 'vorname': 'Feieie', 'name': 'Xu', 'strasse': 'Ponttorstr.1','ort': '52074  Aachen', 'status': 'S-RWTH', 'matnr': '404093', 'telefon': '00491799860915'}, 
'id': 0, 'username': 'suiyi', 'ort': 'suiyi', 'kursnr': '08511007'}
```

5. 选择要预定的位置，分了图一和图二，以及上午和下午。要抢哪个，哪个就把哪行switch改为1，可以选择多个。这些信息在学校预定网页都可以找到，如果没有你要的自习室，自行添加一行就可以了。区分自习室的只是kursnr。

```python
lernraumList = [
    {'switch': 1, 'ort': 'Bib1', 'kursnr': "08511007", 'time': '08:00-14:00'},
    {'switch': 0, 'ort': 'Bib2', 'kursnr': "08611004", 'time': '08:00-14:00'},

    {'switch': 0, 'ort': 'Bib1', 'kursnr': "08511008", 'time': '14:00-20:00'},
    {'switch': 0, 'ort': 'Bib2', 'kursnr': "08611005", 'time': '14:00-20:00'}
]
```

6. 使用pyhton运行random_test.py。

## 2.简单说明

每20秒刷新一次，只要有位置就预定，不会自动停止，直到把所有要抢的自习室都预定到了位置为止。。自行谷歌搜索如何设置定时运行程序抢座。主要用处还是挂机捡漏。。不会后台运行，需要保持电脑不待机。

