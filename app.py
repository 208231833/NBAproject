from flask import Flask,render_template,request,url_for,json
from databasetool import *
import databasetool
from flask import jsonify
from draw_tool import *
app = Flask(__name__)
draw_tool=draw_event()
rank_data = databasetool.rank_data()
team_data=databasetool.team_data()
play1=""
play2=""
@app.route('/')
def index():

    return render_template("index.html")


@app.route('/api_upload',methods=['POST'])
def api_upload():
    print("111112321312")
    data = request.get_data().decode()
    result=databasetool.search(data)
    print(result,"1111")
    return jsonify(result)
@app.route('/page1/')
def page1():

    return render_template("page1.html",data=rank_data)

@app.route('/page2/')
def page2():
    return render_template("page2.html",data=rank_data)

@app.route('/page3/')
def page3():
    return render_template("page3.html",data=rank_data)

@app.route('/page4/')
def page4():
    return render_template("page4.html",data=rank_data)

@app.route('/page5/')
def page5():
    return render_template("page5.html",data=rank_data)

@app.route('/page6/')
def page6():
    return render_template("page6.html",data=rank_data)

@app.route('/player/')
def player():
    player_basis_info=databasetool.player_basis_info(request.values.get('name'))
    player_current_game=databasetool.player_current_game(request.values.get('name'))
    len1=len(player_current_game)
    avg_data_normal_get=databasetool.avg_data_normal_get(request.values.get('name'))
    history_normal_data=databasetool.history_normal_data(request.values.get('name'))
    len3=len(history_normal_data)
    avg_data_normal_get=databasetool.avg_data_normal_get(request.values.get('name'))
    history_jihousai_data=databasetool.history_jihousai_data(request.values.get('name'))
    len5=len(history_jihousai_data)
    imgList1=list()
    for i in range(17):
        img = draw_tool.draw_plot_interface(request.values.get('name'), i, 3)
        if img:
           imgList1.append(img)

    imgList2=list()
    for i in range(18):
        img = draw_tool.draw_plot_interface(request.values.get('name'), i, 1)
        if img:
            imgList2.append(img)

    imgList3 = list()
    for i in range(18):
        img = draw_tool.draw_plot_interface(request.values.get('name'), i, 2)
        if img:
            imgList3.append(img)


    return render_template("player.html",
                           data=player_basis_info,
                           data1=player_current_game,
                           len1=len1,
                           data2=avg_data_normal_get,
                           data3=history_normal_data,
                           len3=len3,
                           data4=avg_data_normal_get,
                           data5=history_jihousai_data,
                           len5=len5,
                            list1=imgList1,
                           list2=imgList2,
                           list3=imgList3
                           )

@app.route('/team/')
def team():
    content=len(team_data)
    return render_template("teams.htm",data=team_data,lenth=content)

@app.route('/predict/')
def predict():
    content=databasetool.predict_game()
    lenth=len(content)
    return render_template("predict.html",data=content,lenth=lenth)

@app.route('/compare/',methods=['post', 'get'])
def compare():
    data = ""
    qd_name = getname()
    if request.method == 'POST':
        rev = request.get_data().decode()
        # 对收到的数据进行判断，调用相应函数
        # 通过球队获取球队成员
        if rev in qd_name:
            print(0000)
            data = qd_names_get(rev)
        elif "one" in rev:
            print(111)
            data = get_year(rev)
        elif "second" in rev:
            print(222)
            data = player_basis_infos(rev)
        elif "third" in rev:
            print(333)
            data+=get_img1(rev)
            data+=" "+get_img2(rev)
            data+=" "+get_img3(rev)
        print(data)
        return data
    else:
        return render_template("player_compare.html")


# 获得年份
def get_year(info):
    year = ""
    L = info.split(" ")
    y = year_get(L[1], L[2], L[3])
    for i in y:
        year += ("".join(i) + " ")
    return year

def get_img1(msg):
    s=msg.split(" ")
    result = draw_tool.draw_subplot_year_interface(int(s[1]), s[2], s[4])
    print(type(result))
    return result
def get_img2(msg):
    s1=msg.split(" ")
    print(s1)
    result = draw_tool.draw_subplot_many_interface(s1[2], s1[3], int(s1[1]), str(s1[4]))
    print(result)
    return result
# 获得球队的名字
def getname():
    qd = (search_team_name())
    qd_name = ""
    for i in qd:
        qd_name += ("".join(i) + " ")
    return qd_name
def get_img3(msg):
    s=msg.split(" ")
    result = draw_tool.draw_subplot_year_interface(int(s[1]), s[3], s[4])
    return result

def qd_names_get(name):
    qd_names = ""
    qy = (search_name_from_team(name))
    for i in qy:
        qd_names += ("".join(i) + " ")
    return qd_names


# 获得球员信息
def player_basis_infos(name):
    Name=name.split(" ")
    print(Name[1])
    msg = ""
    info = player_basis_info(Name[1])
    for i in info:
        for j in i:
            msg += ("".join(j) + " ")
    return msg

if __name__ == '__main__':
    app.run()
