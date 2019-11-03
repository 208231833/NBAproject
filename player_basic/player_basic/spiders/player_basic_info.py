# -*- coding: utf-8 -*-
import scrapy
import requests
from PIL import Image
from io import BytesIO
import pymysql

class PlayerBasicInfoSpider(scrapy.Spider):
    name = 'player_basic_info'
    allowed_domains = ['https://nba.hupu.com']
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
        info=[]
        name=response.xpath('//p[@class="bread-crumbs"]/b/text()').extract()[0]
        photo=response.xpath("//div[@class='img']/img/@src").extract()[0]
        poisition=response.xpath("//div[@class='font']/p[1]/text()").extract()[0]
        height=response.xpath("//div[@class='font']/p[2]/text()").extract()[0]
        weight=response.xpath("//div[@class='font']/p[3]/text()").extract()[0]
        birthday=response.xpath("//div[@class='font']/p[4]/text()").extract()[0]
        team=response.xpath("//div[@class='font']/p[5]/a/text()").extract()[0]
        info.extend(["照片：{}".format(photo),"姓名：{}".format(name),poisition,height,weight,birthday,"球队：{}".format(team)])
        for i in range(6,11):
            temp=response.xpath("//div[@class='font']/p[{}]/text()".format(i)).extract()
            if len(temp)>0:
                info.append(temp[0])
        item={}
        for i in info:
            index,key=i.split("：")
            item[index]=key
        yield item

