from flask import jsonify
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from db import cursor,encode

class Buses(Resource):
    @jwt_required
    def get(self):
        try: cursor.execute(f'''SELECT * FROM Bus''')
        except: return {"message": "An error occurred while accessing Bus table."},500
        result=encode(cursor.fetchall())
        return jsonify(result)
