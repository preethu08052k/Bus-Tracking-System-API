from flask import jsonify
from flask_restful import Resource,reqparse
from db import cursor,encode

class Users(Resource):
    def get(self):
        cursor.execute(f'''SELECT * FROM Users''')
        result=encode(cursor.fetchall())
        return jsonify(result)
