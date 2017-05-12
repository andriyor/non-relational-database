from flask_mongoengine import MongoEngine
from lab_3.app import app
from datetime import datetime
db = MongoEngine(app)


class Port(db.Document):
    name = db.StringField(unique=True)


class Ship(db.Document):
    name = db.StringField(unique=True)
    type = db.StringField()


class Container(db.Document):
    product_description = db.StringField()
    discharge_rules = db.StringField()


class Consignee(db.Document):
    name = db.StringField(unique=True)


class Flight(db.Document):
    number = db.IntField()
    ship = db.ReferenceField(Ship)
    port_departure = db.ReferenceField(Port)
    port_arrival = db.ReferenceField(Port)
    departure_date = db.DateTimeField()
    arrival_date = db.DateTimeField()


class Invoice(db.Document):
    container = db.ReferenceField(Container)
    flight = db.ReferenceField(Flight)
    consignee = db.ReferenceField(Consignee)
