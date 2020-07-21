from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required,get_jwt_claims
from db import query

class Buses(Resource):
    @jwt_required
    def get(self):
        vendorid=get_jwt_claims()['vendorid']
        try:
            return query(f"""SELECT * FROM Bus WHERE vendorId={vendorid} ORDER BY routeId""")
        except:
            return {"message": "An error occurred while accessing Bus table."},500
