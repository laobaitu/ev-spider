# -*- coding: utf-8 -*-

import bs4
from bs4 import BeautifulSoup
import requests
import string
import time
import codecs
import threading

class CarInfo:
    subBrand = ''
    name = ''

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
        brandList = []
        soup = BeautifulSoup(content, 'lxml')
        carTree = soup.find_all('div', class_='cartree')[0].find_all('li')
        for line in carTree:
            brandInfo = BrandInfo()
            brandInfo.name = line.get_text().strip().split('(')[0]
            brandInfo.url = r'https://car.autohome.com.cn' + line.find('a')['href']
            brandList.append(brandInfo)
        return brandList
    else:
        return None
    pass

def getCars(brandContent):
    if brandContent != None:
        pass
    else:
        return None
    pass

def log(msg):
    print('[LOG] ' + ', ' + time.strftime('%H:%M:%S',time.localtime(time.time())) + ' Thread: ' + threading.current_thread().name + ', ' + msg)

def UrlsThreads():
    threadPool = []

    for keyword in keywords:
        threadPool.append(threading.Thread(target=getUrlByKeyword, name='menu ' + keyword ,args=(keyword,)))

    for thread in threadPool:
        thread.start()

    while len(threadPool) > 0:
        for thread in threadPool:
            if thread.is_alive() == False:
                threadPool.remove(thread)
    return


if __name__ == "__main__":
    url = 'https://car.autohome.com.cn/diandongche/index.html'
    content = getUrlContent(url)
    bList = getBrandList(content)
    for b in bList:
        print(b.name, b.url)
    pass