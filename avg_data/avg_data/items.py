# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class AvgDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    type = scrapy.Field()
    name = scrapy.Field()
    session = scrapy.Field()
    time = scrapy.Field()
    hit = scrapy.Field()
    hit_percentage = scrapy.Field()
    three = scrapy.Field()
    three_percentage = scrapy.Field()
    free = scrapy.Field()
    free_percentage = scrapy.Field()
    rebound = scrapy.Field()
    assist = scrapy.Field()
    steal = scrapy.Field()
    block = scrapy.Field()
    fault = scrapy.Field()
    foul = scrapy.Field()
    scores = scrapy.Field()
"""
球队的信息成绩
"""
# class Team_current(scrapy.Item):
#     rank=scrapy.Field()
#     name=scrapy.Field()
#

"""

得分排名
球员的当前数据
"""
class current_player_DataItem(scrapy.Item):
    '''
    排名，球员，球队，得分，命中-出手，命中率，命中-三分，三分命中率，命中——罚球，罚球命中率，场次，上场时间
    '''
    rank=scrapy.Field()
    name=scrapy.Field()
    team=scrapy.Field()
    scores=scrapy.Field()
    hit_attempts=scrapy.Field()
    hit_percentages=scrapy.Field()
    three_attempts=scrapy.Field()
    three_percentages=scrapy.Field()
    free_attempts=scrapy.Field()
    free_percentages=scrapy.Field()
    session=scrapy.Field()
    time=scrapy.Field()
"""
球员的基本信息
"""
class player_basic_info(scrapy.Item):
    """
    照片的url,姓名,身高,体重,生日,球队，球队，学校，选秀，国籍，薪水，合同
    """
    photo=scrapy.Field()
    name=scrapy.Field()
    poisition=scrapy.Field()
    height=scrapy.Field()
    weight=scrapy.Field()
    birthday=scrapy.Field()
    team=scrapy.Field()
    school=scrapy.Field()
    draft=scrapy.Field()
    country=scrapy.Field()
    salary=scrapy.Field()
    contract=scrapy.Field()
class player_curreent_game(scrapy.Item):
    #本赛季比赛
    """
    日期，对手，比分，时间，，投篮，命中率，三分，命中率，罚球，命中率，篮板，命中率，助攻，盖帽，失误，得分
    """
    name=scrapy.Field()
    date=scrapy.Field()
    enemy=scrapy.Field()
    result=scrapy.Field()
    time=scrapy.Field()
    hit=scrapy.Field()
    hit_percentage=scrapy.Field()
    three=scrapy.Field()
    three_percentage=scrapy.Field()
    free=scrapy.Field()
    free_percentage=scrapy.Field()
    rebound=scrapy.Field()
    assist=scrapy.Field()
    steal=scrapy.Field()
    block=scrapy.Field()
    fault=scrapy.Field()
    foul=scrapy.Field()
    scores=scrapy.Field()
class player_history_data(scrapy.Item):
    #生涯的所有数据
    type=scrapy.Field()
    name=scrapy.Field()
    year=scrapy.Field()
    team=scrapy.Field()
    session=scrapy.Field()
    first_publish=scrapy.Field()
    time=scrapy.Field()
    hit = scrapy.Field()
    hit_percentage = scrapy.Field()
    three = scrapy.Field()
    three_percentage = scrapy.Field()
    free = scrapy.Field()
    free_percentage = scrapy.Field()
    rebound = scrapy.Field()
    assist = scrapy.Field()
    steal = scrapy.Field()
    block = scrapy.Field()
    fault = scrapy.Field()
    foul = scrapy.Field()
    scores = scrapy.Field()



