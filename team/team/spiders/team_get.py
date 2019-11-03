# -*- coding: utf-8 -*-
import scrapy


class TeamGetSpider(scrapy.Spider):
    name = 'team_get'
    allowed_domains = ['nba.hupu.com']
    start_urls=["https://nba.hupu.com/stats/teams"]
    def parse(self, response):
        ids = []
        names = []
        urls = []
        for i in range(3, 33):
            id = response.xpath("//tbody/tr[{}]/td[1]/text()".format(i)).extract()
            name = response.xpath("//tbody/tr[{}]/td[2]/a/text()".format(i)).extract()
            url = response.xpath("//tbody/tr[{}]/td[2]/a/@href".format(i)).extract()
            team_name = response.xpath("//tbody/tr[{}]/td[3]/a/text()").extract()
            if id == []:
                break
            yield {"id": int(id[0]), "name": name[0], "url": url[0]}

