from flask import jsonify
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required,get_jwt_claims
from decimal import Decimal
from db import query

class BusGeoFence(Resource):
    @jwt_required
    def post(self):
        vendorid=get_jwt_claims()['vendorid']
        parser=reqparse.RequestParser()
        parser.add_argument('routeId',type=int,required=True,help="routeId cannot be left blank!")
        parser.add_argument('latitude',type=str,required=True,help="latitude cannot be left blank!")
        parser.add_argument('longitude',type=str,required=True,help="logitude cannot be left blank!")
        parser.add_argument('pointNum',type=int,required=True,help="pointNum cannot be left blank!")
        data=parser.parse_args()
        try:
            imei=query(f"""SELECT IMEI FROM Bus WHERE routeId={data['routeId']} AND vendorId={vendorid}""",return_json=False)
            if len(imei)==0: return {"message":"Invalid routeId!"}, 404
            query(f"""INSERT INTO BusGeofence VALUES ( {data['routeId']},{Decimal(data['latitude'])},
                                                    {Decimal(data['longitude'])},{data['pointNum']})""")
        except:
            return {"message" : "An error occurred while updating."}, 500
        return {"message": "BusGeofence created successfully."},201

    @jwt_required
    def delete(self):
        vendorid=get_jwt_claims()['vendorid']
        parser=reqparse.RequestParser()
        parser.add_argument('routeId',type=int,required=True,help="routeId cannot be left blank!")
        data=parser.parse_args()
        try:
            check=query(f"""SELECT bg.* FROM BusGeofence bg, Bus b
                            WHERE bg.routeId=b.routeId AND bg.routeId={data['routeId']}
                                  AND vendorId={vendorid}""",return_json=False)
            if len(check)==0: return {"message" : "BusGeofence for given routeId not found."}, 404
            query(f"""DELETE FROM BusGeofence WHERE routeId={data['routeId']}""")
        except:
            return {"message" : "An error occurred while deleting."}, 500
        return {"message" : "Deleted successfully."}, 200

    @jwt_required
    def get(self):
        vendorid=get_jwt_claims()['vendorid']
        parser=reqparse.RequestParser()
        parser.add_argument('routeId',type=int)
        data=parser.parse_args()
        if data['routeId']==None:
            try:
                routeids=query(f"""SELECT DISTINCT bg.routeId FROM BusGeofence bg, Bus b
                                   WHERE bg.routeId=b.routeId AND b.vendorId={vendorid}""",return_json=False)
                routeids=[x['routeId'] for x in routeids]
                result={}
                for i in routeids:
                    ll=query(f"""SELECT longitude,latitude FROM BusGeofence
                                 WHERE routeId={i} ORDER BY pointNum""",return_json=False)
                    result[i]=[(x['longitude'],x['latitude']) for x in ll]
                return jsonify(result)
            except:
                return {"message" : "An error occurred while accessing BusGeofence table."}, 500
        else:
            try:
                result=query(f"""SELECT longitude,latitude FROM BusGeofence bg, Bus b
                                 WHERE bg.routeId=b.routeId AND bg.routeId={data['routeId']} AND b.vendorId={vendorid}
                                 ORDER BY pointNum""",return_json=False)
                return jsonify([(x['longitude'],x['latitude']) for x in result])
            except:
                return {"message" : "An error occurred while accessing BusGeofence table."}, 500
