import logging
from flask import Flask
from flask_restful import Api
from waitress import serve
from resources.tracking import Tracking
from resources.buses import Buses
from resources.routes import Routes
from resources.drivers import Drivers
from resources.sos import Sos
from resources.alerts import Alerts
from resources.users import Users

app=Flask(__name__)
app.secret_key='bustrackingsystem'
api = Api(app)

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

if __name__ == '__main__':
    serve(app,host='127.0.0.1',port=2000)
