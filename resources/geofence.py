from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from db import query

class GeoFence(Resource):
    @jwt_required
    def post(Resource):
        parser=reqparse.RequestParser()
        parser.add_argument('IMEI',type=str,required=True,help="IMEI cannot be left blank!")
        parser.add_argument('gDate',type=str,required=True,help="Date cannot be left blank!")
        parser.add_argument('gTime',type=str,required=True,help="Time cannot be left blank!")
        parser.add_argument('status',type=int,required=True,help="status cannot be left blank!")
        data=parser.parse_args()
        try:
            query(f"""INSERT INTO Geofence VALUES ( '{data['IMEI']}','{data['gDate']}','{data['gTime']}',{data['status']})""")
        except:
            return {"message": "An error occurred while updating."}, 500
        return data,201

    @jwt_required
    def get(Resource):
        parser=reqparse.RequestParser()
        parser.add_argument('gDate',type=str,required=True,help="Date cannot be left blank!")
        parser.add_argument('routeId',type=int)
        data=parser.parse_args()
        if  data['gDate'] is not None and data['routeId']==None:
            try:
                return query(f"""SELECT g.*,b.routeId FROM Geofence g, Bus b
												WHERE g.IMEI=b.IMEI AND g.gDate='{data['gDate']}'""")
            except:
                return {"message": "An error occurred while accessing Geofence table."},500
        elif data['gDate'] is not None and data['routeId'] is not None:
            try:
                return query(f"""SELECT g.*,b.routeId FROM Geofence g, Bus b
												WHERE g.IMEI=b.IMEI AND g.gDate='{data['gDate']}'
                                                      AND b.routeId={data['routeId']}""")
            except:
                return {"message": "An error occurred while accessing Livedata table."},500
