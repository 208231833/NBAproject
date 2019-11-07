#coding=utf-8
"""
封装一个画图类用来画需要的图
"""
IP="rm-bp114480lvkwg38x6xo.mysql.rds.aliyuncs.com"
Databasename="nba_player"
ACCOUNT='dev'
PASSWD='520520cjj+'
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
        plt.show()
        # sio = BytesIO()
        # plt.savefig(sio, format='png')
        # return sio
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
        # data = base64.encodebytes(sio.getvalue()).decode()
        # return data
if __name__=="__main__":
    draw_tool=draw_event()
    #首发场次为0时间为1 以此类推"场次","首发", "时间", "投篮命中数","投篮出手","投篮总命中率","三分命中","三分出手","三分命中率","罚球命中","罚球出手","罚球命中率","篮板","助攻","抢断","盖帽" ,"失误","犯规","得分"
    #"时间","投篮命中数","投篮出手","投篮总命中率","三分命中","三分出手","三分命中率","罚球命中","罚球出手","罚球命中率" ,"篮板" ,"助攻" ,"抢断" ,"盖帽" ,"失误" ,"犯规" ,"得分",类行3
    draw_tool.draw_plot_interface("詹姆斯-哈登",2,3)
#
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