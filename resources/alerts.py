from flask import jsonify
from flask_restful import Resource,reqparse
from db import cursor,encode

class Alerts(Resource):
    def get(self):
        cursor.execute(f'''SELECT * FROM AlertsControl''')
        result=encode(cursor.fetchall())
        return jsonify(result)
