#coding=utf-8
"""
用来查询数据库的封装函数工具类
"""
import pymysql
IP="rm-bp114480lvkwg38x6xo.mysql.rds.aliyuncs.com"
Databasename="nba_player"
ACCOUNT='dev'
PASSWD='520520cjj+'

"""
获取所有球队的Url
"""

def init():
    """
    用来初始化数据库
    :return:
    """
    conn=pymysql.connect(IP,ACCOUNT,PASSWD,Databasename)
    return conn


def rank_data():
    """
    查询出按照得分排好名的数据
    """
    conn = init()
    url_lists = dataget(conn, "select * from rank_order")
    destory(conn)
    return url_lists

def player_basis_info(name):
    """
    传入名字返回某个球员的基本信息
    :param name:
    :return:
    """
    conn = init()
    url_lists = dataget(conn, "select * from player_basic_info where name='{}'".format(name))
    print(url_lists)
    destory(conn)
    return url_lists

def player_current_game(name):
    """
    传入姓名返回球员最近的比赛
    :param name:
    :return:
    """
    conn = init()
    url_lists = dataget(conn, 'select * from player_current_game where name= "{}" ORDER BY STR_TO_DATE(date,"%m/%d") DESC'.format(name))
    destory(conn)
    return url_lists
def avg_data_normal_get(name):
    """
    传入名字来获得某个球员的常规赛生涯平均数据
    :param name:
    :return:
    """
    conn = init()
    url_lists = dataget(conn,'select * from avgdata where name="{}" and type="1"'.format(name))
    print(url_lists)
    destory(conn)
    return url_lists
def avg_data_jihousai(name):
    """
        传入名字来获得某个球员的季后赛生涯平均数据
        :param name:
        :return:
        """
    conn = init()
    url_lists = dataget(conn, 'select * from avgdata where name="{}" and type="2"'.format(name))
    print(url_lists)
    destory(conn)
    return url_lists
def dataget(conn,sql):
    """
    执行查询并返回结果
    :param conn:
    :param sql:
    :return:
    """
    cursor=conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def history_normal_data(name):
    """
    传入名字返回这个球员所有赛季的常规赛表现
    :param name:
    :return:
    """
    conn = init()
    url_lists = dataget(conn, 'select * from player_history_data where name="{}" and type="1" order by convert(year,SIGNED) '.format(name))
    print(url_lists)
    destory(conn)
    return url_lists
def history_jihousai_data(name):
    """
    传入名字返回球员的所有季后赛表现
    :param name:
    :return:
    """
    conn = init()
    url_lists = dataget(conn,
                        'select * from player_history_data where name="{}" and type="2" order by convert(year,SIGNED) '.format(
                            name))
    print(url_lists)
    destory(conn)
    return url_lists
def team_data():
    """
    返回球员的排名信息
    :param name:
    :return:
    """

    conn = init()
    url_lists = dataget(conn,'select * from team_data ORDER BY CONVERT(rank,SIGNED) ')
    print(url_lists)
    destory(conn)
    return url_lists
def team_info(name):
    """
    传入球队名字的缩写返回球队的基本信息
    :param name:
    :return:
    """
    conn = init()
    sql_q='select detail from name_abbr_detail where name="{}"'.format(name)
    url_lists = dataget(conn, " SELECT * from team_info where name = ({}) ".format(sql_q))
    print(url_lists)
    destory(conn)
    return url_lists

def destory(conn):
    """
    用来关闭数据库
    :param conn:
    :return:
    """
    conn.close()
def search(shuru):
    """
    传入用户输入的信息发生联想功能
    模糊匹配
    :param shuru:
    :return:
    """
    conn = init()
    url_lists = dataget(conn, ' select name from current_player_data where name like "%{}%" '.format(shuru))
    print(url_lists)
    destory(conn)


def search_team_name():
    """
    查询所有球队的名字
    :return:
    """
    conn = init()
    url_lists = dataget(conn, "SELECT name from name_abbr_detail")
    destory(conn)
    return url_lists
def search_name_from_team(team_name):
    """
    通过球队名字返回球员名字
    :param name:
    :return:
    """
    conn = init()
    url_lists = dataget(conn, "select name from current_player_data where team = '{}'".format(team_name))
    print(url_lists)
    destory(conn)
    return url_lists

def year_get(name1,name2,type):
        """
        传入两个球员的名字返回两个球员共有的赛季,1是常规赛,2是季后赛
        :param name1:
        :param name2:
        :param type:
        :return:
        """
        # type 1 type 2
        # 1季后赛，2是常规赛
        conn = init()
        url_lists = dataget(conn,
                            'select distinct year from player_history_data where name = "{}" and type="{}" and year in(select year from player_history_data where name = "{}" and type="{}")'.format(name1,name2,type))
        print(url_lists)
        destory(conn)
        return url_lists
if __name__=="__main__":
    search_name_from_team("火箭")
