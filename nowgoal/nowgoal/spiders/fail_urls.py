# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider,CrawlSpider,Rule
import re
from datetime import datetime,date,timedelta,time
from nowgoal.items import data_handicap,data_game,data_total,data_euro,data_url
from scrapy.loader import ItemLoader
import pickle
import time
import pymysql
import pandas as pd

class nowgoal_nba(CrawlSpider):
    name = 'fail_urls'


    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '123456',
        'db': 'win007_min',
        'charset': 'utf8',
    }

    connection = pymysql.connect(**config)

    sql1 = """   SELECT url
                FROM soccer_url_fail
    """


    fail_urls = pd.read_sql(sql1, con=connection)
    urls = fail_urls.drop_duplicates()['url'].tolist()
    start_urls = urls
    # allowed_domains = ['win007.com']
    def __init__(self):
        self.date = datetime.today()-timedelta(days=1)
        self.delta = timedelta(days=1)
    def parse(self,response):
        url = response.url
        if 'js' in url:
            gameid = url.split('/')[-1].split('.')[0]
            yield scrapy.Request(
                url, callback=self.parse_euro,
                meta={'gameid': gameid}, errback=self.err_callback)
        elif 'Over' in url:
            gameid = url.split('=')[1]
            yield scrapy.Request(
                url, callback=self.parse_total,
                meta={'gameid': gameid}, errback=self.err_callback)
        elif 'Asian' in url:
            gameid = url.split('=')[1]
            yield scrapy.Request(
                url, callback=self.parse_handicap,
                meta={'gameid': gameid}, errback=self.err_callback)


    def chtoen(self,x):
        return {'澳门':'Macauslot','金宝博':'bet188', '利记':'Sbobet', '立博':'Ladbrokes', '韦德':'Vcbet',
                '易胜':'Easybet', '明陞':'M88', '盈禾':'Wewbet','10Bet':'Bet10','12Bet':'Bet12'}.get(x,x)

    def parse_handicap(self,response):
        start_time  = time.time()
        l = ItemLoader(item = data_handicap(),response = response)
        gameid = response.meta['gameid']
        print('请求剩余数目：' + str(len(self.crawler.engine.slot.inprogress)))
        try:
            table_odds = response.xpath('//table[@id = "oddsDetail"]')[0]
            company = table_odds.xpath('.//tr')[0].xpath('.//td//text()').extract()[:-3]
        except:
            print('让球请求失败，重新请求!\n ')
            print('响应内容:' + response.url)
            print('状态:'+str(response.status))
            print('响应内容:' + response.text)
            l = ItemLoader(item=data_url(), response=response)
            l.add_value('game_id', gameid)
            l.add_value('url', response.url)
            return l.load_item()
            # yield scrapy.Request(url=response.url,callback = self.parse_handicap, dont_filter=True,meta = response.meta['gameid'])
        for tr in table_odds.xpath('.//tr')[1:]:
            tds= tr.xpath('.//td')
            tds[2].extract()
            for index,td in  enumerate(tds[:-2]):
                text = td.xpath('.//text()').extract()
                if  text != []:
                    try:
                        l.add_value('game_id', gameid)
                        l.add_value('company', company[index])
                        l.add_value('line', text[0])
                        l.add_value('odds_home', text[1])
                        l.add_value('odds_away', text[-1])
                        dt = tds[-1].xpath('.//text()').extract()
                        l.add_value('change_time', dt[0]+' '+dt[1])
                    except:
                        print('让球解析错误！！！！！！！！！！！！！！！！！')
                    try:
                        l.add_value('score', tds[-2].xpath('.//text()').extract()[0])
                    except:
                        l.add_value('score', 'pregame')
        print(time.time() - start_time)
        return l.load_item()


    def parse_total(self, response):
        l = ItemLoader(item=data_total(), response=response)
        gameid = response.meta['gameid']
        print('请求剩余数目：' + str(len(self.crawler.engine.slot.inprogress)))
        try:
            table_odds = response.xpath('//table[@id = "oddsDetail"]')[0]
            company = table_odds.xpath('.//tr')[0].xpath('.//td//text()').extract()[:-3]
        except:
            print('大小分请求失败，重新请求!\n ')
            print('响应内容:' + response.url)
            print('状态:'+str(response.status))
            print('响应内容:' + response.text)
            l = ItemLoader(item=data_url(), response=response)
            l.add_value('game_id', gameid)
            l.add_value('url', response.url)
            return l.load_item()
            # yield scrapy.Request(url=response.url,callback = self.parse_total, dont_filter=True,meta = response.meta['gameid'])

        for tr in table_odds.xpath('.//tr')[1:]:
            tds = tr.xpath('.//td')
            tds[2].extract()
            for index, td in enumerate(tds[:-2]):
                text = td.xpath('.//text()').extract()
                if text != []:
                    try:
                        l.add_value('game_id', gameid)
                        l.add_value('company', company[index])
                        l.add_value('line', text[0])
                        l.add_value('odds_over', text[1])
                        l.add_value('odds_down', text[-1])
                        dt = tds[-1].xpath('.//text()').extract()
                        l.add_value('change_time', dt[0]+' '+dt[1])
                    except:
                        print('大小球解析错误！！！！！！！！！！！！！！！！！')
                    try:
                        l.add_value('score', tds[-2].xpath('.//text()').extract()[0])
                    except:
                        l.add_value('score', 'pregame')
        return l.load_item()

    def parse_euro(self, response):
        if response.url =='http://1x2.nowscore.com/1575294.js':
            p=0
        start_time =time.time()
        gameid = response.meta['gameid']
        flag = True
        l = ItemLoader(item=data_euro(), response=response,meta = response.meta['gameid'])
        print('请求剩余数目：' + str(len(self.crawler.engine.slot.inprogress)))
        re_game = re.compile(r'(?<=game\=Array\().*?(?=\);)')
        re_id = re.compile(r'(?<=\")\d*(?=\^)')
        re_gameDetail = re.compile(r'(?<=gameDetail\=Array\().*?(?=\);)')
        re_game = re.compile(r'(?<=game\=Array\().*?(?=\);)')
        try:
            cells_g = re_game.findall(response.text)[0].split('",')
            cells_d = re_gameDetail.findall(response.text)[0].split('",')
        except:
            try:
                cells_g = re_game.findall(response.text)[0].split('",')
                cells_d = re_game.findall(response.text)[0].split('",')
            except:
                print('欧赔请求失败，重新请求!\n ')
                print('响应内容:' + response.url)
                print('状态:'+str(response.status))
                print('响应内容:' + response.text)
                flag = False
            #yield scrapy.Request(url=response.url,callback = self.parse_euro, dont_filter=True)

        if flag ==True:

            try:
                companys = {}
                for cell in cells_g:
                    cells = cell.split('|')
                    if cells[-1]=='1' or cells[-2] == '1':# cells[-1]==1 : 交易所，cells[-2] = 1: 主流公司
                        companys[cells[1]] = cells[2]
                companys_id = [key for key in companys]
                print('euro', time.time() - start_time)
                start_time = time.time()
                for cell in cells_d:
                    if re_id.findall(cell)[0] in companys_id:
                        company = companys[re_id.findall(cell)[0]]
                        for c in cell.split('^')[-1].split(';')[:-1]:
                            cells = c.split('|')
                            l.add_value('odds_home',cells[0])
                            l.add_value('odds_away', cells[2])
                            l.add_value('odds_tie', cells[1])
                            l.add_value('change_time', cells[3])
                            l.add_value('game_id', gameid)
                            l.add_value('company', company)
                            try:
                                l.add_value('kelly_home', cells[4])
                                l.add_value('kelly_away', cells[6])
                                l.add_value('kelly_tie', cells[5])
                            except:
                                continue
            except:
                if cell == '':
                    print('没有欧赔数据')
                else:
                    print('欧赔解析错误！\n ')
                    l = ItemLoader(item=data_url(), response=response)
                    l.add_value('game_id', gameid)
                    l.add_value('url', response.url)
                    return l.load_item()
        print('euro',time.time() - start_time)
        return l.load_item()

    def err_callback(self, failure):
        if 'multiOddsData' in failure.request.url:
            yield failure.request
        else:
            l = ItemLoader(item=data_url())
            l.add_value('url', failure.request.url)
            yield l.load_item()








