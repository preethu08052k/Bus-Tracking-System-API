from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required,get_jwt_claims
from db import query

class GeoFence(Resource):
    @jwt_required
    def post(self):
        vendorid=get_jwt_claims()['vendorid']
        parser=reqparse.RequestParser()
        parser.add_argument('IMEI',type=str,required=True,help="IMEI cannot be left blank!")
        parser.add_argument('gDate',type=str,required=True,help="Date cannot be left blank!")
        parser.add_argument('gTime',type=str,required=True,help="Time cannot be left blank!")
        parser.add_argument('status',type=int,required=True,help="status cannot be left blank!")
        data=parser.parse_args()
        try:
            imei=query(f"""SELECT IMEI FROM Bus WHERE IMEI={data['IMEI']} AND vendorId={vendorid}""",return_json=False)
            if len(imei)==0: return {"message":"Invalid IMEI!"}, 404
            query(f"""INSERT INTO Geofence(IMEI, gDate, gTime, status)
                                    VALUES('{data['IMEI']}','{data['gDate']}','{data['gTime']}',{data['status']})""")
        except:
            return {"message" : "An error occurred while updating."}, 500
        return {"message": "Geofence status updated successfully."},201

    @jwt_required
    def get(self):
        vendorid=get_jwt_claims()['vendorid']
        parser=reqparse.RequestParser()
        parser.add_argument('fromDate',type=str,required=True,help="Date cannot be left blank!")
        parser.add_argument('toDate',type=str,required=True,help="Date cannot be left blank!")
        parser.add_argument('routeId',type=int)
        parser.add_argument('status',type=int)
        data=parser.parse_args()
        if data['status']==None:
            if  data['routeId']==None:
                try:
                    return query(f"""SELECT g.*,b.routeId FROM Geofence g, Bus b
    								 WHERE g.IMEI=b.IMEI AND b.vendorId={vendorid} AND
                                           g.gDate BETWEEN '{data['fromDate']}' AND '{data['toDate']}'
                                     ORDER BY gTime""")
                except:
                    return {"message" : "An error occurred while accessing Geofence table."},500
            else:
                try:
                    return query(f"""SELECT g.*,b.routeId FROM Geofence g, Bus b
    								 WHERE g.IMEI=b.IMEI AND b.routeId={data['routeId']} AND b.vendorId={vendorid} AND
                                           g.gDate BETWEEN '{data['fromDate']}' AND '{data['toDate']}'
                                     ORDER BY gTime""")
                except:
                    return {"message" : "An error occurred while accessing Geofence table."},500
        else:
            if data['status'] not in (0,1): return {"message": "Invalid status."},500
            if  data['routeId']==None:
                try:
                    return query(f"""SELECT g.*,b.routeId FROM Geofence g, Bus b
    								 WHERE g.IMEI=b.IMEI AND g.status={data['status']} AND b.vendorId={vendorid} AND
                                           g.gDate BETWEEN '{data['fromDate']}' AND '{data['toDate']}'
                                     ORDER BY gTime""")
                except:
                    return {"message" : "An error occurred while accessing Geofence table."},500
            else:
                try:
                    return query(f"""SELECT g.*,b.routeId FROM Geofence g, Bus b
    								 WHERE g.IMEI=b.IMEI AND b.routeId={data['routeId']} AND
                                           g.status={data['status']} AND b.vendorId={vendorid} AND
                                           g.gDate BETWEEN '{data['fromDate']}' AND '{data['toDate']}'
                                     ORDER BY gTime""")
                except:
                    return {"message" : "An error occurred while accessing Geofence table."},500
