from flask import jsonify
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from db import query

class Sos(Resource):
    @jwt_required
    def get(self):
        try:
            return query(f"""SELECT * FROM Sos""")
        except:
            return {"message": "An error occurred while accessing Sos table."},500
