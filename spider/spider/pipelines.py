# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from .items import *
import pymysql
Host='rm-bp114480lvkwg38x6xo.mysql.rds.aliyuncs.com'
user='dev'
password='520520cjj+'
database='nba_player'
port='3306'
class SpiderPipeline(object):
    def open_spider(self, spider):
        self.conn = pymysql.connect(host=Host, user=user, password=password, database=database, port=3306)
        self.cur = self.conn.cursor()
        self.begin_init()
    def begin_init(self):
        sqllist=["avgdata","current_player_data","player_basic_info","player_current_game","player_history_data","team_data","team_info"]
        self.sqlinit(sqllist)
    def sqlinit(self,sqllist):
        for sql in sqllist:
            try:
                sql="truncate "+sql
                self.cur.execute(sql)
                self.conn.commit()
            except Exception as e:
                print(e)
                self.conn.rollback()
                print("初始化失败")
    def process_item(self, item, spider):
        if isinstance(item,current_player_DataItem):
            sql = r"""
                        insert into  current_player_data values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
                        """.format(item['rank'],item['name'],item['team'],item['scores'],item['hit_attempts'],item['hit_percentages'],item['three_attempts'],item['three_percentages'],item['free_attempts'],item['free_percentages'],item['session'],item['time'])
        elif isinstance(item,player_basic_info):
            sql = r"""
                                    insert into  player_basic_info values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
                                    """.format(item['photo'], item['name'], item['poisition'], item['height'],
                                               item['weight'], item['birthday'], item['team'],
                                               item['school'], item['draft'],
                                               item['country'], item['salary'], item['contract'])
        elif isinstance(item,player_curreent_game):
            sql=r"""
            insert into  player_current_game values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
                                    """.format(item['name'],item['date'],item['enemy'],item['result'],item['time'],item['hit'],item['hit_percentage'],item['three'],item['three_percentage'],item['free'],item['free_percentage'],item['rebound'],item['assist'],item['steal'],item['block'],item['fault'],item['foul'],item['scores'])
            print(sql)
        elif isinstance(item,player_history_data):
            sql=r"""
                insert into  player_history_data values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
            """.format(item['type'],item['name'],item['year'],item['team'],item['session'],item['first_publish'],item['time'],item['hit'],item['hit_percentage'],item['three'],item['three_percentage'],item['free'],item['free_percentage'],item['rebound'],item['assist'],item['steal'],item['block'],item['fault'],item['foul'],item['scores'])
        elif isinstance(item,AvgDataItem):
            sql=r"""
                insert into  AvgData values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
            """.format(item['type'],item['name'],item['session'],item['time'],item['hit'],item['hit_percentage'],item['three'],item['three_percentage'],item['free'],item['free_percentage'],item['rebound'],item['assist'],item['steal'],item['block'],item['fault'],item['foul'],item['scores'])
        elif isinstance(item,team_data):
            sql = r"""
                           insert into  team_data values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
                       """.format(item['rank'], item['team_name'], item['hit_percentage'], item['hit_number'], item['out_number'],
                                  item['three_percentage'], item['three_number'], item['three_out_number'], item['free_percentage'],item['free_out_number'],
                                  item['free_out_number'], item['All_rebound'], item['fight_rebound'], item['defind_rebound'],
                                  item['assist'], item['fault'], item['steal'],item['block'],item['foul'], item['scores'])
        elif isinstance(item,team_info):
            sql=r"""
                insert into  team_info values ('{}','{}','{}','{}','{}','{}','{}')
            """.format(item['url'],item['name'],item['enter_time'],item['home'],item['web'],item['coach'],item['describes'])

        self.sqlinsert(sql)
        return item

    def close_spider(self, spider):
        self.conn.close()
    def sqlinsert(self,sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
            print("插入失败")