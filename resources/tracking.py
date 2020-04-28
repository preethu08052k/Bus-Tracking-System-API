from flask_restful import Resource, reqparse
from models.tracking import TrackingModel

class Tracking(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('VehicleId',
                        type=int,
                        required=True,
                        help="Vehicle Id cannot be left blank!"
                        )
    parser.add_argument('RecordTime',
                        type=str,
                        required=True,
                        help="Record Time cannot be left blank!"
                        )
    parser.add_argument('UpdatedTime',
                        type=str,
                        required=True,
                        help="Updatef Time cannot be left blank!"
                        )
    parser.add_argument('DataFrameId',
                        type=int,
                        required=True,
                        help="DataFrame Id cannot be left blank!"
                        )
    parser.add_argument('Latitude',
                        type=float,
                        required=True,
                        help="Vehicle's Location can't be left blank!"
                        )
    parser.add_argument('Longitude',
                        type=float,
                        required=True,
                        help="Vehicle's Location can't be left blank!"
                        )
    parser.add_argument('Altitude',
                        type=float,
                        required=True,
                        help="Vehicle's Location can't be left blank!"
                        )
    parser.add_argument('Speed',
                        type=float,
                        required=True,
                        help="Vehicle's Speed can't be left blank!"
                        )
    parser.add_argument('IgnitionStatus',
                        type=int,
                        required=True,
                        help="Vehicle's Ignition Status can't be left blank!"
                        )
    parser.add_argument('Fuel',
                        type=float,
                        required=True,
                        help="Vehicle's Fuel Reading can't be left blank!"
                        )
    parser.add_argument('Battery',
                        type=float,
                        required=True,
                        help="Vehicle's Battery Reading can't be left blank!"
                        )
    parser.add_argument('Direction',
                        type=str,
                        required=True,
                        help="Vehicle's Direction can't be left blank!"
                        )
    parser.add_argument('Distance',
                        type=float,
                        required=True,
                        help="Vehicle's Distance from CBIT can't be left blank!"
                        )
    parser.add_argument('VehicleNumber',
                        type=str,
                        required=True,
                        help="Vehicle Number can't be left blank!"
                        )
    parser.add_argument('TodayRunHrs',
                        type=str,
                        required=True,
                        help="Vehicle's Run Hours can't be left blank!"
                        )


    def post(self):
        data = Tracking.parser.parse_args()
        tracking = TrackingModel(**data)
        try:
            tracking.save()
        except:
            return {"message": "An error occurred in updating."}, 500
        return tracking.json(), 201
