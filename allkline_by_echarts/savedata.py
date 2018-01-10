import requests
import json
import time
import pymysql

conn = pymysql.connect(host='localhost', user='root', passwd='', db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("USE DIGICCY")

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

def deldatahb(endtime):
    endtime1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(endtime))
    cur.execute('''DELETE FROM hb WHERE id < %s''', endtime1)

def deldataokcoin(endtime):
    endtime1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(endtime))
    cur.execute('''DELETE FROM okcoin WHERE id < %s''', endtime1)

urlhb = '''https://api.huobi.pro/market/history/kline?period=1min&size=60&symbol=btcusdt'''
urlokcoin = '''https://www.okcoin.com/api/v1/kline.do?symbol=btc_usd&type=1min&size=60'''
headershb = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
}
while True:
    wb_data_hb = requests.get(urlhb, headers=headershb)
    wb_data_okcoin = requests.get(urlokcoin)
    j1 = json.loads(wb_data_hb.text)
    j = j1['data']
    j = sorted(j, key=lambda x: x['id'])
    savedatahb(j)
    j = json.loads(wb_data_okcoin.text)
    j = sorted(j, key=lambda x: x[0])
    savedataokcoin(j)
    deldatahb(time.time()-60)
    deldataokcoin(time.time()-60)
    time.sleep(60)

cur.close()
conn.close()
