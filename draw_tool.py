#coding=utf-8
"""
封装一个画图类用来画需要的图
"""
IP="rm-bp114480lvkwg38x6xo.mysql.rds.aliyuncs.com"
Databasename="nba_player"
ACCOUNT='dev'
PASSWD='520520cjj+'
import matplotlib
import numpy as np
import pymysql
from matplotlib import pyplot as plt
import pandas as pd
from io import BytesIO
import base64
class draw_event():
    def __init__(self):
        conn = pymysql.connect(IP, ACCOUNT, PASSWD, Databasename)
        self.player_history_data = pd.read_sql('select * from player_history_data', conn)
        self.player_current_game=pd.read_sql("SELECT * from  order_data",conn)
        self.historyitem = ["场次","首发", "时间", "投篮命中数","投篮出手","投篮总命中率","三分命中","三分出手","三分命中率","罚球命中","罚球出手","罚球命中率","篮板","助攻","抢断","盖帽" ,"失误","犯规","得分"]
        self.current_game_item=["时间","投篮命中数","投篮出手","投篮总命中率","三分命中","三分出手","三分命中率","罚球命中","罚球出手","罚球命中率" ,"篮板" ,"助攻" ,"抢断" ,"盖帽" ,"失误" ,"犯规" ,"得分"]
        self.player_current_game = self.deal(self.player_current_game, (5,8,11),("hit_percentage", "three_percentage", "free_percentage"))
        self.player_history_data=self.deal(self.player_history_data,(7,10,13),("hit_percentage","three_percentage","free_percentage"))
        self.temp_data=pd.read_sql('select * from player_history_data where team <>"汇总"', conn)
        self.player_normal = pd.read_sql("select * from avgdata where type='1'", conn)
        self.player_jihousai = pd.read_sql("select * from avgdata where type='2'", conn)
        self.player_normal=self.init_data(self.player_normal)
        self.player_jihousai=self.init_data(self.player_jihousai)
        self.label=['得分', '助攻', '篮板', '抢断', '盖帽', '投篮命中率', '三分命中率']
        self.Year=2
        self.First=4
        self.item1="赛季"
        self.item2="日期"
    def deal(self,df,num,rows):
        df=self.mutidf(df,num)
        df=self.mutidf2(df,rows)
        return df
    def mutidf(self,df, rows):

        for row in rows:
            df_ok_number = df.iloc[:, row].apply(lambda x: x.split('-')[1])
            df_number = df.iloc[:, row].apply(lambda x: x.split('-')[0])
            df.iloc[:, row] = df_ok_number
            temp = df.columns.tolist()
            temp.insert(row, "number{}".format(row))
            df = df.reindex(columns=temp)
            df.iloc[:, row] = df_number
        return df
    def mutidf2(self,df,rows):
        for row in rows:
            temp=df[row].map(lambda x:float(x.split("%")[0])/100)
            df[row]=temp
        return df
    def df_get(self,name):
        """
        用来传入名字后返回球员的常规赛数据的df
        :param name:
        :return:
        """
        self.player_who_history_data = self.player_history_data[self.player_history_data['name'] == name]

        self.player_normal_data =self.player_who_history_data[self.player_who_history_data["type"] == "1"]
        self.player_jihousai_data = self.player_who_history_data[self.player_who_history_data["type"] == "2"]

    def df_get2(self, name):
        self.player_current=self.player_current_game[self.player_current_game['name'] == name]
    def draw_plot1(self,df, x, y, title):
        plt.rcParams['font.family'] = ['SimHei']
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(title)
        plt.tick_params(top=False, right=False, left=False, bottom=False)
        plt.grid(alpha=0.2)
        plt.plot(df.iloc[:,0],df.iloc[:,1])
        sio = BytesIO()
        plt.savefig(sio)
        plt.close()
        return sio
    def draw_plot_interface(self,name,x,type):
        """
        给前端使用调用这个方法返回一个BufferIO
        name 球员名字，x就是数据表中的第i列 就是对应前端的数据顺序，type=1就代表是常规赛，type=2代表的是季后赛，投篮和三分的要分成两列,宽度，高度,type=3就是代表绘制最近比赛的折线图
        :param name:
        :return base64类型的东西 显示到网页的方法在下面有附加:
        """

        if type==1:
            self.df_get(name)
            self.First=5
            df = pd.DataFrame(list(zip( self.player_normal_data.iloc[:,self.Year].astype("float"),self.player_normal_data.iloc[:,x+self.First].astype("float"))))
            sio=self.draw_plot1(df,self.item1,self.historyitem[x],"常规赛中{}的{}的变化".format(name,self.historyitem[x]))
        elif type==2:
            self.df_get(name)
            self.First=5
            df = pd.DataFrame(list(zip(self.player_jihousai_data.iloc[:, self.Year].astype("float"),
                                       self.player_jihousai_data.iloc[:, x + self.First].astype("float"))))
            sio=self.draw_plot1(df, self.item1, self.historyitem[x], "季后赛中{}的{}的变化".format(name, self.historyitem[x]))
        elif type==3:
            self.df_get2(name)
            self.First=4

            df = self.player_current.iloc[:,[1,x + self.First]]
            df.iloc[:,1]=df.iloc[:, 1].apply(lambda x:float(x))
            print(df)
            sio = self.draw_plot1(df, self.item2, self.current_game_item[x], "{}最近的{}的变化".format(name, self.current_game_item[x]))
        data = base64.b64encode(sio.getvalue()).decode()
        return data
    def draw_subplot_avg(self,type,name):
        """
        #分析职业生涯的平均数据
        #1是分析出常规赛，2是季后赛
        返回的是一个单独的能力图
        :param type:
        :param name:
        :return:
        """
        if type==1:
            result=self.radar(self.label,self.player_normal,name,"常规赛","生涯")
        else:
            result = self.radar(self.label, self.player_jihousai, name, "季后赛","生涯")
        data = base64.encodebytes(result.getvalue()).decode()
        return data


    def radar(self, label, df, name, istype,live):

        matplotlib.rcParams['font.family'] = 'SimHei'  # 将绘图区域设置成中文字符
        radar_labels = np.array(label)  # 雷达标签
        nAttr = 7
        player = df[df[0] == name]
        print(player)
        eachdata = []
        if not player.empty:
            print(player)
        else:
            list2=[[name,0.0,0.0,0.0,0.0,0.0,0.0,0.0]]
            player=pd.DataFrame(list2,columns=[0,1,2,3,4,5,6,7])
            print(player)

        for i in range(1, player.shape[1]):
            eachdata.append(list(player[i]))
        eachdata.append(list(player[1]))
        print(eachdata)
        #     =[[scoreratio[1]],[assistratio[1]],[reboundratio[1]],[stealratio[1]],[blockratio[1]],[hit_percentageratio[1]],[three_percentageratio[1]],[scoreratio[1]]]
        angles = np.linspace(0, 2 * np.pi, nAttr, endpoint=False)
        angles = np.concatenate((angles, [angles[0]]))  # 将angles[0]以行的形式添加到angles的最下方，在末尾添加第一行是为了画出的图形能闭合
        plt.figure(facecolor="white")  # 设置画布的底色（除雷达突然以外的画布）
        ax = plt.subplot(111, polar=True)  # 将画框设置成圆形雷达图案
        ax.set_rgrids(np.arange(0, 1.2, 0.2), '-')  # 加了这一行后，一定要设置'-'，a就没了网格线上的数字了（0.2-1.0）
        plt.plot(angles, eachdata, 'o-', linewidth=1, alpha=0.3)  # 设置七芒星图案角上的点，alpha为控制透明度
        plt.fill(angles, eachdata, alpha=0.4)  # 填充七芒星图案
        plt.thetagrids(angles * 180 / np.pi, radar_labels)  # 设置雷达七角上标签
        plt.figtext(0.5, 1, name, ha='center', size=20)  # figtext加入文本框，前面两个数字代表位置
        plt.figtext(0.5, 0, '{}{}{}平均数据数据得出的能力图'.format(name,live,istype), ha='center', size=15, color='blue')
        plt.grid(True)
        sio = BytesIO()
        plt.savefig(sio)
        plt.close()
        return sio
    def init_data(self,df):
        name = df['name']
        rebound = df['rebound'].astype("float")
        assist = df['assist'].astype("float")
        steal = df['steal'].astype("float")
        block = df['block'].astype("float")
        scores = df['scores'].astype('float')
        hit_percentage = df['hit_percentage'].apply(lambda x: float(x.replace("%", "")) / 100)
        three_percentage = df['three_percentage'].apply(lambda x: float(x.replace("%", "")) / 100)
        scoremax = scores.max()
        assistmax = assist.max()
        reboundmax = rebound.max()
        stealmax = steal.max()
        blockmax = block.max()
        hit_percentagemax = hit_percentage.max()
        three_percentagemax = three_percentage.max()
        scoreratio = scores / scoremax
        assistratio = assist / assistmax
        reboundratio = rebound / reboundmax
        stealratio = steal / stealmax
        blockratio = block / blockmax
        hit_percentageratio = hit_percentage / hit_percentagemax
        three_percentageratio = three_percentage / three_percentagemax
        df = pd.DataFrame(list(
            zip(name, scoreratio, assistratio, reboundratio, stealratio, blockratio, hit_percentageratio,
                three_percentageratio)))
        return df

    def draw_subplot_year_interface(self, type, name,year):
        """
        #分析职业生涯的平均数据
        #1是分析出常规赛，2是季后赛
        #year是某一年
        返回的是一个单独的能力图
        :param type:
        :param name:
        :return:
        """
        if type==1:
            self.normal=self.temp_data[self.temp_data['type']=="1"]
            print(self.normal)
            self.normal_year=self.normal[self.normal['year']==year]
            df=self.init_data(self.normal_year)

            sio=self.radar(self.label, df,name, "常规赛",year)
        else:
            self.normal2 = self.temp_data[self.temp_data['type'] == "2"]
            self.normal_year2 = self.normal2[self.normal2['year'] == year]
            df = self.init_data(self.normal_year2)
            sio=self.radar(self.label, df, name, "季后赛", year)
        data = base64.b64encode(sio.getvalue()).decode()
        return data

    """多个雷达图放在一起的效果"""
    def draw_subplot_many_interface(self,name1,name2,type,year):
        """
        球员1，球员2，类型1是常规赛，2是季后赛year生效,3是常规赛平均，4是季后赛
        :param name1:
        :param name2:
        :param type:
        :param year:
        :return:
        """
        if type==1:
            self.normal = self.temp_data[self.temp_data['type'] == "1"]
            self.normal_year = self.normal[self.normal['year'] == year]
            df = self.init_data(self.normal_year)
            sio = self.radar_many(self.label, df, (name1,name2), "常规赛", year)
        elif type==2:
            self.normal2 = self.temp_data[self.temp_data['type'] == "2"]
            self.normal_year2 = self.normal2[self.normal2['year'] == year]
            df = self.init_data(self.normal_year2)
            sio = self.radar_many(self.label, df, (name1, name2), "季后赛", year)
        elif type==3:
            sio=self.radar_many(self.label,self.player_normal,(name1,name2),"常规赛","生涯")
        elif type==4:
            sio=self.radar_many(self.label,self.player_jihousai,(name1,name2),"季后赛","生涯")
        data = base64.b64encode(sio.getvalue()).decode()
        return data
    #多个球员的重合在一起的图
    def radar_many(self, label, df, name, istype, live):
        matplotlib.rcParams['font.family'] = 'SimHei'  # 将绘图区域设置成中文字符
        radar_labels = np.array(label)  # 雷达标签
        nAttr = 7
        result=[]
        for i in range(2):
            player = df[df[0] == name[i]]
            eachdata = []
            if not player.empty:
                print(player)
            else:
                list2 = [[name[i], 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
                player = pd.DataFrame(list2, columns=[0, 1, 2, 3, 4, 5, 6, 7])
                print(player)

            for i in range(1, player.shape[1]):
                eachdata.append(list(player[i]))
            eachdata.append(list(player[1]))
            print(eachdata)
            result.append(eachdata)
        #     =[[scoreratio[1]],[assistratio[1]],[reboundratio[1]],[stealratio[1]],[blockratio[1]],[hit_percentageratio[1]],[three_percentageratio[1]],[scoreratio[1]]]
        angles = np.linspace(0, 2 * np.pi, nAttr, endpoint=False)
        angles = np.concatenate((angles, [angles[0]]))  # 将angles[0]以行的形式添加到angles的最下方，在末尾添加第一行是为了画出的图形能闭合
        plt.figure(facecolor="white")  # 设置画布的底色（除雷达突然以外的画布）
        ax = plt.subplot(111, polar=True)  # 将画框设置成圆形雷达图案
        ax.set_rgrids(np.arange(0, 1.2, 0.2), '-')  # 加了这一行后，一定要设置'-'，a就没了网格线上的数字了（0.2-1.0）
        plt.plot(angles, result[0], 'o-', linewidth=1, alpha=0.3)  # 设置七芒星图案角上的点，alpha为控制透明度
        plt.fill(angles, result[0], alpha=0.4)  # 填充七芒星图案
        plt.plot(angles, result[1], 'o-', linewidth=1, alpha=0.3)  # 设置七芒星图案角上的点，alpha为控制透明度
        plt.fill(angles, result[1], alpha=0.4)  # 填充七芒星图案
        plt.thetagrids(angles * 180 / np.pi, radar_labels)  # 设置雷达七角上标签
        plt.figtext(0.5, 1, name, ha='center', size=20)  # figtext加入文本框，前面两个数字代表位置
        plt.figtext(0.5, 0, '{}{}{}{}能力对比的能力图'.format(name[0], name[0], istype,live), ha='center', size=15, color='blue')
        legend = plt.legend(name, loc=(0.94, 0.80), labelspacing=0.1)
        plt.grid(True)
        sio = BytesIO()
        plt.savefig(sio, format='png')
        plt.close()
        return sio

if __name__=="__main__":
    draw_tool=draw_event()
    #首发场次为0时间为1 以此类推"场次","首发", "时间", "投篮命中数","投篮出手","投篮总命中率","三分命中","三分出手","三分命中率","罚球命中","罚球出手","罚球命中率","篮板","助攻","抢断","盖帽" ,"失误","犯规","得分"
    #"时间","投篮命中数","投篮出手","投篮总命中率","三分命中","三分出手","三分命中率","罚球命中","罚球出手","罚球命中率" ,"篮板" ,"助攻" ,"抢断" ,"盖帽" ,"失误" ,"犯规" ,"得分",类行3
    # draw_tool.draw_plot_interface("詹姆斯-哈登",16,3)
    # result=draw_tool.draw_subplot_avg(1,"詹姆斯-哈登")
    # result = draw_tool.draw_subplot_avg(1, "勒布朗-詹姆斯")
    #年份要是字符类型
    # draw_tool.draw_subplot_year_interface(1,"詹姆斯-哈登","2018")
    #yearfloat类型
    # draw_tool.draw_subplot_many_interface("詹姆斯-哈登","勒布朗-詹姆斯",1,"2018")
    print(draw_tool.draw_subplot_many_interface("詹姆斯-哈登", "勒布朗-詹姆斯", 2, "2017"))
    """
   附上前端转换成iod
  # 转成图片的步骤//data调用方法返回
    data = base64.encodebytes(sio.getvalue()).decode()
    print(data)
    html = '''
       <html>
           <body>
               <img src="data:image/png;base64,{}" />
           </body>
        <html>
    '''
    plt.close()
    # 记得关闭，不然画出来的图是重复的
    return html.format(data)
    #format的作用是将data填入{}
"""