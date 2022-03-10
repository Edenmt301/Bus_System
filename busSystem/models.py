from itertools import count
from flask_sqlalchemy import SQLAlchemy
from busSystem import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model , UserMixin) :
    id = db.Column(db.Integer , primary_key = True)
    password = db.Column(db.String(60) , nullable = False)
    phone_number = db.Column(db.String(60))
    time = db.Column(db.DateTime , default = datetime.now)
    uname = db.Column(db.String(20) , unique = True , nullable = False)
    email = db.Column(db.String(50) , unique = True , nullable = False)
    role = db.Column(db.String(20))

    def get_id(self):
        try:
            return (self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def __repr__(self):
        return  'User(%s , %s)' % (self.uname , self.email)

class Route_Station(db.Model):
    __tablename__ = 'route_station'
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer,db.ForeignKey('station.id'), primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), primary_key=True)
    current_count = db.Column(db.Integer)


# class station(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     station_name = db.Column(db.String(45))
#     station_location = db.Column(db.String(45))
#     routes = db.relationship('route', backref='Station', lazy=True)
#     counts = db.relationship('current_count', backref='Station', lazy=True)

#     def get_id(self):
#         try:
#             return (self.id)
#         except AttributeError:
#             raise NotImplementedError('No `id` attribute - override `get_id`')

#     def __repr__(self):
#         return  'User(%s , %s)' % (self.uname , self.email)
class Station(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(20) , unique = True , nullable = False)
    routes = db.relationship('Route_Station', backref='station',
                         primaryjoin=id == Route_Station.station_id)


class Route(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(20) , unique = True , nullable = False)
    starting_station = db.Column(db.Integer, db.ForeignKey('station.id'))
    ending_station = db.Column(db.Integer, db.ForeignKey('station.id'))
    buss = db.relationship('Bus', backref='route')
    stations = db.relationship('Route_Station', backref='route',
                         primaryjoin=id == Route_Station.route_id)

class Bus(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    current_cout = db.Column(db.Integer)
    latitude = db.Column(db.Integer)
    longtiude = db.Column(db.Integer)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'))
    driver = db.Column(db.Integer, db.ForeignKey('user.id'))

