import pymysql
from decimal import Decimal
from datetime import datetime
from flask import jsonify

def query(querystr,return_json=True):
    connection=pymysql.connect( host='182.18.164.20',
                                user='app',
                                password='Passw0rd2019',
                                db='gpstrackerdb',
                                cursorclass=pymysql.cursors.DictCursor )
    connection.begin()
    cursor=connection.cursor()
    cursor.execute(querystr)
    result=encode(cursor.fetchall())
    connection.commit()
    cursor.close()
    connection.close()
    if return_json: return jsonify(result)
    return result

def encode(data):
    for row in data:
        for key,value in row.items():
            if isinstance(value,Decimal):
                row[key]=str(value)
            if isinstance(value,datetime):
                row[key]=datetime.strftime(value,'%a, %d %b %Y %H:%M:%S IST')
    return data
