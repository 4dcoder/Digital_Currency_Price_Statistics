from flask import Flask, request, render_template, jsonify
import pymysql


app = Flask(__name__)

def connect_mysql():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='mysql', charset='utf8')
    cur = conn.cursor()
    cur.execute("USE DIGICCY")

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/5minutesaverage', methods=['GET'])
def cal_5_minutes():
    

if __name__ == "__main__":
    app.run(debug=True)