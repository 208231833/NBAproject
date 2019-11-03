# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
class PlayerBasicPipeline(object):
    def open_spider(self, spider):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='root', database='nba_player', port=3306)
        self.cur = self.conn.cursor()
        sql = r"TRUNCATE player_basis"
        try:
            self.cur.execute(sql)
        except Exception as e:
            print(e)
            print("初始化失败")

    def process_item(self, item, spider):
        """初始化数据库"""

        """数据插入"""
        index=["姓名","照片","位置","身高","体重","生日","球队","学校","选秀","国籍","本赛季薪金","合同"]
        for i in range(len(index)):
            if index[i] not in item:
                item[index[i]]=""

        sql = r"""
           insert into player_basis values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
           """.format(item["姓名"],item["照片"],item["位置"],item["身高"],item["体重"],item["生日"],item["球队"],item["学校"],item["选秀"],item["国籍"],item["本赛季薪金"],item["合同"])
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