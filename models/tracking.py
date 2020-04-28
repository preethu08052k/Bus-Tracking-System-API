from db import db

class TrackingModel(db.Model):
    __tablename__ = 'tracking'

    Id = db.Column(db.Integer, primary_key=True)
    VehicleId = db.Column(db.Integer)
    RecordTime = db.Column(db.String(30))
    UpdatedTime = db.Column(db.String(30))
    DataFrameId = db.Column(db.Integer)
    Latitude = db.Column(db.Float)
    Longitude = db.Column(db.Float)
    Altitude = db.Column(db.Float)
    Speed = db.Column(db.Float(precision=2))
    IgnitionStatus = db.Column(db.Integer)
    Fuel = db.Column(db.Float(precision=2))
    Battery = db.Column(db.Float(precision=2))
    Direction  = db.Column(db.String(20))
    Distance  = db.Column(db.Float(precision=2))
    VehicleNumber = db.Column(db.String(10))
    TodayRunHrs = db.Column(db.String(30))

    def __init__(self,Id,VehicleId,RecordTime,UpdatedTime,DataFrameId,Latitude,Longitude,Altitude,Speed,IgnitionStatus,Fuel,Battery,Direction,Distance,
    VehicleNumber,TodayRunHrs):
        self.Id = Id
        self.VehicleId = VehicleId
        self.RecordTime = RecordTime
        self.UpdatedTime = UpdatedTime
        self.DataFrameId = DataFrameId
        self.Latitude = Latitude
        self.Longitude = Longitude
        self.Altitude = Altitude
        self.Speed = Speed
        self.IgnitionStatus = IgnitionStatus
        self.Fuel = Fuel
        self.Battery = Battery
        self.Direction  = Direction
        self.Distance  = Distance
        self.VehicleNumber = VehicleNumber
        self.TodayRunHrs = TodayRunHrs

    def json(self):
        return {
            'Id' : self.Id,
            'VehicleId' : self.VehicleId,
            'RecordTime' : self.RecordTime,
            'UpdatedTime' : self.UpdatedTime,
            'DataFrameId' : self.DataFrameId,
            'Latitude' : self.Latitude,
            'Longitude' : self.Longitude,
            'Altitude' : self.Altitude,
            'Speed' : self.Speed,
            'IgnitionStatus' : self.IgnitionStatus,
            'Fuel' : self.Fuel,
            'Battery' : self.Battery,
            'Direction' : self.Direction,
            'Distance' : self.Distance,
            'VehicleNumber' : self.VehicleNumber,
            'TodayRunHrs' : self.TodayRunHrs
            }

    def save(self):
        db.session.add(self)
        db.session.commit()
