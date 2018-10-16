# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
class data_game(scrapy.Item):
    team_home = scrapy.Field()
    team_away = scrapy.Field()
    team_home_rank = scrapy.Field()
    team_away_rank = scrapy.Field()
    team_home_en = scrapy.Field()
    team_away_en = scrapy.Field()
    team_home_f = scrapy.Field()
    team_away_f = scrapy.Field()
    game_id = scrapy.Field()
    team_home_id = scrapy.Field()
    team_away_id = scrapy.Field()
    score_home = scrapy.Field()
    score_away = scrapy.Field()
    datetime = scrapy.Field()
    league_id = scrapy.Field()
    league = scrapy.Field()
    league_f = scrapy.Field()
    league_en = scrapy.Field()

class data_handicap(scrapy.Item):
    game_id = scrapy.Field()
    company = scrapy.Field()
    score = scrapy.Field()
    line = scrapy.Field()
    odds_home = scrapy.Field()
    odds_away = scrapy.Field()
    change_time = scrapy.Field()
    pass

class data_total(scrapy.Item):
    game_id = scrapy.Field()
    company = scrapy.Field()
    line = scrapy.Field()
    score = scrapy.Field()
    odds_over = scrapy.Field()
    odds_down = scrapy.Field()
    change_time = scrapy.Field()
    pass

class data_euro(scrapy.Item):
    game_id = scrapy.Field()
    company = scrapy.Field()
    score = scrapy.Field()
    odds_home = scrapy.Field()
    odds_away = scrapy.Field()
    odds_tie = scrapy.Field()
    probability_home = scrapy.Field()
    probability_away = scrapy.Field()
    probability_tie = scrapy.Field()
    grr = scrapy.Field()
    kelly_home = scrapy.Field()
    kelly_away = scrapy.Field()
    kelly_tie = scrapy.Field()
    change_time = scrapy.Field()
    pass

class data_url(scrapy.Item):
    game_id = scrapy.Field()
    url = scrapy.Field()
    pass