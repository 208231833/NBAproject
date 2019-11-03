# -*- coding: utf-8 -*-
import scrapy
import pymysql

class HistorySpider(scrapy.Spider):
    name = 'history'
    allowed_domains = ['nba.hupu.com']
    start_urls=[]
    conn=pymysql.connect(host='127.0.0.1', user='root', password='root', database='nba_player', port=3306)
    cur = conn.cursor()
    sql = r"select url from player"
    cur.execute(sql)
    urls=cur.fetchall()
    for url in urls:
        print(url[0])
        start_urls.append(url[0])

    def parse(self, response):
        """
        获取球员的常规赛和季后赛的所有数据
        """
        name=response.xpath('//p[@class="bread-crumbs"]/b/text()').extract()
        history_data=response.xpath('//div[@class="list_table_box J_p_l"]/table[@class="players_table bott bgs_table"]/tbody/tr/td/text()').extract()
        try:
            jihousai=history_data[18:].index("赛季")
        except:
            jihousai=len(history_data)
        history_data_normal = history_data[18:jihousai]
        if jihousai==len(history_data):
            history_data_jihousai=history_data[jihousai:]
        else:
            history_data_jihousai=history_data[jihousai+18:]
        for i in range(len(history_data_normal)//18):
             item={1:"1","name":name[0]}
             for index in range(2,20):
                item[index]=history_data_normal[i*18+index-2]
             print(item)
             yield item
        for i in range(len(history_data_jihousai) // 18):
            item2 = {1:"2","name": name[0]}
            for index in range(2, 20):
                item2[index]=history_data_jihousai[i*18++index-2]
            yield item2

