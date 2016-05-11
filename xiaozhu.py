# -*- coding: utf-8 -*-

import requests, time, pymongo
from bs4 import BeautifulSoup

def gender_info(soup):  # 获取性别信息
    gender = 'female' if soup.find_all('div','div.member_ico1') else 'male'
    return gender

def get_info(url):
    wb_data = requests.get(url)  # 向服务器请求页面
    wb_data.encoding ='utf-8'  # 标明编码为utf-8,以免出现解码错误
    soup = BeautifulSoup(wb_data.text,'lxml')  # 以lxml方式对页面进行解析
    title = soup.select('h4 em')[0].text
    address = soup.select('span.pr5')[0].text
    price = int(soup.select('div.day_l span')[0].text)
    img = soup.select('#curBigImage')[0].get('src')
    hostPic = soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > a > img')[0].get('src')
    hostName = soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a')[0].text
    hostGender = gender_info(soup)
    data = {
        'title' : title,
        'address': address,
        'price' : price,
        'img' :img,
        'hostPic' : hostPic,
        'hostName' : hostName,
        'hostGender' : hostGender
    }
    print('get_info Done')
    return data

def get_list_url(pageURL):  # 获取页面中所有详细房源的url
    listUrl = []
    wb_data = requests.get(pageURL)
    wb_data.encoding = 'utf-8'
    soup = BeautifulSoup(wb_data.text,'lxml')
    pageList = soup.select('div.result_btm_con.lodgeunitname')
    for i in pageList:
        listUrl.append(i.get('detailurl'))
    print('get_list_url Done')
    return listUrl

def get_info_by_page(startPage, endPage, baseURL,database):  # 获取整个页面的信息
    for i in range(startPage,endPage+1):
        url = baseURL.format(i)
        listUrl = get_list_url(url)
        for j in listUrl:
            time.sleep(4)
            dataInfo = get_info(j)  # 获取每个页面的信息
            database.insert_one(dataInfo)  # 将信息插入到指定的页面中
    print('input to database Done')



client = pymongo.MongoClient('localhost',27017)  # 连接mongodb
xiaozhu = client['xiaozhu']  # 创建一个名叫xiaozhu的库文件
home_info = xiaozhu['home_info'] # 创建一个home_info的页面
pageBaseUrl = 'http://bj.xiaozhu.com/search-duanzufang-p{}-0/'  # 构造共同url连接

get_info_by_page(1,3,pageBaseUrl,home_info)

for info in home_info.find({'price':{'$gte':500}}):
    print(info)
