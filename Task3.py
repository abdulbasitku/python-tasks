# TASK 3 - Abdul Basit
# REST based Web API expose for Mobile App to interact with database

from flask import Flask, jsonify, request
import sqlite3


def GetDatabaseConnection():
    return sqlite3.connect('etisalat.db')

app = Flask(__name__)

conn = GetDatabaseConnection()
crsr = conn.cursor()

crsr.execute("CREATE TABLE IF NOT EXISTS Controller (processname text, activationswitch text)") 

conn.commit()
conn.close() 


@app.route("/")
def Welcome():
    return '<h1>Welcome to Web API for Etisalat Mobile Application</h1>' \
           '</br><a href="/api/v1/insertprocess?pname=hello_world&sact=0">Insert Process</a></br>' \
           '<a href="/api/v1/updateprocessactivation?pname=hello_world&sact=1">Update Process Activation</a></br>' \
           '<a href="/api/v1/getallprocesses">Get All Processes</a></br>'



@app.route("/api/v1/insertprocess")
def InsertProcess():
    
    pname = request.args.get('pname')
    sact = request.args.get('sact')

    conn = GetDatabaseConnection()
    crsr = conn.cursor()
    
    crsr.execute("INSERT INTO Controller VALUES ('"+ pname + "','" + sact + "')")
    
    conn.commit()
    conn.close() 

    return jsonify(pname)

@app.route('/api/v1/updateprocessactivation', methods=['GET'])
def UpdateProcessActivation():
    pname = request.args.get('pname')
    sact = request.args.get('sact')

    conn = GetDatabaseConnection()
    crsr = conn.cursor()
    crsr.execute('UPDATE Controller SET activationswitch = ? WHERE processname = ?', (sact, pname))
        
    conn.commit()
    conn.close() 

    return jsonify(pname)

@app.route('/api/v1/getallprocesses', methods=['GET'])
def GetAllProcessesDetail():    
    
    conn = GetDatabaseConnection()
    crsr = conn.cursor()
    crsr.execute("SELECT * FROM Controller")
    data = crsr.fetchall()
    
    conn.close() 

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)  