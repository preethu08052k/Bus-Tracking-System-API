from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from decimal import Decimal
from db import query

class Tracking(Resource):
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('IMEI',type=str,required=True,help="Vehicle Id cannot be left blank!")
        parser.add_argument('dataframeId',type=int,required=True,help="DataFrame Id cannot be left blank!")
        parser.add_argument('deviceTime',type=str,required=True,help="Record Time cannot be left blank!")
        parser.add_argument('updatedTime',type=str,required=True,help="Updatef Time cannot be left blank!")
        parser.add_argument('latitude',type=str,required=True,help="Vehicle's Location can't be left blank!")
        parser.add_argument('longitude',type=str,required=True,help="Vehicle's Location can't be left blank!")
        parser.add_argument('speed',type=int,required=True,help="Vehicle's Speed can't be left blank!")
        parser.add_argument('ignition',type=str,required=True,help="Vehicle's Ignition Status can't be left blank!")
        parser.add_argument('fuel',type=float,required=True,help="Vehicle's Fuel Reading can't be left blank!")
        parser.add_argument('altitude',type=float,required=True,help="Vehicle's Location can't be left blank!")
        parser.add_argument('battery',type=float,required=True,help="Vehicle's Battery Reading can't be left blank!")
        parser.add_argument('runHrs',type=int,required=True,help="Vehicle's Run Hours can't be left blank!")
        parser.add_argument('alert',type=int,required=True,help="Alert can't be left blank!")
        parser.add_argument('distance',type=str,required=True,help="Vehicle's Distance from CBIT can't be left blank!")
        data=parser.parse_args()
        try:
            query(f"""INSERT INTO Rawdata (IMEI,dataframeId,deviceTime,updatedTime,latitude,longitude,
                                            speed,ignition,fuel,altitude,battery,runHrs,alert,distance)
                                  VALUES('{data['IMEI']}',{data['dataframeId']},'{data['deviceTime']}',
                                        '{data['updatedTime']}',{Decimal(data['latitude'])},{Decimal(data['longitude'])},
                                        {data['speed']},'{data['ignition']}',{data['fuel']},{data['altitude']},
                                        {data['battery']},{data['runHrs']},{data['alert']},'{data['distance']}')""")
        except:
            return {"message": "An error occurred while updating."}, 500
        return {"message": "Tracking data posted successfully."}, 201

    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('routeId',type=int)
        parser.add_argument('deviceTime',type=str)
        data=parser.parse_args()
        if  data['routeId']==None and data['deviceTime']==None:
            try:
                return query(f"""SELECT l.*,r.*,d.driverId,d.driverName,d.phone as driverPhone
                                 FROM Livedata l, Bus b, Routes r, Driver d
						         WHERE l.IMEI=b.IMEI AND b.routeId=r.routeId
                                       AND b.driverId=d.driverId
                                 ORDER BY updatedTime""")
            except:
                return {"message": "An error occurred while accessing Livedata table."},500
        elif data['routeId']!=None and data['deviceTime']==None:
            try:
                return query(f"""SELECT l.*,r.*,d.driverId,d.driverName,d.phone as driverPhone
                                 FROM Livedata l, Bus b, Routes r, Driver d
								 WHERE l.IMEI=b.IMEI AND b.routeId=r.routeId
                                       AND b.driverId=d.driverId AND r.routeId={data['routeId']}
                                 ORDER BY updatedTime""")
            except:
                return {"message": "An error occurred while accessing Livedata table."},500
        elif data['routeId']!=None and data['deviceTime']!=None:
            try:
                return query(f"""SELECT l.*,r.*,d.driverId,d.driverName,d.phone as driverPhone
                                 FROM Rawdata l, Bus b, Routes r, Driver d
								 WHERE l.IMEI=b.IMEI AND b.routeId=r.routeId AND b.driverId=d.driverId
                                       AND r.routeId={data['routeId']} AND l.deviceTime='{data['deviceTime']}'
                                 ORDER BY updatedTime""")
            except:
                return {"message": "An error occurred while accessing Rawdata table."},500
        return {"message": "Invalid Input."},400
