from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from db import query

class GeoFence(Resource):
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('IMEI',type=str,required=True,help="IMEI cannot be left blank!")
        parser.add_argument('gDate',type=str,required=True,help="Date cannot be left blank!")
        parser.add_argument('gTime',type=str,required=True,help="Time cannot be left blank!")
        parser.add_argument('status',type=int,required=True,help="status cannot be left blank!")
        data=parser.parse_args()
        try:
            query(f"""INSERT INTO Geofence(IMEI, gDate, gTime, status)
                                    VALUES('{data['IMEI']}','{data['gDate']}','{data['gTime']}',{data['status']})""")
        except:
            return {"message" : "An error occurred while updating."}, 500
        return {"message": "Geofence status updated successfully."},201

    @jwt_required
    def get(self):
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
    												WHERE g.IMEI=b.IMEI AND
                                                          g.gDate BETWEEN '{data['fromDate']}' AND '{data['toDate']}'""")
                except:
                    return {"message" : "An error occurred while accessing Geofence table."},500
            else:
                try:
                    return query(f"""SELECT g.*,b.routeId FROM Geofence g, Bus b
    												WHERE g.IMEI=b.IMEI AND b.routeId={data['routeId']} AND
                                                          g.gDate BETWEEN '{data['fromDate']}' AND '{data['toDate']}'""")
                except:
                    return {"message" : "An error occurred while accessing Geofence table."},500
        else:
            if data['status'] not in (0,1): return {"message": "Invalid status."},500
            if  data['routeId']==None:
                try:
                    return query(f"""SELECT g.*,b.routeId FROM Geofence g, Bus b
    												WHERE g.IMEI=b.IMEI AND g.status={data['status']} AND
                                                          g.gDate BETWEEN '{data['fromDate']}' AND '{data['toDate']}'""")
                except:
                    return {"message" : "An error occurred while accessing Geofence table."},500
            else:
                try:
                    return query(f"""SELECT g.*,b.routeId FROM Geofence g, Bus b
    												WHERE g.IMEI=b.IMEI AND b.routeId={data['routeId']} AND g.status={data['status']}
                                                          AND g.gDate BETWEEN '{data['fromDate']}' AND '{data['toDate']}'""")
                except:
                    return {"message" : "An error occurred while accessing Geofence table."},500
