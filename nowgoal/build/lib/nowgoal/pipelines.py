# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pandas as pd
from sqlalchemy import create_engine
from nowgoal.items import data_sb,data_365,data_eb,data_cr,data_vb

class NowgoalPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,data_sb):
            data = pd.DataFrame(dict(item))
            cnx = create_engine('mysql+pymysql://root:blw3927493@127.0.0.1:3306/nba_reference',echo=False)
            data.to_sql(name = 'nowgoal_spread_sb_201708',con = cnx, if_exists = 'append',index = False)
        if isinstance(item,data_cr):
            data = pd.DataFrame(dict(item))
            cnx = create_engine('mysql+pymysql://root:blw3927493@127.0.0.1:3306/nba_reference',echo=False)
            data.to_sql(name = 'nowgoal_spread_cr_201708',con = cnx, if_exists = 'append',index = False)
        if isinstance(item,data_365):
            data = pd.DataFrame(dict(item))
            cnx = create_engine('mysql+pymysql://root:blw3927493@127.0.0.1:3306/nba_reference',echo=False)
            data.to_sql(name = 'nowgoal_spread_365_201708',con = cnx, if_exists = 'append',index = False)
        if isinstance(item,data_eb):
            data = pd.DataFrame(dict(item))
            cnx = create_engine('mysql+pymysql://root:blw3927493@127.0.0.1:3306/nba_reference',echo=False)
            data.to_sql(name = 'nowgoal_spread_eb_201708',con = cnx, if_exists = 'append',index = False)
        if isinstance(item,data_vb):
            data = pd.DataFrame(dict(item))
            cnx = create_engine('mysql+pymysql://root:blw3927493@127.0.0.1:3306/nba_reference',echo=False)
            data.to_sql(name = 'nowgoal_spread_vb_201708',con = cnx, if_exists = 'append',index = False)
        return item
