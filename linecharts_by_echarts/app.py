from flask import Flask, render_template, jsonify
import pymysql


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/5minutesaverage', methods=['GET','POST'])
def cal_5_minutes():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='mysql', charset='utf8')
    cur = conn.cursor()
    cur.execute("USE DIGICCY")
    cur.execute("SELECT id, close FROM hb")
    res = cur.fetchall()
    tot = 0
    mmnt = []
    closeaver5_hb = []
    now = 0
    for data in res:
        now += data[1]
        if tot <= 3:
            tot += 1
            continue
        mmnt.append(data[0])
        if tot > 3:
            closeaver5_hb.append((now / 5))
        tot += 1
        now -= res[tot - 4][1]
    cur.execute("SELECT id, close FROM okcoin")
    res = cur.fetchall()
    closeaver5_okcoin = []
    now = 0
    tot = 0
    for data in res:
        now += data[1]
        if tot <= 3:
            tot += 1
            continue
        if tot > 3:
            closeaver5_okcoin.append((now / 5))
        tot += 1
        now -= res[tot - 4][1]
    cur.close()
    conn.close()
    return jsonify(time=mmnt, aver_hb=closeaver5_hb, aver_okcoin=closeaver5_okcoin)


if __name__ == "__main__":
    app.run(debug=True)