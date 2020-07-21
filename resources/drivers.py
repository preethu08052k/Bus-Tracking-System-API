from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required,get_jwt_claims
from db import query

class Drivers(Resource):
    @jwt_required
    def get(self):
        vendorid=get_jwt_claims()['vendorid']
        try:
            return query(f"""SELECT * FROM Driver d, Bus b
                             WHERE b.driverId=d.driverId AND b.vendorId={vendorid}""")
        except:
            return {"message": "An error occurred while accessing Driver table."},500
