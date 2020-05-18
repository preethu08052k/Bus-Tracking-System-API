from flask import jsonify
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from db import query

class Uptime(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('routeId',type=int)
        parser.add_argument('fromDate',type=str,required=True,help="fromDate cannot be left blank!")
        parser.add_argument('toDate',type=str,required=True,help="toDate cannot be left blank!")
        data=parser.parse_args()
        if data['routeId']==None:
            try:
                routes=query(f"""SELECT routeId,IMEI FROM Bus""",return_json=False)
                routes=[(x['routeId'],x['IMEI']) for x in routes]
                result={}
                for routeid,imei in routes:
                    runhrs=query(f"""SELECT max(runHrs) AS runHrs,updatedTime AS time
                                     FROM Rawdata
                                     WHERE IMEI='{imei}' AND
                                           deviceTime BETWEEN
                                           '{data['fromDate']}' AND '{data['toDate']}'
                                     GROUP BY deviceTime""",
                                 return_json=False)
                    runhrs=sorted(runhrs,key=lambda x:x['time'])
                    result[routeid]=runhrs
                return jsonify(result)
            except:
                return {"message": "An error occurred collecting report data."}, 500
        else:
            try:
                imei=query(f"""SELECT IMEI FROM Bus WHERE routeId={data['routeId']}""",return_json=False)
                if len(imei)==0: return {"message": "Invalid routeId."}, 400
                runhrs=query(f"""SELECT max(runHrs) AS runHrs,updatedTime AS time
                                 FROM Rawdata
                                 WHERE IMEI='{imei[0]['IMEI']}' AND
                                       deviceTime BETWEEN '{data['fromDate']}' AND '{data['toDate']}'
                                 GROUP BY deviceTime""",
                             return_json=False)
                runhrs=sorted(runhrs,key=lambda x:x['time'])
                return jsonify(runhrs)
            except:
                return {"message": "An error occurred collecting report data."}, 500

class Fleet(Resource):
    @jwt_required
    def get(self):
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
                    routes=query(f"""SELECT routeId,IMEI FROM Bus""",return_json=False)
                    routes=[(x['routeId'],x['IMEI']) for x in routes]
                    result={}
                    for routeid,imei in routes:
                        fleet=query(f"""SELECT speed,battery,ignition,latitude,longitude,updatedTime AS time
                                        FROM Rawdata WHERE IMEI='{imei}' AND deviceTime BETWEEN
                                                           '{data['fromDate']}' AND '{data['toDate']}'""",return_json=False)
                        fleet=sorted(fleet,key=lambda x:x['time'])
                        result[routeid]=fleet
                    return jsonify(result)
                except:
                    return {"message": "An error occurred collecting report data."}, 500
            else:
                try:
                    imei=query(f"""SELECT IMEI FROM Bus WHERE routeId={data['routeId']}""",return_json=False)
                    if len(imei)==0: return {"message": "Invalid routeId."}, 400
                    fleet=query(f"""SELECT speed,battery,ignition,latitude,longitude,updatedTime AS time
                                    FROM Rawdata WHERE IMEI='{imei[0]['IMEI']}' AND
                                         deviceTime BETWEEN '{data['fromDate']}' AND '{data['toDate']}'""",return_json=False)
                    fleet=sorted(fleet,key=lambda x:x['time'])
                    return jsonify(fleet)
                except:
                    return {"message": "An error occurred collecting report data."}, 500
        else:
            if data['routeId']==None:
                try:
                    routes=query(f"""SELECT routeId,IMEI FROM Bus""",return_json=False)
                    routes=[(x['routeId'],x['IMEI']) for x in routes]
                    result={}
                    for routeid,imei in routes:
                        fleet=query(f"""SELECT speed,battery,ignition,latitude,longitude,updatedTime AS time
                                        FROM Rawdata WHERE IMEI='{imei}'""",return_json=False)
                        fleet=sorted(fleet,key=lambda x:x['time'])
                        result[routeid]=fleet
                    return jsonify(result)
                except:
                    return {"message": "An error occurred collecting report data."}, 500
            else:
                try:
                    imei=query(f"""SELECT IMEI FROM Bus WHERE routeId={data['routeId']}""",return_json=False)
                    if len(imei)==0: return {"message": "Invalid routeId."}, 400
                    fleet=query(f"""SELECT speed,battery,ignition,latitude,longitude,updatedTime AS time
                                    FROM Rawdata WHERE IMEI='{imei[0]['IMEI']}'""",return_json=False)
                    fleet=sorted(fleet,key=lambda x:x['time'])
                    return jsonify(fleet)
                except:
                    return {"message": "An error occurred collecting report data."}, 500

class Alert(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('fromDate',type=str,required=True,help="fromDate cannot be left blank!")
        parser.add_argument('toDate',type=str,required=True,help="toDate cannot be left blank!")
        parser.add_argument('alertCode',type=int)
        data=parser.parse_args()
        if data['alertCode']==None:
            try:
                alerts=query(f"""SELECT a.*,ac.description FROM Alerts a,AlertsControl ac
                                 WHERE a.alertCode=ac.alertCode AND
                                       a.alertDate BETWEEN '{data['fromDate']}' AND '{data['toDate']}'""",
                             return_json=False)
                alerts=sorted(alerts,key=lambda x:x['alertDate'])
                return jsonify(alerts)
            except:
                return {"message": "An error occurred collecting report data."}, 500
        else:
            try:
                alerts=query(f"""SELECT a.*,ac.description FROM Alerts a,AlertsControl ac
                                 WHERE a.alertCode=ac.alertCode AND
                                       a.alertCode={data['alertCode']} AND
                                       a.alertDate BETWEEN '{data['fromDate']}' AND '{data['toDate']}'""",
                             return_json=False)
                alerts=sorted(alerts,key=lambda x:x['alertDate'])
                return jsonify(alerts)
            except:
                return {"message": "An error occurred collecting report data."}, 500

class Distance(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('routeId',type=int)
        parser.add_argument('fromDate',type=str,required=True,help="fromDate cannot be left blank!")
        parser.add_argument('toDate',type=str,required=True,help="toDate cannot be left blank!")
        data=parser.parse_args()
        if data['routeId']==None:
            try:
                routes=query(f"""SELECT routeId,IMEI FROM Bus""",return_json=False)
                routes=[(x['routeId'],x['IMEI']) for x in routes]
                result={}
                for routeid,imei in routes:
                    distances=query(f"""SELECT max(distance) AS distance,updatedTime AS time
                                        FROM Rawdata
                                        WHERE IMEI='{imei}' AND
                                              deviceTime BETWEEN
                                              '{data['fromDate']}' AND '{data['toDate']}'
                                        GROUP BY deviceTime""",
                                    return_json=False)
                    distances=sorted(distances,key=lambda x:x['time'])
                    result[routeid]=distances
                return jsonify(result)
            except:
                return {"message": "An error occurred collecting report data."}, 500
        else:
            try:
                imei=query(f"""SELECT IMEI FROM Bus WHERE routeId={data['routeId']}""",return_json=False)
                if len(imei)==0: return {"message": "Invalid routeId."}, 400
                distances=query(f"""SELECT max(distance) AS distance,updatedTime AS time
                                    FROM Rawdata
                                    WHERE IMEI='{imei[0]['IMEI']}' AND
                                          deviceTime BETWEEN '{data['fromDate']}' AND '{data['toDate']}'
                                    GROUP BY deviceTime""",
                                return_json=False)
                distances=sorted(distances,key=lambda x:x['time'])
                return jsonify(distances)
            except:
                return {"message": "An error occurred collecting report data."}, 500
