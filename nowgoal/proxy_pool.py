# *-* coding:utf-8 *-*
import requests
from bs4 import BeautifulSoup
import pickle
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,WebDriverException
import re
from datetime import datetime,timedelta
import json
import random

def veridation(ips):
    work = []
    with open('proxy_pool.pickle', 'rb') as f:
        old = pickle.load(f)
    count =0
    ips_h = [{'http': 'http://'+ip} for ip in ips]
    old = [{'http': ip} for ip in old]
    date = datetime.today() - timedelta(days=random.choice(range(500)))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'From': 'pxpwoa@163.com'  # This is another valid field
    }
    r = requests.get('http://vip.win007.com/history/multiOddsData.aspx?date=' + date.strftime('%Y-%m-%d'),headers=headers)
    re_game = re.compile(r'\$.*?\$')
    re_ft = re.compile(r'False,|True,')
    re_comma = re.compile(r',|;|\$')
    cells =[]
    for game in re_ft.split(re_game.findall(r.text)[0]):
        try:
            cells.append(re_comma.split(game)[1])
        except:
            continue
    for ip in ips_h+old:
        try:
            count += 1
            print(count)
            r=requests.get('http://vip.win007.com/AsianOdds_n.aspx?id=' + random.choice(cells), proxies=ip,timeout=1, allow_redirects=False,headers=headers)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text)
                table = soup.find('table',id = "oddsDetail")
                company = table.find('td').text
                print('success %s' % ip)
                work.append(ip['http'])
            else:
                print('fail %s' % ip)
        except:
            print('fail %s' % ip)
    with open('proxy_pool.pickle', 'wb') as f:
        pickle.dump(list(set(work)),f)
    print('更新！！！！！！！！！！！！！！！！！！！！！')
    print(len(work))



import redis   # 导入redis模块，通过python操作redis 也可以直接在redis主机的服务端操作缓存数据库
while True:
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    ips =r.hgetall('useful_proxy')
    print(len(ips))
    veridation(ips)


