# -*- coding: utf-8 -*-

import bs4
from bs4 import BeautifulSoup
import requests
import time

class CarInfo:
    """
    车辆信息：
        型号，链接，用户评分，图片，级别，续航里程，发动机，充电时间，官方指导价，折扣后价格，颜色列表
    """
    name = ''
    url = ''
    score = ''
    image = ''
    level = ''
    dist = ''
    motor = ''
    charge_time = ''
    official_price = ''
    discounted_price = ''
    colors = []


class BrandInfo:
    """
    品牌信息：
        名称，链接，车型列表
    """
    name = ''
    url = ''
    cars = []

def getUrlContent(url):
    """
    description: 获取指定url的内容\n
    param url: 链接地址\n
    return: 返回链接的页面内容，html文本。\n
        如果出错，返回None。
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

def getBrandList(content):
    """
    description: 从页面内容中获取品牌信息\n
    param content: 页面html内容\n
    return: 返回页面内容的品牌信息，BrandInfo类型。
    """
    if content != None:
        brands = []
        soup = BeautifulSoup(content, 'lxml')
        brandTree = soup.find('div', class_='cartree').find_all('li')
        for line in brandTree:
            brand = BrandInfo()
            brand.name = line.get_text().strip().split('(')[0]
            brand.url = r'https://car.autohome.com.cn' + line.find('a')['href']
            brands.append(brand)
        return brands
    else:
        return None
    pass

def getCars(brandContent):
    """
    description: 从页面内容中获取车辆信息\n
    param brandContent: 页面html内容\n
    return: 返回页面内容的车辆信息，CarInfo类型。
    """
    cars = []
    if brandContent != None:
        soup = BeautifulSoup(brandContent, 'lxml')
        carTree = soup.find_all('div', class_='tab-content fn-visible')[0]
        for line in carTree.find_all('div', class_='list-cont-bg'):
            car = CarInfo()
            car.name = line.find('div', class_='main-title').find('a').get_text().strip()
            car.url = r'https://car.autohome.com.cn' + line.find('div', class_='main-title').find('a')['href']
            car.score = line.find('div', class_='score-cont').get_text().split('：')[1].strip()
            car.image = r'https:' + line.find('div', class_='list-cont-img').find('img')['src']
            lis = line.find('ul', class_='lever-ul').find_all('li')
            car.level, car.dist, car.motor, car.charge_time = lis[0].find('span').get_text().strip(), lis[1].find('span').get_text().strip(), lis[2].find('span').get_text().strip(), lis[3].find('span').get_text().strip()
            for colorInfo in lis[4].find_all('a'):
                car.colors = car.colors + [colorInfo.find('div', class_='tip-content').get_text().strip()]
            car.official_price = line.find('div', class_='main-lever-right').find('span').get_text().strip()
            cars.append(car)
        return cars
    else:
        return None
    pass

def saveFile(brands):
    """
    description: 将数据写入markdown文件\n
    param brands: 爬取到的数据\n
    return: 无
    """
    with open('output.md', 'w', encoding='utf-8') as f:
        f.write('| 品牌 | 型号 | 图片 | 用户评分 | 级别 | 续航里程 | 发动机 | 充电时间 | 颜色 | 官方指导价 |\n')
        f.write('| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |\n')
        for brand in brands:
            for car in brand.cars:
                f.write('| <u>[' + brand.name + '](' + brand.url + ')</u> ')
                f.write('| <u>[' + car.name + '](' + car.url + ')</u> ')
                f.write('| ![](' + car.image + ') ')
                f.write('| ' + car.score + ' ')
                f.write('| ' + car.level + ' ')
                f.write('| ' + car.dist + ' ')
                f.write('| ' + car.motor + ' ')
                f.write('| ' + car.charge_time + ' ')
                f.write('| ')
                for color in car.colors:
                    f.write(color + ' ')
                f.write('| ' + car.official_price + ' ')
                f.write('|\n')
        pass
    

def log(msg):
    print('[LOG] ' + ', ' + time.strftime('%H:%M:%S',time.localtime(time.time())) + ': ' + str(msg))

if __name__ == "__main__":
    # 汽车之家电动车首页，爬虫入口网页
    url = 'https://car.autohome.com.cn/diandongche/index.html'
    # 获取首页的html内容
    content = getUrlContent(url)
    # 获取所有品牌的名称及链接列表
    brands = getBrandList(content)
    log('====== Total brand number :' + str(len(brands)) + ' ======')
    index = 1
    # 对每个品牌进行抓取
    for brand in brands:
        # 延迟防止被反爬虫
        time.sleep(0.56)
        log('++++++ Parsing ' + str(index) + '/' + str(len(brands)) + ': ' + brand.name + ' ++++++')    
        index = index + 1
        # 获取每个品牌页面中的车辆信息
        brand.cars = list(getCars(getUrlContent(brand.url)))
        log('++++++ ' + brand.name + ' contains ' + str(len(brand.cars)) + ' cars ++++++')    
    # 保存信息至文件
    saveFile(brands)

    pass