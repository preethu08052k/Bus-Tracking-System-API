import pymysql
from decimal import Decimal

connection=pymysql.connect(
                        host='gpstrackerdb.cgvswcwjh49d.ap-south-1.rds.amazonaws.com',
                        user='admin',
                        password='test1234',
                        db='gpstrackerdb',
                        cursorclass=pymysql.cursors.DictCursor
                    )

cursor=connection.cursor()

def encode(data):
    for row in data:
        for key,value in row.items():
            if isinstance(value,Decimal):
                row[key]=str(value)
    return data
