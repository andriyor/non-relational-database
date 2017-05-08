from flask_mongoengine import MongoEngine
from .app import app
db = MongoEngine(app)


class Port(db.Document):
    port_name = db.StringField()


class Ship(db.Document):
    name = db.StringField()
    type = db.StringField()


class Container(db.Document):
    product_description = db.StringField()
    discharge_rules = db.StringField()


class Consignee(db.Document):
    consignee_name = db.StringField()


class Flight(db.Document):
    ship = db.ReferenceField(Ship)
    port_departure = db.ReferenceField(Port)
    port_arrival = db.ReferenceField(Port)
    departure_date = db.DateTimeField()
    arrival_date = db.DateTimeField()


class Invoice(db.Document):
    container = db.ReferenceField(Container)
    flight = db.ReferenceField(Flight)
    consignee = db.ReferenceField(Consignee)
