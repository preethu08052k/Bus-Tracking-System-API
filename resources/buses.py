from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required,get_jwt_claims
from db import query

class Buses(Resource):
    @jwt_required
    def post(self):
        vendorid=get_jwt_claims()['vendorid']
        parser=reqparse.RequestParser()
        parser.add_argument('IMEI',type=str,required=True,help="IMEI cannot be left blank!")
        parser.add_argument('vehicleNo',type=str,required=True,help="vehicleNo cannot be left blank!")
        parser.add_argument('routeId',type=int,required=True,help="routeId cannot be left blank!")
        parser.add_argument('status',type=str,required=True,help="status cannot be left blank!")
        parser.add_argument('personCapacity',type=int,required=True,help="personCapacity cannot be left blank!")
        parser.add_argument('fuelCapacity',type=int,required=True,help="fuelCapacity cannot be left blank!")
        parser.add_argument('driverId',type=int,required=True,help="driverId cannot be left blank!")
        data=parser.parse_args()
        try:
            imei=query(f"""SELECT IMEI FROM Bus WHERE IMEI='{data['IMEI']}' AND vendorId={vendorid}""",return_json=False)
            if len(imei)>0: return {"message":"Bus already exists!"}, 400
            route=query(f"""SELECT routeId FROM Routes WHERE routeId={data['routeId']}""",return_json=False)
            if len(route)==0: return {"message":"Route doesn't exist!"}, 400
            route=query(f"""SELECT routeId FROM Bus WHERE routeId={data['routeId']}""",return_json=False)
            if len(route)>0: return {"message":"Route already assigned to other bus!"}, 400
            driver=query(f"""SELECT driverId FROM Driver WHERE driverId={data['driverId']}""",return_json=False)
            if len(driver)==0: return {"message":"Driver doesn't exist!"}, 400
            driver=query(f"""SELECT driverId FROM Bus WHERE driverId={data['driverId']}""",return_json=False)
            if len(driver)>0: return {"message":"Driver already assigned to other bus!"}, 400
            query(f"""INSERT INTO Bus VALUES('{data['IMEI']}','{data['vehicleNo']}',{data['routeId']},
                                     '{data['status']}',{data['personCapacity']},{data['fuelCapacity']},
                                     {data['driverId']},{vendorid})""")
        except:
           return {"message": "An error occurred while creating."}, 500
        return {"message": "Bus created successfully."}, 201

    @jwt_required
    def get(self):
        vendorid=get_jwt_claims()['vendorid']
        parser=reqparse.RequestParser()
        parser.add_argument('routeId',type=int)
        data=parser.parse_args()
        if data['routeId']==None:
            try:
                return query(f"""SELECT * FROM Bus WHERE vendorId={vendorid} ORDER BY routeId""")
            except:
                return {"message": "An error occurred while accessing Bus table."},500
        else:
            try:
                return query(f"""SELECT * FROM Bus WHERE routeId={data['routeId']} AND vendorId={vendorid} ORDER BY routeId""")
            except:
                return {"message": "An error occurred while accessing Bus table."},500

    @jwt_required
    def put(self):
        vendorid=get_jwt_claims()['vendorid']
        parser=reqparse.RequestParser()
        parser.add_argument('IMEI',type=str,required=True,help="IMEI cannot be left blank!")
        parser.add_argument('vehicleNo',type=str,required=True,help="vehicleNo cannot be left blank!")
        parser.add_argument('routeId',type=int,required=True,help="routeId cannot be left blank!")
        parser.add_argument('status',type=str,required=True,help="status cannot be left blank!")
        parser.add_argument('personCapacity',type=int,required=True,help="personCapacity cannot be left blank!")
        parser.add_argument('fuelCapacity',type=int,required=True,help="fuelCapacity cannot be left blank!")
        parser.add_argument('driverId',type=int,required=True,help="driverId cannot be left blank!")
        data=parser.parse_args()
        try:
            imei=query(f"""SELECT IMEI FROM Bus WHERE IMEI='{data['IMEI']}' AND vendorId={vendorid}""",return_json=False)
            if len(imei)==0: return {"message":"Bus doesn't exist!"}, 400
            route=query(f"""SELECT routeId FROM Routes WHERE routeId={data['routeId']}""",return_json=False)
            if len(route)==0: return {"message":"Route doesn't exist!"}, 400
            route=query(f"""SELECT routeId FROM Bus WHERE routeId={data['routeId']} AND IMEI!='{data['IMEI']}'""",return_json=False)
            if len(route)>0: return {"message":"Route already assigned to other bus!"}, 400
            driver=query(f"""SELECT driverId FROM Driver WHERE driverId={data['driverId']}""",return_json=False)
            if len(driver)==0: return {"message":"Driver doesn't exist!"}, 400
            driver=query(f"""SELECT driverId FROM Bus WHERE driverId={data['driverId']} AND IMEI!='{data['IMEI']}'""",return_json=False)
            if len(driver)>0: return {"message":"Driver already assigned to other bus!"}, 400
            query(f"""UPDATE Bus SET vehicleNo='{data['vehicleNo']}',routeId={data['routeId']},status='{data['status']}',
                                     personCapacity={data['personCapacity']},fuelCapacity={data['fuelCapacity']},
                                     driverId={data['driverId']}
                                 WHERE IMEI='{data['IMEI']}'""")
        except:
            return {"message": "An error occurred while updating."}, 500
        return {"message": "Bus updated successfully."}, 201

    @jwt_required
    def delete(self):
        vendorid=get_jwt_claims()['vendorid']
        parser=reqparse.RequestParser()
        parser.add_argument('routeId',type=int,required=True,help="routeId cannot be left blank!")
        data=parser.parse_args()
        data=parser.parse_args()
        try:
            check=query(f"""SELECT * FROM Bus WHERE routeId={data['routeId']} AND vendorId={vendorid}""",return_json=False)
            if len(check)==0: return {"message" : "No such Bus found."}, 404
            query(f"""DELETE FROM Bus WHERE routeId={data['routeId']} AND vendorId={vendorid}""")
        except:
            return {"message" : "An error occurred while deleting."}, 500
        return {"message" : "Deleted successfully."}, 200
