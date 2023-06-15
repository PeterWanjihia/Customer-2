from flask_login import UserMixin
from project import db

from faker import Faker
fake = Faker()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    role = db.Column(db.String(100))
    
class CustomerTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    date = db.Column(db.Date)
    transNumber = db.Column(db.Integer)
    transAmount = db.Column(db.Float)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(200))
    contact_info = db.Column(db.String(100))
    transactions = db.relationship('CustomerTransaction', backref='client', lazy=True)

    

    



