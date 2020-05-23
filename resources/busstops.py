from flask import jsonify
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from db import query
from decimal import Decimal

class BusStops(Resource):
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('routeId',type=int,required=True,help="routeId cannot be left blank!")
        parser.add_argument('busStopName',type=str,required=True,help="busStopName cannot be left blank!")
        parser.add_argument('latitude',type=str,required=True,help="latitude cannot be left blank!")
        parser.add_argument('longitude',type=str,required=True,help="longitude cannot be left blank!")
        parser.add_argument('busStopNum',type=int,required=True,help="busStopNum cannot be left blank!")
        data=parser.parse_args()
        try:
            query(f"""INSERT INTO BusStops (routeId,busStopName,latitude,longitude,busStopNum)
                                    VALUES ({data['routeId']},'{data['busStopName']}',{Decimal(data['latitude'])},
                                            {Decimal(data['longitude'])},{data['busStopNum']})""")
        except:
            return {"message": "An error occurred while updating."}, 500
        return {"message": "BusStop created successfully."}, 201

    @jwt_required
    def delete(self):
        parser=reqparse.RequestParser()
        parser.add_argument('routeId',type=int,required=True,help="routeId cannot be left blank!")
        parser.add_argument('busStopNum',type=int,required=True,help="busStopNum cannot be left blank!")
        data=parser.parse_args()
        try:
            check=query(f"""SELECT * FROM BusStops WHERE routeId={data['routeId']} AND busStopNum={data['busStopNum']}""",return_json=False)
            if len(check)==0: return {"message" : "No such BusStop found."}, 404
            query(f"""DELETE FROM BusStops WHERE routeId={data['routeId']} AND busStopNum={data['busStopNum']}""")
        except:
            return {"message" : "An error occurred while deleting."}, 500
        return {"message" : "Deleted successfully."}, 200

    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('routeId',type=int)
        data=parser.parse_args()
        if data['routeId']==None:
            try:
                routeids=query(f"""SELECT DISTINCT routeId FROM BusStops""",return_json=False)
                routeids=[x['routeId'] for x in routeids]
                result={}
                for i in routeids:
                    busstops=query(f"""SELECT busStopNum,busStopName,latitude,longitude FROM BusStops
                                       WHERE routeId={i} ORDER BY busStopNum""",return_json=False)
                    result[i]=busstops
                return jsonify(result)
            except:
                return {"message" : "An error occurred while accessing BusStops table."}, 500
        else:
            try:
                return query(f"""SELECT busStopNum,busStopName,latitude,longitude FROM BusStops
                                 WHERE routeId={data['routeId']} ORDER BY busStopNum""")
            except:
                return {"message" : "An error occurred while accessing BusStops table."}, 500
