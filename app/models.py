from . import db

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255),nullable=False)
    description = db.Column(db.Text, nullable=True)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    price = db.Column(db.String,nullable=True)
    type = db.Column(db.String(50),nullable=False)
    location = db.Column(db.String(255),nullable=False)
    photo = db.Column(db.String(255),nullable=True)
    
