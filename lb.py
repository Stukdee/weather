import re
import urllib.request
from bs4 import BeautifulSoup
from cutecharts.charts import Line
pd = str(input("输入城市代码:"))
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
