from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from db import query

class Alerts(Resource):
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('routeId',type=int,required=True,help="routeId cannot be left blank!")
        parser.add_argument('smsStatus',type=int,required=True,help="smsStatus cannot be left blank!")
        parser.add_argument('alertDate',type=str,required=True,help="alertDate cannot be left blank!")
        parser.add_argument('alertTime',type=str,required=True,help="alertTime cannot be left blank!")
        parser.add_argument('alertCode',type=str,required=True,help="alertCode cannot be left blank!")
        data=parser.parse_args()
        try:
            imei=query(f"""SELECT IMEI FROM Bus WHERE routeId={data['routeId']}""",return_json=False)
            if len(imei)==0: return {"message":"Invalid routeId!"}
            query(f"""INSERT INTO Alerts(IMEI,smsStatus,alertDate,alertTime,alertCode)
	                             VALUES('{imei[0]['IMEI']}',{data['smsStatus']},'{data['alertDate']}',
                                 '{data['alertTime']}','{data['alertCode']}');""")
        except:
            return {"message": "An error occurred while updating."}, 500
        return {"message": "Alert created successfully."}, 201

    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('routeId',type=int)
        parser.add_argument('alertDate',type=str,required=True,help="Date cannot be left blank!")
        data=parser.parse_args()
        if data['routeId']==None:
            try:
                return query(f"""SELECT a.*,ac.description,b.routeId FROM Alerts a, AlertsControl ac, Bus b
                                                                     WHERE a.IMEI=b.IMEI AND a.alertCode=ac.alertCode
                                                                           AND a.alertDate='{data['alertDate']}'""")
            except:
                return {"message": "An error occurred while accessing Alerts table."},500
        else:
            try:
                return query(f"""SELECT a.*,ac.description,b.routeId FROM Alerts a, AlertsControl ac, Bus b
                                                                     WHERE a.IMEI=b.IMEI AND a.alertCode=ac.alertCode
                                                                           AND b.routeId={data['routeId']}
                                                                           AND a.alertDate='{data['alertDate']}'""")
            except:
                return {"message": "An error occurred while accessing Alerts table."},500
