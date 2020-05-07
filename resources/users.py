from flask import json,jsonify
from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
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

    @classmethod
    def getUserById(cls,id):
        result=query(f"""SELECT Id,username,password FROM Users WHERE Id='{id}'""",return_json=False)
        if len(result)>0: return User(result[0]['Id'],result[0]['username'],result[0]['password'])
        return None

class UserLogin(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('username',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('password',type=str,required=True,help="This field cannot be blank.")
    def post(self):
        data=self.parser.parse_args()
        user=User.getUserByName(data['username'])
        if user and safe_str_cmp(user.password,data['password']):
            access_token=create_access_token(identity=user.id,expires_delta=False)
            return {'access_token':access_token},200
        return {"message":"Invalid Credentials!"}, 401

class Users(Resource):
    @jwt_required
    def get(self):
        try:
            return query(f"""SELECT * FROM Users""")
        except:
            return {"message": "An error occurred while accessing Users table."},500
