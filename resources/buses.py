from flask import jsonify
from flask_restful import Resource,reqparse
from db import cursor,encode

class Buses(Resource):
    def get(self):
        cursor.execute(f'''SELECT * FROM Bus''')
        result=encode(cursor.fetchall())
        return jsonify(result)
