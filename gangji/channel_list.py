# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
url = 'http://bj.ganji.com/wu/'
def get_channel_list_from(url):
    wb_data = requests.get(url)  # 获取页面html
    wb_data.encoding = 'utf-8'
    soup = BeautifulSoup(wb_data.text,'lxml')  # 对页面进行解析
    catalog = soup.select('dl.fenlei dt a')  # 找寻分类列表
    data = []
    for i in catalog:
            #print('http://bj.ganji.com'+i.get('href'))
            data.append('http://bj.ganji.com'+i.get('href'))
    return data


channel_list = get_channel_list_from(url)

