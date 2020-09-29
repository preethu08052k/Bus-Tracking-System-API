from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_claims
from db import query

class User():
    def __init__(self,id,username,password):
        self.id=id
        self.username=username
        self.password=password

    @classmethod
    def getUserByName(cls,user):
        result=query(f"""SELECT Id,username,password FROM Users WHERE username='{user}'""",return_json=False)
        if len(result)>0: return User(result[0]['Id'],result[0]['username'],result[0]['password'])
        return None

class UserRegister(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('username',type=str,required=True,help="Username cannot be left blank!")
        parser.add_argument('password',type=str,required=True,help="Password cannot be left blank!")
        parser.add_argument('firstName',type=str,required=True,help="Firstname cannot be left blank!")
        parser.add_argument('lastName',type=str,required=True,help="Lastname cannot be left blank!")
        parser.add_argument('phone',type=str,required=True,help="Phone number can't be left blank!")
        parser.add_argument('email',type=str,required=True,help="Email can't be left blank!")
        parser.add_argument('createdDate',type=str,required=True,help="Created Date can't be left blank!")
        parser.add_argument('updatedDate',type=str,required=True,help="Updated Date can't be left blank!")
        parser.add_argument('vendorId',type=int,required=True,help="vendorId can't be left blank!")
        data=parser.parse_args()
        if User.getUserByName(data['username']):
            return {"message": "A user with that username already exists"}, 400
        try:
            query(f"""INSERT INTO Users(username,password,firstName,lastName,phone,email,createdDate,updatedDate,vendorId)
                                  VALUES('{data['username']}','{data['password']}','{data['firstName']}',
                                        '{data['lastName']}','{data['phone']}','{data['email']}',
                                        '{data['createdDate']}','{data['updatedDate']}',{data['vendorId']})""")
        except:
            return {"message": "An error occurred while registering."}, 500
        return {"message": "User created successfully."}, 201

class UserLogin(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('username',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('password',type=str,required=True,help="This field cannot be blank.")
    def post(self):
        data=self.parser.parse_args()
        user=User.getUserByName(data['username'])
        if user and safe_str_cmp(user.password,data['password']):
            access_token=create_access_token(identity=user.id,expires_delta=False)
            return {
                    'access_token':access_token,
                    'vendorName':query(f"""SELECT vendorName FROM Users u, Vendors v
                                           WHERE u.Id={user.id} AND u.vendorId=v.vendorId
                                           """,return_json=False)[0]['vendorName']
                   },200
        return {"message":"Invalid Credentials!"}, 401

class Users(Resource):
    @jwt_required
    def get(self):
        vendorid=get_jwt_claims()['vendorid']
        parser=reqparse.RequestParser()
        parser.add_argument('Id',type=int)
        data=parser.parse_args()
        if data['Id']==None:
            try:
                return query(f"""SELECT * FROM Users WHERE vendorId={vendorid}""")
            except:
                return {"message": "An error occurred while accessing Users table."},500
        else:
            try:
                return query(f"""SELECT * FROM Users WHERE Id={data['Id']} AND vendorId={vendorid}""")
            except:
                return {"message": "An error occurred while accessing Users table."},500

    @jwt_required
    def put(self):
        vendorid=get_jwt_claims()['vendorid']
        parser=reqparse.RequestParser()
        parser.add_argument('Id',type=int,required=True,help="UserId cannot be left blank!")
        parser.add_argument('username',type=str,required=True,help="Username cannot be left blank!")
        parser.add_argument('password',type=str,required=True,help="Password cannot be left blank!")
        parser.add_argument('firstName',type=str,required=True,help="Firstname cannot be left blank!")
        parser.add_argument('lastName',type=str,required=True,help="Lastname cannot be left blank!")
        parser.add_argument('phone',type=str,required=True,help="Phone number can't be left blank!")
        parser.add_argument('email',type=str,required=True,help="Email can't be left blank!")
        parser.add_argument('createdDate',type=str,required=True,help="Created Date can't be left blank!")
        parser.add_argument('updatedDate',type=str,required=True,help="Updated Date can't be left blank!")
        data=parser.parse_args()
        try:
            check=query(f"""SELECT Id FROM Users WHERE Id={data['Id']} AND vendorId={vendorid}""",return_json=False)
            if len(check)==0: return {"message":"User doesn't exist!"}, 400
            query(f"""UPDATE Users SET username='{data['username']}',password='{data['password']}',
                                       firstName='{data['firstName']}',lastName='{data['lastName']}',
                                       phone='{data['phone']}',email='{data['email']}',
                                       createdDate='{data['createdDate']}',updatedDate='{data['updatedDate']}'
                                   WHERE Id={data['Id']}""")
        except:
            return {"message": "An error occurred while updating."}, 500
        return {"message": "User updated successfully."}, 201

    @jwt_required
    def delete(self):
        vendorid=get_jwt_claims()['vendorid']
        parser=reqparse.RequestParser()
        parser.add_argument('Id',type=int,required=True,help="UserId cannot be left blank!")
        data=parser.parse_args()
        try:
            check=query(f"""SELECT * FROM Users WHERE Id={data['Id']} AND vendorId={vendorid}""",return_json=False)
            if len(check)==0: return {"message" : "No such User found."}, 404
            query(f"""DELETE FROM Users WHERE Id={data['Id']} AND vendorId={vendorid}""")
        except:
            return {"message" : "An error occurred while deleting."}, 500
        return {"message" : "Deleted successfully."}, 200
