#coding=utf-8
"""
重写这个IP地址可以访问我的数据库
封装好的工具类用来提取数据库里面的数据
获得数据的类
"""

import pymysql
IP="127.0.0.1"
Databasename="nba_player"
ACCOUNT='root'
PASSWD='root'
"""
获取所有球队的Url
"""
def init():
    conn=pymysql.connect(IP,ACCOUNT,PASSWD,Databasename)
    return conn
"获取所有爬取球队的url"
def get_team_url():
    conn =init()
    url_lists=dataget(conn,"select url from team")
    destory(conn)
    return url_lists

"""
rank_data
获取所有球员，
返回类型
"""

def rank_data():
    conn = init()
    url_lists = dataget(conn, "select id,name,team_name from player_order")
    print(url_lists)
    destory(conn)
    return url_lists

def dataget(conn,sql):
    cursor=conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    return results
def destory(conn):
    conn.close()

if __name__=="__main__":
    rank_data()

