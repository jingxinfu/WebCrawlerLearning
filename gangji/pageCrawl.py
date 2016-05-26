# -*- coding : utf-8 -*-
import requests, time, pymongo, random
from bs4 import BeautifulSoup

# http://cn-proxy.com/
proxy_list = [
    'http://117.177.250.151:8081',
    'http://122.70.183.138:8118'
]
proxy_ip = random.choice(proxy_list)  # 随机获取代理ip
proxies = {'http': proxy_ip}

# 伪装成人类
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
    'Connection': "keep-alive"
}

# 连接数据库
client = pymongo.MongoClient('localhost', 27017)
gangjiData = client['gangjiData']
# 建立页面 需要爬取的url,和商品详情页面
url_list = gangjiData['url_list']
items_info = gangjiData['items_info']


# 获取商品链接
def get_all_url_from(channel, page, who_sells='o'):
    count = 0
    for i in range(1, page + 1):
        url = '{}{}{}/'.format(channel, str(who_sells), str(i))
        wb_data = requests.get(url, headers=headers)
        time.sleep(2)
        wb_data.encoding = 'utf-8'
        soup = BeautifulSoup(wb_data.text, 'lxml')
        if soup.find('ul', 'pageLink clearfix'):
            links = soup.select('li.js-item a[href^="http://bj.ganji.com/"]')
            count += 1
            print(count)
            for l in links:
                url_list.insert_one({'link': l.get('href')})
                print(l.get('href'))
        else:
            break  # 没有找到,说明页面到达尾部


# 获取商品详情
def get_iterms_from(url):
    wb_data = requests.get(url)
    if wb_data.status_code == 404:
        pass
    else:
        time.sleep(2)
        wb_data.encoding = 'utf-8'
        soup = BeautifulSoup(wb_data.text, 'lxml')
        data = {
            'title': soup.select('h1.title-name')[0].text,
            'pubDate': soup.select('i.pr-5')[0].text.strip().split("\xa0")[0],
            'type': soup.select('ul.det-infor > li:nth-of-type(1) > span > a')[0].text,
            'price': soup.select('i.f22.fc-orange.f-type')[0].text,
            'area': list(map(lambda x: x.text.strip(), soup.select('ul.det-infor > li:nth-of-type(3) > a'))),
            'quality': list(soup.select('ul.second-det-infor.clearfix > li')[0].stripped_strings),
            'url': url  # 断点存储
        }
        print(data)
        items_info.insert_one(data)


get_all_url_from('http://bj.ganji.com/jiaju/', page=7)
