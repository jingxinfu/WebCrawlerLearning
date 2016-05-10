import requests, urllib.request, time, os
from bs4 import BeautifulSoup  # 导入需要用到的第三方库


def get_img_url(baseURL,fromPage, endPage):  # 获取所有图片的下载地址
    imgURL = []
    for p in range(fromPage,endPage + 1):
        time.sleep(5)  # 避免时间过快造成反爬
        url = baseURL + str(p)
        wb_data = requests.get(url, headers = headers)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        image = soup.select('img.entry_thumbnail')  # 选择的到所有包含图片的标签
        for i in image:
            imgURL.append(i.get('src'))
            print(i.get('src'))
    return imgURL


def sava_img(imgSRC, savePath):
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    print(imgSRC)
    urllib.request.urlretrieve(imgSRC, filename=savePath+ imgSRC.split('/')[-2] + imgSRC.split('/')[-1])


url = 'http://weheartit.com/inspirations/taylorswift?scrolling=true&page='  # 爬取地址

savePath = '/Users/fujingxin/Desktop/taylor/'  # 存储路径
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
    'Connection': "keep-alive"
}  # 伪装成人类
#proxies = {"http": "1.9.21.21:3128"}  # 防止反爬使用代理
imgAddress = get_img_url(url, fromPage=1, endPage=2)
print('--------------------------------')
for address in imgAddress:
    sava_img(address, savePath=savePath)
