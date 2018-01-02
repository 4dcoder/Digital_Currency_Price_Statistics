import requests
import json
import matplotlib.pyplot as plt
import time
import pymysql

conn = pymysql.connect(host='localhost', user='root', passwd='', db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("USE DIGICCY")

def generate_kline_huobi(j):
    tot = 0
    mmnt = []
    closeaver5 = []
    now = 0
    for data in j:
        now += data['close']
        if tot <= 3 :
            tot += 1
            continue
        mmnt.append(time.ctime(data['id'])[:-5])
        closeaver5.append((now/5))
        tot += 1
        now -= j[tot-4]['close']
    plt.plot(mmnt, closeaver5, color="blue", linewidth=1.0, linestyle="-", label='huobi')

def savedatahb(j):
    for data in j:
        tt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['id']))
        if cur.execute('''SELECT id from hb WHERE id = %s''', tt):
            continue
        cur.execute('''
        INSERT INTO hb (id, open, close, low, high, amount, vol, count)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (tt, data['open'], data['close'], data['low'], data['high'], data['amount'], data['vol'], data['count']))
    cur.connection.commit()

def generate_kline_okcoin(j):
    mmnt = []
    closeaver5 = []
    tot = 0
    now = 0
    for i in j:
        now += float(i[4])
        if tot <= 3 :
            tot += 1
            continue
        mmnt.append(time.ctime(int(i[0] / 1000))[:-5])
        closeaver5.append((now/5))
        tot += 1
        now -= float(j[tot-4][4])
    plt.plot(mmnt, closeaver5, color="red", linewidth=1.0, linestyle="-", label='okcoin')

def savedataokcoin(j):
    for data in j:
        tt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(data[0]/1000)))
        if cur.execute('''SELECT id from okcoin WHERE id = %s''', tt):
            continue
        cur.execute('''
        INSERT INTO okcoin (id, open, close, low, high, amount)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''', (tt, data[1], data[4], data[3], data[2], data[5]))
    cur.connection.commit()

urlhb = '''https://api.huobi.pro/market/history/kline?period=1min&size=60&symbol=btcusdt'''
urlokcoin = '''https://www.okcoin.com/api/v1/kline.do?symbol=btc_usd&type=1min&size=60'''
headershb = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
}
wb_data_hb = requests.get(urlhb, headers=headershb)
wb_data_okcoin = requests.get(urlokcoin)

j1 = json.loads(wb_data_hb.text)
j = j1['data']
j = sorted(j, key=lambda x: x['id'])
generate_kline_huobi(j)
savedatahb(j)

j = json.loads(wb_data_okcoin.text)
j = sorted(j, key=lambda x: x[0])
generate_kline_okcoin(j)
savedataokcoin(j)

cur.close()
conn.close()

plt.xlabel('Time')
plt.title('BTC/USDT')
plt.legend(loc='upper left')
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
plt.show()