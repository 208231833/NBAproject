# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class PlayerInfoPipeline(object):
    def open_spider(self, spider):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='root', database='nba_player', port=3306)
        self.cur = self.conn.cursor()
        sql = r"TRUNCATE player"
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
            print("初始化失败")
    def process_item(self, item, spider):
        """初始化数据库"""

        """数据插入"""
        sql = r"""
        insert into player values ({},'{}','{}','{}')
        """.format(item['id'], item['name'], item['url'],item['team_name'])
        print(sql)
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
            print("插入失败")
        return item

    def close_spider(self, spider):
        self.conn.close()