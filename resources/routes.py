from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from db import query

class Routes(Resource):
    @jwt_required
    def get(self):
        try:
            return query(f"""SELECT * FROM Routes""")
        except:
            return {"message": "An error occurred while accessing Routes table."},500
