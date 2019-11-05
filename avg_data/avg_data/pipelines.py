# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
Host=''
user=''
password=''
database=''
port=''
class AvgDataPipeline(object):
    def open_spider(self, spider):
        self.conn = pymysql.connect(host=Host, user=user, password=password, database=database, port=3306)
        self.cur = self.conn.cursor()
        sql = r"TRUNCATE current_game"
        try:
            self.cur.execute(sql)
        except Exception as e:
            print(e)
            print("初始化失败")
    def process_item(self, item, spider):
        return item
