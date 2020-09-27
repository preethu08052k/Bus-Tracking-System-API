from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from db import query

class Drivers(Resource):
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('driverName',type=str,required=True,help="driverName cannot be left blank!")
        parser.add_argument('Phone',type=str,required=True,help="Phone cannot be left blank!")
        data=parser.parse_args()
        try:
            imei=query(f"""SELECT driverId FROM Driver WHERE driverName='{data['driverName']}' AND
                                                             Phone='{data['Phone']}'""",return_json=False)
            if len(imei)>0: return {"message":"Driver already exists!"}, 400
            query(f"""INSERT INTO Driver(driverName,Phone)
                                  VALUES('{data['driverName']}','{data['Phone']}')""")
        except:
           return {"message": "An error occurred while creating."}, 500
        return {"message": "Driver created successfully."}, 201

    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('driverId',type=int)
        data=parser.parse_args()
        if data['driverId']==None:
            try:
                return query(f"""SELECT * FROM Driver""")
            except:
                return {"message": "An error occurred while accessing Driver table."},500
        else:
            try:
                return query(f"""SELECT * FROM Driver WHERE driverId={data['driverId']}""")
            except:
                return {"message": "An error occurred while accessing Driver table."},500

    @jwt_required
    def delete(self):
        parser=reqparse.RequestParser()
        parser.add_argument('driverId',type=int,required=True,help="driverId cannot be left blank!")
        data=parser.parse_args()
        try:
            check=query(f"""SELECT * FROM Driver WHERE driverId={data['driverId']}""",return_json=False)
            if len(check)==0: return {"message" : "No such Driver found."}, 404
            query(f"""DELETE FROM Driver WHERE driverId={data['driverId']}""")
        except:
            return {"message" : "An error occurred while deleting."}, 500
        return {"message" : "Deleted successfully."}, 200
