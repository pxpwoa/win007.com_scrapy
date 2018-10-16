import scrapy
from scrapy.spiders import Spider
import re
from datetime import datetime,date,timedelta,time
from nowgoal.items import data_sb,data_365,data_eb,data_cr,data_vb
from scrapy.loader import ItemLoader

class nowgoal_nba(Spider):
    
# scrapy crawl nba    
#   while flag_all:
    name = 'nba'
    start_urls = ['http://data.nowgoal.id/nba/oddsHistory.htm?Selday=2017-08-31']
    allowed_domains = ['nowgoal.id']
    def __init__(self):
        self.date = datetime(2017,8,31)
        self.delta = timedelta(days=1)
        self.timelist = ['Halftime','Quarter 1','Quarter 3']
    def parse(self,response):
                
        for gameid in response.xpath('//a[contains(@href,"javascript:BaskOdds")]//@href').re(r'\d+'):  
            yield scrapy.Request('http://data.nowgoal.id/OddsCompBasket.aspx?id='+gameid,callback = self.parse_link,meta = {'gameid':gameid})             
          
        yield scrapy.Request("http://data.nowgoal.id/nba/oddsHistory.htm?Selday="+date,callback = self.parse)
        if date == '2017-08-30':
            raise CloseSpider('data is enough!')
        else:
            date = (self.date - self.delta).strftime('%Y-%m-%d') 

            
    def parse_link(self,response):
       
        gameid = response.meta['gameid']
        tr = response.xpath('//table[@class= "oddstable"]//tr')
        if len(tr[1].xpath('.//td//text()')) > 5:
            yield scrapy.Request('http://data.nowgoal.id/NBA/2in1odds.htm?id='+gameid+'&cId=31',callback = self.parse_odds,meta = {'gameid':gameid})
        if len(tr[2].xpath('.//td//text()')) > 5:
            yield scrapy.Request('http://data.nowgoal.id/NBA/2in1odds.htm?id='+gameid+'&cId=2',callback = self.parse_odds,meta = {'gameid':gameid})
        if len(tr[3].xpath('.//td//text()')) > 5:
            yield scrapy.Request("http://data.nowgoal.id/NBA/2in1odds.htm?id="+gameid+"&cId=3",callback = self.parse_odds,meta = {'gameid':gameid})
        if len(tr[4].xpath('.//td//text()')) > 5:
            yield scrapy.Request("http://data.nowgoal.id/NBA/2in1odds.htm?id="+gameid+"&cId=8",callback = self.parse_odds,meta = {'gameid':gameid})
        if len(tr[5].xpath('.//td//text()')) > 5:
            yield scrapy.Request("http://data.nowgoal.id/NBA/2in1odds.htm?id="+gameid+"&cId=9",callback = self.parse_odds,meta = {'gameid':gameid})   
            
    def parse_odds(self,response):
        
        if 'cId=3' in response.url:
            l = ItemLoader(item = data_cr(), response = response)
        elif 'cId=31' in response.url:
            l = ItemLoader(item = data_sb(), response = response)
        elif 'cId=2' in response.url:
            l = ItemLoader(item = data_eb(), response = response)
        elif 'cId=8' in response.url:
            l = ItemLoader(item = data_365(), response = response)
        elif 'cId=9' in response.url:
            l = ItemLoader(item = data_vb(), response = response)
            
        table_spread = response.xpath('//table[@class = "tbs"]')[0]
        gameid = response.meta['gameid']
        id = response.xpath('//div[@class = "sTtitle"]/b/text()').extract()[0].replace('\xa0-\xa0',self.date.strftime('%Y%m%d')).replace(' ','')
        for tr in table_spread.xpath('.//tr')[2:]:
            tds = tr.xpath('.//td/text()').extract()
            if tds[-1] == 'Run':#run or live
                if ':' in tds[0]:
                    q = int(tds[0].split(' ')[1])*12
                    time_s = datetime.strptime(tds[0].split(' ')[-1],'%M:%S')
                    time_Q = datetime(1900, 1, 1, 0, q, 0)                        
                    time_delta = time_Q-time_s
                    time_game = (datetime.min + time_delta).time()
                    l.add_value('time_game',time_game)
                elif '加时' in tds[0]: # gametime
                    l.add_value('time_game',tds[0])
                elif 'Quarter 1' in tds[0]:
                    l.add_value('time_game',time(0,12))
                elif tds[0] in  ['Halftime ','Quarter 2 ']:
                    l.add_value('time_game',time(0,24))
                elif 'Quarter 3' in tds[0]:
                    l.add_value('time_game',time(0,36))
                else:
                    l.add_value('time_game','wrong')
                    
                if len(tds) == 6:# line close
                    l.add_value('game_id',gameid)
                    l.add_value('score_h',int(tds[1].split('-')[0]))
                    l.add_value('score_a',int(tds[1].split('-')[1]))
                    l.add_value('line_spread',float(tds[3]))
                    l.add_value('odd_sh',float(tds[2]))
                    l.add_value('odd_sa',float(tds[4]))
                    l.add_value('status',tds[-1])
                else:
                    l.add_value('game_id',gameid)
                    l.add_value('score_h',int(tds[1].split('-')[0]))
                    l.add_value('score_a',int(tds[1].split('-')[1]))
                    l.add_value('line_spread','close')
                    l.add_value('odd_sh','close')
                    l.add_value('odd_sa','close')
                    l.add_value('status',tds[-1])
            else:
                    l.add_value('game_id',gameid)
                    l.add_value('time_game',time(0,0))
                    l.add_value('score_h',0)
                    l.add_value('score_a',0)
                    l.add_value('line_spread',float(tds[2]))
                    l.add_value('odd_sh',float(tds[1]))
                    l.add_value('odd_sa',float(tds[3]))
                    l.add_value('status',tds[-1])

        yield l.load_item()
            
