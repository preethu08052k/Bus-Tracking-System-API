from flask import jsonify
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from db import query

class Tracking(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('routeId',type=int)
    parser.add_argument('deviceTime',type=str)
    @jwt_required
    def get(self):
        data=self.parser.parse_args()
        if  data['routeId']==None and data['deviceTime']==None:
            try:
                return query(f"""SELECT * FROM Livedata""")
            except:
                return {"message": "An error occurred while accessing Livedata table."},500
        elif data['routeId'] is not None and data['deviceTime']==None:
            try:
                imei=query(f"""SELECT IMEI FROM Bus WHERE routeId={data['routeId']}""",return_json=False)
                if len(imei)==0: return {"message":"Invalid RouteID."},500
                return query(f"""SELECT * FROM Livedata WHERE IMEI='{imei[0]['IMEI']}'""")
            except:
                return {"message": "An error occurred while accessing Livedata table."},500
        elif data['routeId']==None and data['deviceTime'] is not None:
            try:
                return query(f"""SELECT * FROM Rawdata WHERE deviceTime='{data['deviceTime']}'""")
            except:
                return {"message": "An error occurred while accessing Rawdata table."},500
        elif data['routeId'] is not None and data['deviceTime'] is not None:
            try:
                imei=query(f"""SELECT IMEI FROM Bus WHERE routeId={data['routeId']}""",return_json=False)
                if len(imei)==0: return {"message":"Invalid RouteID."},500
                return query(f"""SELECT * FROM Rawdata WHERE IMEI='{imei[0]['IMEI']}' AND deviceTime='{data['deviceTime']}'""")
            except:
                return {"message": "An error occurred while accessing Rawdata table."},500
