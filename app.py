from flask import Flask, render_template, request, url_for, json
from databasetool import *

app = Flask(__name__)


@app.route('/', methods=['post', 'get'])
def result():
    qd_name = search_team_name()
    return render_template("plays_compare.html", data1=qd_name, length1=len(qd_name),data2="",length2=0,data3="",length3=0)


@app.route('/page1', methods=['GET'])
def result1():
    value1 = request.values.get('qd_msg1')
    value2 = request.values.get('qd_msg2')
    qd_name = search_team_name()
    print(value1,value2)
    qy_name1 = search_name_from_team(value1)
    qy_name2 =search_name_from_team(value2)
    return render_template("plays_compare.html", data1=qd_name, length1=len(qd_name),data2=qy_name1,length2=len(qy_name1),data3=qy_name2,length3=len(qy_name2))


if __name__ == '__main__':
    app.run(debug=True)
