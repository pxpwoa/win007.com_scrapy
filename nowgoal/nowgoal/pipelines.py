# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR,INT,TIME,DATE,FLOAT,TEXT,DATETIME,TIMESTAMP
from nowgoal.items import data_handicap,data_game,data_total,data_euro,data_url

class NowgoalPipeline(object):
    def __init__(self):
        self.game_dtype ={'datetime':DATETIME,'change_time':VARCHAR(20), 'company': VARCHAR(50), 'game_id':INT(), 'line':VARCHAR(20), 'odds_away':FLOAT(5,2), 'odds_home':FLOAT(5,2),
       'score':VARCHAR(20), 'odds_down':FLOAT(5,2), 'odds_over':FLOAT(5,2), 'score_away':VARCHAR(20), 'score_home':VARCHAR(20), 'team_away':VARCHAR(20),
       'team_away_f':VARCHAR(20), 'team_away_id':INT(), 'team_away_rank':VARCHAR(20), 'team_home':VARCHAR(20), 'team_home_f':VARCHAR(20), 'team_home_id':INT(),
       'team_home_rank':VARCHAR(20),'grr':FLOAT(5,2), 'kelly_away':FLOAT(5,2), 'kelly_home':FLOAT(5,2), 'kelly_tie':FLOAT(5,2), 'odds_away':FLOAT(5,2),
       'odds_home':FLOAT(5,2), 'odds_tie':FLOAT(5,2), 'probability_away':FLOAT(5,2), 'probability_home':FLOAT(5,2),'probability_tie':FLOAT(5,2),
       'team_home_en': VARCHAR(50),'team_away_en': VARCHAR(50),'league':VARCHAR(20),'league_f':VARCHAR(20),'league_en':VARCHAR(20),'league_id':INT(),}
    def process_item(self, item, spider):
        cnx = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/win007_min?charset=utf8', echo=False)
        if isinstance(item,data_game):
            try:
                data = pd.DataFrame(dict(item))
                data.to_sql(name = 'soccer_game_info',con = cnx, if_exists = 'append',index = False,dtype=self.game_dtype)
            except:
                print('比赛基础数据存入数据库错误!')
        elif isinstance(item,data_handicap):
            data = pd.DataFrame(dict(item))
            for g,group in data.groupby(['company']):
                # if g in ['澳门','易胜','Bet365','Crown','12Bet','明陞','利记']:
                    try:
                        group = group.drop('company', axis=1)
                        group.to_sql(name = '{company}_handicap_info'.format(company = self.chtoen(g)),con = cnx, if_exists = 'append',index = False,dtype=self.game_dtype)
                    except:
                        print('让球数据数据存入数据库错误!')
        elif isinstance(item,data_total):
            data = pd.DataFrame(dict(item))
            for g,group in data.groupby(['company']):
                # if g in['澳门','易胜','Bet365','Crown','12Bet','明陞','利记']:
                    try:
                        group = group.drop('company', axis=1)
                        group.to_sql(name = '{company}_total_info'.format(company = self.chtoen(g)),con = cnx, if_exists = 'append',index = False,dtype=self.game_dtype)
                    except:
                        print('大小球数据数据存入数据库错误!')
        elif isinstance(item,data_euro):
            data = pd.DataFrame(dict(item))
            for g,group in data.groupby(['company']):
                # if g in ['Interwetten', 'Easybets', 'Bet 365', 'Crown','Betfair','Macauslot','Sbobet','William Hill','Lottery Official']:
                    try:
                        group= group.drop('company',axis =1)
                        group.to_sql(name = '{company}_euro_info'.format(company = g.replace(' ','')),con = cnx, if_exists = 'append',index = False,dtype=self.game_dtype)
                    except:
                        print('欧赔球数据数据存入数据库错误!')
        elif isinstance(item,data_url):
            data = pd.DataFrame(dict(item))
            try:
                data.to_sql(name = 'soccer_url_fail',con = cnx, if_exists = 'append',index = False,dtype=self.game_dtype)
            except:
                print('url存入数据库错误!')
        return item

    def chtoen(self, x):
        return {'澳门': 'Macauslot', '金宝博': 'bet188', '利记': 'Sbobet', '立博': 'Ladbrokes', '韦德': 'Vcbet',
                    '易胜': 'Easybet', '明陞': 'M88', '盈禾': 'Wewbet', '10Bet': 'Bet10', '12Bet': 'Bet12'}.get(x, x)
