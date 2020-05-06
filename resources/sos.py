from flask import jsonify
from flask_restful import Resource,reqparse
from db import cursor,encode

class Sos(Resource):
    def get(self):
        cursor.execute(f'''SELECT * FROM Sos''')
        result=encode(cursor.fetchall())
        return jsonify(result)
