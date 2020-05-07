import logging
from flask import Flask,jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from waitress import serve
from resources.tracking import Tracking
from resources.buses import Buses
from resources.routes import Routes
from resources.drivers import Drivers
from resources.sos import Sos
from resources.alerts import Alerts
from resources.users import Users,UserLogin

app=Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS']=True
app.config['PREFERRED_URL_SCHEME']='https'
app.config['JWT_SECRET_KEY']='bustrackingsystemapi'
api = Api(app)

jwt = JWTManager(app)

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'error': 'authorization_required',
        "description": "Request does not contain an access token."
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'error': 'invalid_token',
        'message': 'Signature verification failed.'
    }), 401

logger=logging.getLogger('waitress')
logger.setLevel(logging.DEBUG)
logfile=logging.FileHandler('logs.txt')
logfile.setLevel(logging.DEBUG)
app.logger.addHandler(logfile)

api.add_resource(Tracking,'/tracking')
api.add_resource(Buses,'/buses')
api.add_resource(Routes,'/routes')
api.add_resource(Drivers,'/drivers')
api.add_resource(Sos,'/sos')
api.add_resource(Alerts,'/alerts')
api.add_resource(Users,'/users')
api.add_resource(UserLogin,'/login')

if __name__ == '__main__':
    server(app,host='0.0.0.0',port=80)
