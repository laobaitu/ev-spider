# -*- coding: utf-8 -*-

import bs4
from bs4 import BeautifulSoup
import requests
import time

class CarInfo:
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
    name = ''
    url = ''
    cars = []

def getUrlContent(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

def getBrandList(content):
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
            car.level = lis[0].find('span').get_text().strip()
            car.dist = lis[1].find('span').get_text().strip()
            car.motor = lis[2].find('span').get_text().strip()
            car.charge_time = lis[3].find('span').get_text().strip()
            for colorInfo in lis[4].find_all('a'):
                car.colors = car.colors + [colorInfo.find('div', class_='tip-content').get_text().strip()]
            car.official_price = line.find('div', class_='main-lever-right').find('span').get_text().strip()
            cars.append(car)
        return cars
    else:
        return None
    pass

def saveFile(brands):
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
    url = 'https://car.autohome.com.cn/diandongche/index.html'
    content = getUrlContent(url)
    brands = getBrandList(content)
    log('====== Total brand number :' + str(len(brands)) + ' ======')
    index = 1
    for brand in brands:
        time.sleep(0.56)
        log('++++++ Parsing ' + str(index) + '/' + str(len(brands)) + ': ' + brand.name + ' ++++++')    
        index = index + 1
        brand.cars = list(getCars(getUrlContent(brand.url)))
        log('++++++ ' + brand.name + ' contains ' + str(len(brand.cars)) + ' cars ++++++')    

    saveFile(brands)

    pass