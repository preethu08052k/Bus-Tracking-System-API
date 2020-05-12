from requests import post
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from db import query

class SMS(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('to',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('message',type=str,required=True,help="This field cannot be blank.")
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        headers = {
                    'authkey': "142980AujH4djLH58b3a475",
                    'content-type': "application/json"
                  }
        payload='''{
                        "sender" : "CBITBT",
                        "route" : "4",
                        "country" : "91",
                        "sms" : [{
                                    "message" : '''

        payload+=f'''"{data['message']}","to" : [ '''
        if data['to']=='users':
            phoneNumbers=query("""SELECT phone FROM Users""",return_json=False)
            for i in phoneNumbers:
                payload+=('''"''' )+str(i['phone'])+('''"''')+(",")
            payload=payload[:-1]
            payload=payload+("""        ]
                                    }
                                ]}""")
            try:
                return post("http://api.msg91.com/api/v2/sendsms", headers=headers,data=payload).json()
            except:
                return {"message":"There was an error sending messages"},500
        elif data['to']=='drivers':
            phoneNumbers=query("""SELECT phone FROM Driver""",return_json=False)
            for i in phoneNumbers:
                payload+=('''"''' )+str(i['phone'])+('''"''')+(",")
            payload=payload[:-1]
            payload=payload+("""        ]
                                    }
                                ]}""")
            try:
                return post("http://api.msg91.com/api/v2/sendsms", headers=headers,data=payload).json()
            except:
                return {"message":"There was an error sending messages"},500
        return {"message":"Invalid input."},400
