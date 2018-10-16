# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class data_sb(scrapy.Item):
    # define the fields for your item here like:
    game_id = scrapy.Field()
    line_spread =scrapy.Field()
    line_total =scrapy.Field()
    odd_sa = scrapy.Field()
    odd_sh = scrapy.Field()
    odd_ta = scrapy.Field()
    odd_th = scrapy.Field()
    score_a = scrapy.Field()
    score_h = scrapy.Field()
    time_game = scrapy.Field()
    time_local = scrapy.Field()
    status = scrapy.Field()
    pass

class data_eb(scrapy.Item):
    # define the fields for your item here like:
    game_id = scrapy.Field()
    line_spread =scrapy.Field()
    line_total =scrapy.Field()
    odd_sa = scrapy.Field()
    odd_sh = scrapy.Field()
    odd_ta = scrapy.Field()
    odd_th = scrapy.Field()
    score_a = scrapy.Field()
    score_h = scrapy.Field()
    time_game = scrapy.Field()
    time_local = scrapy.Field()
    status = scrapy.Field()
    pass

class data_cr(scrapy.Item):
    # define the fields for your item here like:
    game_id = scrapy.Field()
    line_spread =scrapy.Field()
    line_total =scrapy.Field()
    odd_sa = scrapy.Field()
    odd_sh = scrapy.Field()
    odd_ta = scrapy.Field()
    odd_th = scrapy.Field()
    score_a = scrapy.Field()
    score_h = scrapy.Field()
    time_game = scrapy.Field()
    time_local = scrapy.Field()
    status = scrapy.Field()
    pass

class data_365(scrapy.Item):
    # define the fields for your item here like:
    game_id = scrapy.Field()
    line_spread =scrapy.Field()
    line_total =scrapy.Field()
    odd_sa = scrapy.Field()
    odd_sh = scrapy.Field()
    odd_ta = scrapy.Field()
    odd_th = scrapy.Field()
    score_a = scrapy.Field()
    score_h = scrapy.Field()
    time_game = scrapy.Field()
    time_local = scrapy.Field()
    status = scrapy.Field()
    pass

class data_vb(scrapy.Item):
    # define the fields for your item here like:
    game_id = scrapy.Field()
    line_spread =scrapy.Field()
    line_total =scrapy.Field()
    odd_sa = scrapy.Field()
    odd_sh = scrapy.Field()
    odd_ta = scrapy.Field()
    odd_th = scrapy.Field()
    score_a = scrapy.Field()
    score_h = scrapy.Field()
    time_game = scrapy.Field()
    time_local = scrapy.Field()
    status = scrapy.Field()
    pass
