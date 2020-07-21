from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required,get_jwt_claims
from db import query

class Routes(Resource):
    @jwt_required
    def get(self):
        vendorid=get_jwt_claims()['vendorid']
        parser=reqparse.RequestParser()
        parser.add_argument('routeId',type=int)
        data=parser.parse_args()
        if data['routeId']==None:
            try:
                return query(f"""SELECT r.routeId,routeName,IMEI,vehicleNo FROM Routes r LEFT JOIN Bus b
                                 ON r.routeId=b.routeId WHERE b.vendorId={vendorid} ORDER BY r.routeId""")
            except:
                return {"message": "An error occurred while accessing Routes table."},500
        else:
            try:
                check=query(f"""SELECT * FROM Routes WHERE routeId={data['routeId']}""",return_json=False)
                if len(check)==0: return {"message":"Invalid routeId."}, 404
                return query(f"""SELECT r.routeId,routeName,IMEI,vehicleNo FROM Routes r LEFT JOIN Bus b
                                 ON r.routeId=b.routeId WHERE r.routeId={data['routeId']} AND b.vendorId={vendorid}""")
            except:
                return {"message": "An error occurred while accessing Routes table."},500
