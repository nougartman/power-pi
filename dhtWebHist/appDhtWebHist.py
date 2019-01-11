import io
import json
from flask import Flask, render_template, send_file, make_response, request
import sqlite3
import schedule
from datetime import date
from datetime import time
conn=sqlite3.connect('/home/pi/power-sqlite.db')
curs=conn.cursor()
app = Flask(__name__)
#enter billing period dates below to return data for selected period
dates = "2019-01-05 00:00:00", "2019-04-17 23:59:59"

def getLastData():
    sql = "SELECT datetime(measure_time, '+10 hours') as measure_time, sensor_count_1, sensor_count_2, ROUND(sensor_1_rate_cost, 2), ROUND(sensor_2_rate_cost, 2), ROUND(total_cost, 2) FROM measure_history ORDER BY measure_time DESC LIMIT 1"
    for row in curs.execute(sql):
        measure_time = str(row[0])
        sensor_count_1 = row[1]
        sensor_count_2 = row[2]
        sensor_1_rate_cost = row[3]
        sensor_2_rate_cost = row[4]
        total_cost = row[5]
        #conn.close()
    return measure_time, sensor_count_1, sensor_count_2, sensor_1_rate_cost, sensor_2_rate_cost, total_cost

def getHistData(numSamples):
        curs.execute("SELECT * FROM measure_history ORDER BY measure_time DESC LIMIT "+str(numSamples))
        data = curs.fetchall()
        measure_time = []
        sensor_count_1 = []
        sensor_count_2 = []
        sensor_1_rate_cost = []
        sensor_2_rate_cost = []
        for row in reversed(data):
            measure_time.append(row[1])
            sensor_count_1.append(row[2])
            sensor_count_2.append(row[3])
            sensor_1_rate_cost.append(row[6])
            sensor_2_rate_cost.append(row[7])
        return measure_time, sensor_count_1, sensor_count_2, sensor_1_rate_cost, sensor_2_rate_cost
        
def maxRowsTable():
    for row in curs.execute("select COUNT(sensor_count_1) from  measure_history"):
        maxNumberRows=row[0]
    return maxNumberRows
    
def costSamplesSensor11():
    sql = '''SELECT ROUND(SUM(sensor_1_rate_cost), 2) FROM measure_history WHERE datetime(measure_time, '+10 hours') BETWEEN ? AND ? ORDER by measure_time ASC LIMIT 1'''
    curs.execute(sql, dates)
    costSamplesSensor1 = curs.fetchone()
    return costSamplesSensor1

def costSamplesSensor22():
    sql = '''SELECT ROUND(SUM(sensor_2_rate_cost), 2) FROM measure_history WHERE datetime(measure_time, '+10 hours') BETWEEN ? AND ? ORDER by measure_time DESC LIMIT 1'''
    curs.execute(sql, dates)
    costSamplesSensor2 = curs.fetchone()
    return costSamplesSensor2
    
def costTotal3():
    sql = '''SELECT ROUND(SUM(total_cost), 2) FROM measure_history WHERE datetime(measure_time, '+10 hours') BETWEEN ? AND ? ORDER by measure_time DESC LIMIT 1'''
    curs.execute(sql, dates)
    costTotal3 = curs.fetchone()
    return costTotal3

global numSamples
numSamples = maxRowsTable()
if (numSamples > 97):
    numSamples = 96
 
# main route
@app.route("/")
def index():
    measure_time, sensor_count_1, sensor_count_2, sensor_1_rate_cost, sensor_2_rate_cost, total_cost = getLastData()
    costSamplesSensor1 = costSamplesSensor11()
    costSamplesSensor2 = costSamplesSensor22()
    costTotal = costTotal3()
    templateData = {
        'measure_time': measure_time,
        'sensor_count_1': sensor_count_1,
        'sensor_count_2': sensor_count_2,
        'sensor_1_rate_cost': sensor_1_rate_cost,
        'sensor_2_rate_cost': sensor_2_rate_cost,
        'numSamples': numSamples,
        'costSamplesSensor1' : costSamplesSensor1,
        'costSamplesSensor2' : costSamplesSensor2,
        'costTotal' : costTotal
    }
    return render_template('index.html', **templateData)
    
@app.route('/aircon.json')
def aircon():
    connection = sqlite3.connect("/home/pi/power-sqlite.db")
    cursor = connection.cursor()
    sql = '''SELECT (julianday(measure_time, '+10 hours')- 2440587.5)*86400000 AS measure_time, sensor_count_1 FROM measure_history WHERE measure_time BETWEEN ? and ?'''
    cursor.execute(sql, dates)
    results = cursor.fetchall()
    return json.dumps(results)

@app.route('/graph1')
def graph1():
    return render_template('index.html')

    
@app.route('/general power.json')
def power():
    connection = sqlite3.connect("/home/pi/power-sqlite.db")
    cursor = connection.cursor()
    sql = '''SELECT (julianday(measure_time, '+10 hours')- 2440587.5)*86400000 AS measure_time, sensor_count_2 FROM measure_history WHERE measure_time BETWEEN ? AND ?'''
    cursor.execute(sql, dates)
    results = cursor.fetchall()
    return json.dumps(results)
    
@app.route("/graph")
def graph():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False)


