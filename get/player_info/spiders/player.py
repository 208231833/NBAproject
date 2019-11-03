# -*- coding: utf-8 -*-
import scrapy


class PlayerSpider(scrapy.Spider):
    name = 'player'
    allowed_domains = ['nba.hupu.com']
    start_urls=[]
    for i in range(1, 7):
        basic = "https://nba.hupu.com/stats/players/pts/{}".format(i)
        start_urls.append(basic)

    def parse(self, response):
        ids = []
        names = []
        urls = []
        for i in range(2, 52):
            id = response.xpath("//tbody/tr[{}]/td[1]/text()".format(i)).extract()
            name = response.xpath("//tbody/tr[{}]/td[2]/a/text()".format(i)).extract()
            url = response.xpath("//tbody/tr[{}]/td[2]/a/@href".format(i)).extract()
            team_name=response.xpath("//tbody/tr[{}]/td[3]/a/text()".format(i)).extract()
            if id == []:
                break
            yield {"id": int(id[0]), "name": name[0], "url": url[0],"team_name":team_name[0]}
