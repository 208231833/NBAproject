# -*- coding: utf-8 -*-
"""

尝试在一个scrapy中爬起多个网站的数据
如果可以后面就全部整合
"""
import scrapy
from ..items import *

class AvgGetSpider(scrapy.Spider):
    name = 'avg_get'
    allowed_domains = ['nba.hupu.com']

    def start_requests(self):
        player_urls=[]
        for i in range(1,7):
            player_urls.append("https://nba.hupu.com/stats/players/pts/{}".format(i))
        for url in player_urls:
            yield scrapy.Request(url=url,callback=self.parse)
        yield  scrapy.Request(url="https://nba.hupu.com/stats/teams",callback=self.parse3)


    #爬取球员的排名信息
    def parse(self, response):
        """
        :param response:
        :return: None
        """
        for i in range(2,52):
            item=current_player_DataItem()
            if response.xpath("//tbody/tr[{}]/td[1]/text()".format(i)).extract():
                item['rank'] = response.xpath("//tbody/tr[{}]/td[1]/text()".format(i)).extract()[0]
                item['name'] = response.xpath("//tbody/tr[{}]/td[2]/a/text()".format(i)).extract()[0]
                url = response.xpath("//tbody/tr[{}]/td[2]/a/@href".format(i)).extract()[0]
                item['team'] = response.xpath("//tbody/tr[{}]/td[3]/a/text()".format(i)).extract()[0]
                item['scores']=response.xpath("//tbody/tr[{}]/td[4]/text()".format(i)).extract()[0]
                item['hit_percentages']=response.xpath("//tbody/tr[{}]/td[6]/text()".format(i)).extract()[0]
                item['three_attempts']=response.xpath("//tbody/tr[{}]/td[7]/text()".format(i)).extract()[0]
                item['three_percentages']=response.xpath("//tbody/tr[{}]/td[8]/text()".format(i)).extract()[0]
                item['free_attempts']=response.xpath("//tbody/tr[{}]/td[9]/text()".format(i)).extract()[0]
                item['free_percentages']=response.xpath("//tbody/tr[{}]/td[10]/text()".format(i)).extract()[0]
                item['session']=response.xpath("//tbody/tr[{}]/td[11]/text()".format(i)).extract()[0]
                item['time']=response.xpath("//tbody/tr[{}]/td[12]/text()".format(i)).extract()[0]
                item['hit_attempts'] = response.xpath("//tbody/tr[{}]/td[5]/text()".format(i)).extract()[0]
            else:
                break
            # yield item
            yield scrapy.Request(url=url,callback=self.parse2)

    def parse2(self,response):
        """
        #爬取球员具体信息,最近比赛，生涯平均数据，生涯具体数据，
        :return:
        """
        player=player_basic_info()

        player['name']=response.xpath('//p[@class="bread-crumbs"]/b/text()').extract()[0]
        player['photo']=response.xpath("//div[@class='img']/img/@src").extract()[0]
        player['poisition'] = response.xpath("//div[@class='font']/p[1]/text()").extract()[0].split("：")[1]
        player['height'] = response.xpath("//div[@class='font']/p[2]/text()").extract()[0].split("：")[1]
        player['weight'] = response.xpath("//div[@class='font']/p[3]/text()").extract()[0].split("：")[1]
        player['birthday'] = response.xpath("//div[@class='font']/p[4]/text()").extract()[0].split("：")[1]
        player['team'] = response.xpath("//div[@class='font']/p[5]/a/text()").extract()[0]
        temp = response.xpath("//div[@class='font']/p[6]/text()").extract()
        self.filternull(player,'school',temp)
        temp = response.xpath("//div[@class='font']/p[7]/text()").extract()
        self.filternull(player, 'draft', temp)
        temp = response.xpath("//div[@class='font']/p[8]/text()").extract()
        self.filternull(player, 'country', temp)
        temp = response.xpath("//div[@class='font']/p[9]/text()").extract()
        self.filternull(player, 'salary', temp)
        temp = response.xpath("//div[@class='font']/p[10]/text()").extract()
        self.filternull(player, 'contract', temp)

        name=response.xpath('//p[@class="bread-crumbs"]/b/text()').extract()[0]
        cureent_game=response.xpath("//div[@class='Js-show-table']/table[@class='players_table bott bgs_table']/tbody/tr[@class='color_font1 borders_btm']/td/text()").extract()
        indexs=self.find_all_index(cureent_game,"日期")
        results=self.filter_unuser(indexs,17,cureent_game)
        for i in range(len(results)):
            player_cureent = player_curreent_game()
            player_cureent['name'] = name
            player_cureent['date']=results[i][0]
            player_cureent['enemy']=results[i][1]
            player_cureent['result']=results[i][2]
            player_cureent['time']=results[i][3]
            player_cureent['hit']=results[i][4]
            player_cureent['hit_percentage']=results[i][5]
            player_cureent['three']=results[i][6]
            player_cureent['three_percentage']=results[i][7]
            player_cureent['free']=results[i][8]
            player_cureent['free_percentage']=results[i][9]
            player_cureent['rebound']=results[i][10]
            player_cureent['assist']=results[i][11]
            player_cureent['steal']=results[i][12]
            player_cureent['block']=results[i][13]
            player_cureent['fault']=results[i][14]
            player_cureent['foul']=results[i][15]
            player_cureent['scores']=results[i][16]
            # yield player_current


            """
            生涯数据具体
            """
        history_data = response.xpath('//div[@class="list_table_box J_p_l"]/table[@class="players_table bott bgs_table"]/tbody/tr/td/text()').extract()
        indexs=self.find_all_index(history_data,"赛季")
        results=self.filter_unuser(indexs,18,history_data)
        type=0
        j=0
        for i in range(len(results)):
            player_history = player_history_data()

            if j!=len(indexs) and i+type == indexs[j]//18:
                j=j+1
                type=type+1
            player_history['type'] = type
            player_history['name'] = name
            player_history['year'] = results[i][0]
            player_history['team'] = results[i][1]
            player_history['session'] = results[i][2]
            player_history['first_publish']=results[i][3]
            player_history['time'] = results[i][4]
            player_history['hit'] = results[i][5]
            player_history['hit_percentage'] = results[i][6]
            player_history['three'] = results[i][7]
            player_history['three_percentage'] = results[i][8]
            player_history['free'] = results[i][9]
            player_history['free_percentage'] = results[i][10]
            player_history['rebound'] = results[i][11]
            player_history['assist'] = results[i][12]
            player_history['steal'] = results[i][13]
            player_history['block'] = results[i][14]
            player_history['fault'] = results[i][15]
            player_history['foul'] = results[i][16]
            player_history['scores'] = results[i][17]
            # yield player_history

        """
        生涯平均数据的爬取
        """
        avg_date=response.xpath("//div[@class='list_table_box J_p_l']/table[@class='players_table bott']/tbody/tr/td/text()").extract()
        results=avg_date[16:31]
        avg_normal=AvgDataItem()
        avg_normal['type']=1
        avg_normal['name']=name
        avg_normal['session']=results[0]
        avg_normal['time'] = results[1]
        avg_normal['hit'] = results[2]
        avg_normal['hit_percentage'] = results[3]
        avg_normal['three'] = results[4]
        avg_normal['three_percentage'] = results[5]
        avg_normal['free'] = results[6]
        avg_normal['free_percentage'] = results[7]
        avg_normal['rebound'] = results[8]
        avg_normal['assist'] = results[9]
        avg_normal['steal'] = results[10]
        avg_normal['block'] = results[11]
        avg_normal['fault'] = results[12]
        avg_normal['foul'] = results[13]
        avg_normal['scores'] = results[14]
        #yield avg_normal
        if len(avg_date)>50:
            avg_jihousai=AvgDataItem()
            results = avg_date[47:]
            avg_jihousai['type'] = 2
            avg_jihousai['name'] = name
            avg_jihousai['session'] = results[0]
            avg_jihousai['time'] = results[1]
            avg_jihousai['hit'] = results[2]
            avg_jihousai['hit_percentage'] = results[3]
            avg_jihousai['three'] = results[4]
            avg_jihousai['three_percentage'] = results[5]
            avg_jihousai['free'] = results[6]
            avg_jihousai['free_percentage'] = results[7]
            avg_jihousai['rebound'] = results[8]
            avg_jihousai['assist'] = results[9]
            avg_jihousai['steal'] = results[10]
            avg_jihousai['block'] = results[11]
            avg_jihousai['fault'] = results[12]
            avg_jihousai['foul'] = results[13]
            avg_jihousai['scores'] = results[14]
            # yield avg_jihousai
    # def parse3(self,response):
    #     """球队信息爬取"""
    #     for i in range(3, 33):
    #         id = response.xpath("//tbody/tr[{}]/td[1]/text()".format(i)).extract()
    #         name = response.xpath("//tbody/tr[{}]/td[2]/a/text()".format(i)).extract()
    #         url = response.xpath("//tbody/tr[{}]/td[2]/a/@href".format(i)).extract()
    #         team_name = response.xpath("//tbody/tr[{}]/td[3]/a/text()").extract()
    #     pass
    def find_all_index(self,arr, item):
        return [i for i, a in enumerate(arr) if a == item]
    #去除爬到的但是无用的数据
    def filter_unuser(self,indexs,length,list):
        indexs = [i // length for i in indexs]
        num = -1
        results = []
        for i in range(len(list) // length):
            if num+1!=len(indexs) and i==indexs[num+1]:
                i=i+1
                num=num+1
                continue
            results.append(list[i*length:(i+1)*length])
        return results
    """
    有的球员有部分信息不存在。。
    """
    def filternull(self,item,filed,list):
        if len(list)>0:
            content=list[0].split("：")[1]
            item[filed] = content
        return item






