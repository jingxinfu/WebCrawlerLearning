# -*- coding: utf=8 -*-
from bs4 import BeautifulSoup
import requests  # 导入必要的第三方库

def get_url_list(list_view):
    urls = []  # 创建存储需求商品url的list
    wb_data = requests.get(list_view)  # 获取整体页面的信息
    wb_data.encoding = 'utf=8'
    soup = BeautifulSoup(wb_data.text, 'lxml')  # 利用lxml 解析网页
    for link in soup.select('td.t > a[href^="http://bj.58.com/"]'):  # 利用正则表达式删选自己需要网页的url
        urls.append(link.get('href'))
    return urls


def get_views(url):
    id = url.split('/')[-1].split('x.')[0]
    api = 'http://jst1.58.com/counter?infoid=' + str(id)  # 查询借口,查询浏览数量
    header = {
        'Referer': url
    }
    js = requests.get(api, headers=header)
    views = js.text.split('=')[-1]
    return views

def get_info(url):  # 获取商品信息
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    title = soup.title.text
    price = soup.select('#content span.price')
    time = soup.select('li.time')
    views = get_views(url)
    areas = list(soup.select('span.c_25d')[0].stripped_strings) if soup.find_all('span','c_25d') else None  # stripped_strings 删除多余的空白符号

    data = {
        'title': title,
        'price': price[0].text,
        'time': time[0].text,
        'area': areas,
        'view': views
    }
    print(data)
Allurl = get_url_list('http://bj.58.com/pbdn/0/')
for i in Allurl:
    get_info(i)
