from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from db import query

class Vendors(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('vendorId',type=int)
        data=parser.parse_args()
        if data['vendorId']==None:
            try:
                return query(f"""SELECT * FROM Vendors""")
            except:
                return {"message": "An error occurred while accessing Vendors table."},500
        else:
            try:
                return query(f"""SELECT * FROM Vendors WHERE vendorId={data['vendorId']}""")
            except:
                return {"message": "An error occurred while accessing Vendors table."},500

    @jwt_required
    def delete(self):
        parser=reqparse.RequestParser()
        parser.add_argument('vendorId',type=int,required=True,help="vendorId cannot be left blank!")
        data=parser.parse_args()
        try:
            check=query(f"""SELECT * FROM Vendors WHERE vendorId={data['vendorId']}""",return_json=False)
            if len(check)==0: return {"message" : "No such Vendor found."}, 404
            query(f"""DELETE FROM Vendors WHERE vendorId={data['vendorId']}""")
        except:
            return {"message" : "An error occurred while deleting."}, 500
        return {"message" : "Deleted successfully."}, 200

    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('vendorName',type=str,required=True,help="vendorName cannot be left blank!")
        data=parser.parse_args()
        try:
            check=query(f"""SELECT vendorId FROM Vendors WHERE vendorName='{data['vendorName']}'""",return_json=False)
            if len(check)>0: return {"message":"Vendor already exists!"}, 400
            query(f"""INSERT INTO Vendors(vendorName) VALUES('{data['vendorName']}')""")
        except:
           return {"message": "An error occurred while creating."}, 500
        return {"message": "Vendor created successfully."}, 201

    @jwt_required
    def put(self):
        parser=reqparse.RequestParser()
        parser.add_argument('vendorId',type=int,required=True,help="vendorId cannot be left blank!")
        parser.add_argument('vendorName',type=str,required=True,help="vendorName cannot be left blank!")
        data=parser.parse_args()
        try:
            check=query(f"""SELECT vendorId FROM Vendors WHERE vendorId={data['vendorId']}""",return_json=False)
            if len(check)==0: return {"message":"Vendor doesn't exist!"}, 400
            query(f"""UPDATE Vendors SET vendorName='{data['vendorName']}'
                                     WHERE vendorId={data['vendorId']}""")
        except:
           return {"message": "An error occurred while updating."}, 500
        return {"message": "Vendor updated successfully."}, 201
