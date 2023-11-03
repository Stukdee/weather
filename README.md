# 如何用python爬取温度

## 需要的库:

* re
* urllib
* bs4
* cutecharts

## 整体逻辑:

1. 向网站发送请求
2. 解析html
3. 以折线统计图的形式呈现

## 1.导入库:

```python
import re #提供对正则表达式的支持，这是用于模式匹配和字符串操作的强大工具。
import urllib.request #提供发出 HTTP 请求的功能，例如打开 URL 并检索其内容。
from bs4 import BeautifulSoup #BeautifulSoup用于解析网页的HTML内容并提取特定数据。
from cutecharts.charts import Line #cutecharts库提供的Line类创建折线图。
```

## 2.获取网站html:

以深圳为例：[深圳天气预报,深圳7天天气预报,深圳15天天气预报,深圳天气查询 (weather.com.cn)](http://www.weather.com.cn/weather/101280601.shtml)

```python
url = 'http://www.weather.com.cn/weather/101280601.shtml' #设定一个网站。
response = urllib.request.urlopen(url) #向网站发送请求。
html = response.read().decode('utf-8') #对获取的html进行解码。
soup = BeautifulSoup(html,'lxml') #整理html。
```

## 3.存储获取的信息:

这里的流程比较复杂

1. 首先需要两个数组，或者可以用三个数组分别用来存储最高温度、最低温度和平均温度
2. 提取html里面温度信息并用数组存储

```python
y_data_1=[] #用来存储最高温度。
y_data_2=[] #用来存储最低温度。
y_data_3=[] #用来存储平均温度。
list(y_data_1)
list(y_data_2)
list(y_data_3)
```

获取城市名称

在浏览器按f12打开开发者模式![1699026477253](image/Untitled-1/1699026477253.png)

通过开发者模式可以看到“深圳"一词对应的是href属性=链接。

```python
namecity = str(soup.find_all(href=url)[0].string) #提取href属性=url的信息并转换成str字符串类型。
print(namecity) #输出城市名称。
```

现在开始存储信息

一共有七天的温度，所以需要循环七天

通过开发者模式可以知道温度在html里的位置

![1699027558381](image/Untitled-1/1699027558381.png)

可以看出位置是在class属性="tem"的标签里面,span标签是最高温度而i标签是最低温度

这里有一个特殊问题，紫色方框里面只有一个温度，在晚上都是只显示一个温度而白天时不会，这里的问题稍后解决

```python
for i in range(7): #循环7次对应七天。
    tq = str(soup.find_all(class_='tem')[i]) #提取所有class属性为tem的内容。
    bds = r'\d+' #提取数字的表达式，整数类型对应的格式字符串是d。
    wendu = re.findall(bds,tq) #利用re库提取tem内容的数字。
    print(wendu) #输出提取的数字有助于检查。
    y_data_1.append(int(wendu[0])) #将最高温度存储到数组里。
    y_data_2.append(int(wendu[1])) #将最低温度存储到数组里。
    y_data_3.append((int(wendu[0])+int(wendu[1]))/2) #将平均温度存储到数组里。
```

但是运行后就会有一个问题

![1699028357717](image/Untitled-1/1699028357717.png)

list index out of range 的意思是超出列表范围

因为晚上打开网站，今天的温度只显示一个![1699028517991](image/Untitled-1/1699028517991.png)

而代码中的每次循环都要求将最高温度和最低温度赋值，所以需要进行改善

```python
for i in range(7):
    tq = str(soup.find_all(class_='tem')[i])
    bds = r'\d+'
    wendu = re.findall(bds,tq)
    print(wendu)
    y_data_1.append(int(wendu[0]))
    try: #对此代码进行正误判断。
        y_data_2.append(int(wendu[1]))
    except IndexError as e: #如果超出范围。
        y_data_2.append(0) #将最低温度赋予0。
    try: #对此代码进行正误判断。
        y_data_3.append((int(wendu[0])+int(wendu[1]))/2)
    except IndexError as e: #如果wendu[1]超出范围。
        y_data_3.append((int(wendu[0])+0)/2) #直接(wendu[0]+0)/2。
print(y_data_1) #输出最高温度数组。
print(y_data_2) #输出最低温度数组。
print(y_data_3) #输出平均温度数组。
```

![1699028916215](image/Untitled-1/1699028916215.png)

可以看到运行比较成功

输出的最坏一行是html,也就是折线统计图的网页

## 4.生成折线统计图：

将七天的温度可视化有助于更方便的浏览

```python
x_data = ['今天', '明天', '后天', '大后天', '大大后天', '大大大后天', '大大大大后天'] #统计图横轴内容。
chart = Line(namecity + "未来7天温度(摄氏度)") #城市+标题。
chart.set_options(
    labels=x_data,
    x_label="日期",
    y_label="温度",
    legend_pos="upRight"
) #定义基础信息。
chart.add_series("最高", y_data_1) #将最高温度添加到折线统计图里。
chart.add_series("最低", y_data_2) #将最低温度添加到折线统计图里。
chart.add_series("平均",y_data_3) #将平均温度添加到折线统计图里。
#chart.render_notebook() 这个是在终端输出统计图。
chart.render() #生成折线统计图的html文件。
```

![1699029371128](image/Untitled-1/1699029371128.png)

## 5.源代码：

```python
import re
import urllib.request
from bs4 import BeautifulSoup
from cutecharts.charts import Line
pd = str(input("输入城市代码:")) #更方便的获取获取网站
url = 'http://www.weather.com.cn/weather/'+pd+'.shtml'
response = urllib.request.urlopen(url)
html = response.read().decode('utf-8')
soup = BeautifulSoup(html,'lxml')
y_data_1=[]
y_data_2=[]
y_data_3=[]
list(y_data_1)
list(y_data_2)
list(y_data_3)
namecity = str(soup.find_all(href=url)[0].string)
print(namecity)
for i in range(7):
    tq = str(soup.find_all(class_='tem')[i])
    bds = r'\d+'
    wendu = re.findall(bds,tq)
    print(wendu)
    y_data_1.append(int(wendu[0]))
    try:
        y_data_2.append(int(wendu[1]))
    except IndexError as e:
        y_data_2.append(0)
    try:
        y_data_3.append((int(wendu[0])+int(wendu[1]))/2)
    except IndexError as e:
        y_data_3.append((int(wendu[0])+0)/2)
print(y_data_1)
print(y_data_2)
print(y_data_3)
x_data = ['今天', '明天', '后天', '大后天', '大大后天', '大大大后天', '大大大大后天']
chart = Line(namecity + "未来7天温度(摄氏度)")
chart.set_options(
    labels=x_data,
    x_label="日期",
    y_label="温度",
    legend_pos="upRight"
)
chart.add_series("最高", y_data_1)
chart.add_series("最低", y_data_2)
chart.add_series("平均",y_data_3)
#chart.render_notebook()
chart.render()

```
