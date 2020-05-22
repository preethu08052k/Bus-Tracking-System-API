from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from db import query

class Buses(Resource):
    @jwt_required
    def get(self):
        try:
            return query(f"""SELECT * FROM Bus ORDER BY routeId""")
        except:
            return {"message": "An error occurred while accessing Bus table."},500
