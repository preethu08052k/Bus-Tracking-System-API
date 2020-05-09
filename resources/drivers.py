from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from db import query

class Drivers(Resource):
    @jwt_required
    def get(self):
        try:
            return query(f"""SELECT * FROM Driver""")
        except:
            return {"message": "An error occurred while accessing Driver table."},500
