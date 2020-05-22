from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from db import query

class Complaints(Resource):
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('cFrom',type=str,required=True,help="cFrom cannot be left blank!")
        parser.add_argument('cBody',type=str,required=True,help="cBody cannot be left blank!")
        parser.add_argument('cDate',type=str,required=True,help="cDate cannot be left blank!")
        parser.add_argument('cTime',type=str,required=True,help="cTime cannot be left blank!")
        data=parser.parse_args()
        try:
            query(f"""INSERT INTO Complaints VALUES ('{data['cFrom']}','{data['cBody']}','{data['cDate']}','{data['cTime']}')""")
        except:
            return {"message": "An error occurred while posting complaint."}, 500
        return {"message": "Complaint created successfully."}, 201

    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('cFrom',type=str)
        parser.add_argument('cDate',type=str,required=True,help='cDate cannot be left blank.')
        data=parser.parse_args()
        if data['cFrom']==None:
            try:
                return query(f"""SELECT cFrom, cBody, cTime FROM Complaints
                                 WHERE cDate='{data['cDate']}' ORDER BY cTime""")
            except:
                return {"message": "An error occurred accessing Complaints table."}, 500
        else:
            if data['cFrom'] not in ['student','staff']: return {"message":"Invalid sender details."}, 400
            try:
                return query(f"""SELECT cFrom, cBody, cTime FROM Complaints
                                 WHERE cFrom='{data['cFrom']}' AND cDate='{data['cDate']}' ORDER BY cTime""")
            except:
                return {"message": "An error occurred accessing Complaints table."}, 500
