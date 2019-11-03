# -*- coding: utf-8 -*-
import scrapy
import pymysql

class CurentGameSpider(scrapy.Spider):
    name = 'curent_game'
    allowed_domains = ['nba.hupu.com']
    start_urls = []
    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', database='nba_player', port=3306)
    cur = conn.cursor()
    sql = r"select url from player"
    cur.execute(sql)
    urls = cur.fetchall()
    for url in urls:
        print(url[0])
        start_urls.append(url[0])

    def parse(self, response):
        name = response.xpath('//p[@class="bread-crumbs"]/b/text()').extract()
        cureent_data = response.xpath("//div[@class='Js-show-table']/table[@class='players_table bott bgs_table']/tbody/tr[@class='color_font1 borders_btm']/td/text()").extract()
        yuefen=[]
        for i in range(len(cureent_data)):
            if cureent_data[i]=="日期":
                yuefen.append(i)
        yuefen.append(len(cureent_data))
        yuefen_data=[]
        j=0
        for i in range(len(cureent_data)//17):
            if i*17==yuefen[j]:
                j=j+1;
                pass
            else:
                yuefen_data.append(cureent_data[i*17:(i+1)*17])
        for item in yuefen_data:
            result={"name":name[0]}
            for index,data in enumerate(item):
                result[index]=data
            yield result

