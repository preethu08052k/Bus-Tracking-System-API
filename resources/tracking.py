from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required,get_jwt_claims
from decimal import Decimal
from db import query

class Tracking(Resource):
    @jwt_required
    def get(self):
        vendorid=get_jwt_claims()['vendorid']
        parser=reqparse.RequestParser()
        parser.add_argument('routeId',type=int)
        parser.add_argument('deviceTime',type=str)
        data=parser.parse_args()
        if  data['routeId']==None and data['deviceTime']==None:
            try:
                return query(f"""SELECT l.*,r.*,d.driverId,d.driverName,d.phone as driverPhone
                                 FROM tracker_latest l, Bus b, Routes r, Driver d
						         WHERE l.IMEI=b.IMEI AND b.routeId=r.routeId AND
                                       b.vendorId={vendorid} AND b.driverId=d.driverId
                                 ORDER BY upd_datetime""")
            except:
                return {"message": "An error occurred while accessing tracker_latest table."},500
        elif data['routeId']!=None and data['deviceTime']==None:
            try:
                return query(f"""SELECT l.*,r.*,d.driverId,d.driverName,d.phone as driverPhone
                                 FROM tracker_latest l, Bus b, Routes r, Driver d
								 WHERE l.IMEI=b.IMEI AND b.routeId=r.routeId AND b.vendorId={vendorid}
                                       AND b.driverId=d.driverId AND r.routeId={data['routeId']}
                                 ORDER BY upd_datetime""")
            except:
                return {"message": "An error occurred while accessing tracker_latest table."},500
        elif data['routeId']!=None and data['deviceTime']!=None:
            try:
                return query(f"""SELECT l.*,r.*,d.driverId,d.driverName,d.phone as driverPhone
                                 FROM tracker l, Bus b, Routes r, Driver d
								 WHERE l.IMEI=b.IMEI AND b.routeId=r.routeId AND b.driverId=d.driverId
                                       AND b.vendorId={vendorid} AND r.routeId={data['routeId']} AND
                                       l.upd_datetime BETWEEN '{data['deviceTime']}' AND ADDDATE('{data['deviceTime']}',INTERVAL 1 DAY)
                                 ORDER BY upd_datetime""")
            except:
                return {"message": "An error occurred while accessing tracker table."},500
        return {"message": "Invalid Input."},400
