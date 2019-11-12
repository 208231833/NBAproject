from flask import Flask, render_template, request, url_for, json
from databasetool import *
app = Flask(__name__)
play1=""
play2=""

@app.route('/', methods=['post', 'get'])
def qiudui():
    data=""
    qd_name =getname()
    if request.method == 'POST':
        rev = request.get_data().decode()
        #对收到的数据进行判断，调用相应函数
        print(rev)
        #通过球队获取球队成员
        if rev in qd_name:
            data=qd_names_get(rev)
        elif "赛" in rev:
            data=get_year(rev)
        else:
            data=player_basis_infos(rev)
        return data
    else:
        return render_template("plays_compare.html")
#获得年份
def get_year(info):
    year=""
    L = info.split(" ")
    if L[2] =="常规赛":
        y = year_get(L[0], L[1],1)
    else:
        y = year_get(L[0], L[1], 2)
    for i in y:
        year += ("".join(i) + " ")
    return year
#获得球队的名字
def getname():
    qd = (search_team_name())
    qd_name = ""
    for i in qd:
        qd_name += ("".join(i) + " ")
    return qd_name

def qd_names_get(name):
    qd_names=""
    qy = (search_name_from_team(name))
    for i in qy:
        qd_names += ("".join(i) + " ")
    return qd_names
#获得球员信息
def player_basis_infos(name):
    msg=""
    info=player_basis_info(name)
    for i in info:
        for j in i:
            msg+=("".join(j)+" ")
    return msg
if __name__ == '__main__':
    app.run(debug=True)
