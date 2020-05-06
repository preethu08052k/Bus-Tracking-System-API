from flask import jsonify
from flask_restful import Resource,reqparse
from db import cursor,encode

class Drivers(Resource):
    def get(self):
        cursor.execute(f'''SELECT * FROM Driver''')
        result=encode(cursor.fetchall())
        return jsonify(result)
