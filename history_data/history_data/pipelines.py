# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
class HistoryDataPipeline(object):
    def open_spider(self, spider):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='root', database='nba_player', port=3306)
        self.cur = self.conn.cursor()
        sql = r"TRUNCATE history_data"
        try:
            self.cur.execute(sql)
        except Exception as e:
            print(e)
            print("初始化失败")

    def process_item(self, item, spider):
        """初始化数据库"""
        """数据插入"""
        sql = r"""
        insert into history_data values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
        """.format(item[1],item[2],item['name'],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[11],item[12],item[13],item[14],item[15],item[16],item[17],item[18],item[19])
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
