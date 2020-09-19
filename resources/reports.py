from flask import jsonify
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required,get_jwt_claims
from db import query

class Fleet(Resource):
    @jwt_required
    def get(self):
        vendorid=get_jwt_claims()['vendorid']
        parser=reqparse.RequestParser()
        parser.add_argument('routeId',type=int)
        parser.add_argument('fromDate',type=str)
        parser.add_argument('toDate',type=str)
        data=parser.parse_args()
        if (data['fromDate']==None and data['toDate']!=None) or (data['fromDate']!=None and data['toDate']==None):
            return {"message":"Invalid Date input!"}, 400
        if (data['fromDate']!=None and data['toDate']!=None):
            if data['routeId']==None:
                try:
                    routes=query(f"""SELECT routeId,IMEI FROM Bus WHERE vendorId={vendorid}""",return_json=False)
                    routes=[(x['routeId'],x['IMEI']) for x in routes]
                    result={}
                    for routeid,imei in routes:
                        fleet=query(f"""SELECT l.IMEI,speed,battery_voltage,ignition_status,latitude,longitude,ac,
                                               mains_voltage,mains_power,alert_id,sos_alert,upd_datetime
                                        FROM tracker l, Bus b
                                        WHERE l.IMEI='{imei}' AND  l.IMEI=b.IMEI AND b.vendorId={vendorid} AND
                                              upd_datetime BETWEEN '{data['fromDate']}' AND ADDDATE('{data['toDate']}', INTERVAL 1 DAY)
                                        ORDER BY upd_datetime""",return_json=False)
                        result[routeid]=fleet
                    return jsonify(result)
                except:
                    return {"message": "An error occurred collecting report data."}, 500
            else:
                try:
                    imei=query(f"""SELECT IMEI FROM Bus WHERE routeId={data['routeId']} AND vendorId={vendorid}""",return_json=False)
                    if len(imei)==0: return {"message": "Invalid routeId."}, 404
                    fleet=query(f"""SELECT l.IMEI,speed,battery_voltage,ignition_status,latitude,longitude,upd_datetime
                                    FROM tracker l, Bus b
                                    WHERE l.IMEI='{imei[0]['IMEI']}' AND  l.IMEI=b.IMEI AND b.vendorId={vendorid} AND
                                          upd_datetime BETWEEN '{data['fromDate']}' AND ADDDATE('{data['toDate']}', INTERVAL 1 DAY)
                                    ORDER BY upd_datetime""",return_json=False)
                    return jsonify(fleet)
                except:
                    return {"message": "An error occurred collecting report data."}, 500
        else:
            if data['routeId']==None:
                try:
                    routes=query(f"""SELECT routeId,IMEI FROM Bus WHERE vendorId={vendorid}""",return_json=False)
                    routes=[(x['routeId'],x['IMEI']) for x in routes]
                    result={}
                    for routeid,imei in routes:
                        fleet=query(f"""SELECT l.IMEI,speed,battery_voltage,ignition_status,latitude,longitude,upd_datetime
                                        FROM tracker l, Bus b
                                        WHERE l.IMEI='{imei}' AND  l.IMEI=b.IMEI AND b.vendorId={vendorid}
                                        ORDER BY upd_datetime""",return_json=False)
                        result[routeid]=fleet
                    return jsonify(result)
                except:
                    return {"message": "An error occurred collecting report data."}, 500
            else:
                try:
                    imei=query(f"""SELECT IMEI FROM Bus WHERE routeId={data['routeId']} AND vendorId={vendorid}""",return_json=False)
                    if len(imei)==0: return {"message": "Invalid routeId."}, 404
                    fleet=query(f"""SELECT l.IMEI,speed,battery_voltage,ignition_status,latitude,longitude,upd_datetime
                                    FROM tracker l, Bus b
                                    WHERE l.IMEI='{imei[0]['IMEI']}' AND  l.IMEI=b.IMEI AND b.vendorId={vendorid}
                                    ORDER BY upd_datetime""",return_json=False)
                    return jsonify(fleet)
                except:
                    return {"message": "An error occurred collecting report data."}, 500

class Alert(Resource):
    @jwt_required
    def get(self):
        vendorid=get_jwt_claims()['vendorid']
        parser=reqparse.RequestParser()
        parser.add_argument('fromDate',type=str,required=True,help="fromDate cannot be left blank!")
        parser.add_argument('toDate',type=str,required=True,help="toDate cannot be left blank!")
        parser.add_argument('alertCode',type=str)
        data=parser.parse_args()
        if data['alertCode']==None:
            try:
                alerts=query(f"""SELECT a.alertCode,a.IMEI,a.smsStatus,a.alertTime,a.alertCode,ac.description
                                 FROM Alerts a,AlertsControl ac, Bus b
                                 WHERE a.alertCode=ac.alertCode AND a.IMEI=b.IMEI AND b.vendorId={vendorid} AND
                                       a.alertDate BETWEEN '{data['fromDate']}' AND '{data['toDate']}'
                                 ORDER BY a.alertTime""",return_json=False)
                return jsonify(alerts)
            except:
                return {"message": "An error occurred collecting report data."}, 500
        else:
            try:
                ac=query(f"""SELECT * FROM AlertsControl WHERE alertCode='{data['alertCode']}'""",return_json=False)
                if len(ac)==0: return {"message": "Invalid alertCode."}, 404
                alerts=query(f"""SELECT a.alertCode,a.IMEI,a.smsStatus,a.alertTime,a.alertCode,ac.description
                                 FROM Alerts a,AlertsControl ac, Bus b
                                 WHERE a.alertCode=ac.alertCode AND a.IMEI=b.IMEI AND
                                       a.alertCode='{data['alertCode']}' AND b.vendorId={vendorid} AND
                                       a.alertDate BETWEEN '{data['fromDate']}' AND '{data['toDate']}'
                                 ORDER BY a.alertTime""",return_json=False)
                return jsonify(alerts)
            except:
                return {"message": "An error occurred collecting report data."}, 500
