from databasetool import *

qd_name = search_team_name()
zd = {};
a=[];
for i in qd_name:
    j="".join(i)
    qy = search_name_from_team(j)
    zd.update({j:qy})


for i in zd:
    print(i)


from flask import Flask,render_template,request,url_for,json
from databasetool import *
app = Flask(__name__)


@app.route('/',methods=['post','get'])
def result():
    qd_name = search_team_name()
    value=request.get_json()
    print(value)
    return render_template("plays_compare.html",data1=qd_name,length1=len(qd_name))

if __name__ == '__main__':
    app.run(debug=True)

