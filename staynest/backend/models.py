from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id         = db.Column(db.Integer,     primary_key=True)
    name       = db.Column(db.String(120), nullable=False)
    email      = db.Column(db.String(255), nullable=False, unique=True)
    password   = db.Column(db.String(255), nullable=False)
    role       = db.Column(db.String(20), nullable=False, default='guest')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookings   = db.relationship('Booking',  backref='user',     lazy=True)
    properties = db.relationship('Property', backref='host',     lazy=True)

    def to_dict(self):
        return {
            'id':         self.id,
            'name':       self.name,
            'email':      self.email,
            'role':       self.role,
            'created_at': self.created_at.isoformat()
        }


class Property(db.Model):
    __tablename__ = 'properties'

    id          = db.Column(db.Integer,        primary_key=True)
    host_id     = db.Column(db.Integer,        db.ForeignKey('users.id'),  nullable=False)
    name        = db.Column(db.String(200),    nullable=False)
    description = db.Column(db.Text)
    location    = db.Column(db.String(255),    nullable=False)
    price       = db.Column(db.Numeric(10, 2), nullable=False)
    bedrooms    = db.Column(db.Integer,        nullable=False, default=1)
    guests      = db.Column(db.Integer,        nullable=False, default=2)
    image_url   = db.Column(db.String(500))
    created_at  = db.Column(db.DateTime,       default=datetime.utcnow)

    bookings    = db.relationship('Booking', backref='property', lazy=True)

    def to_dict(self):
        return {
            'id':          self.id,
            'host_id':     self.host_id,
            'host_name':   self.host.name if self.host else None,
            'name':        self.name,
            'description': self.description,
            'location':    self.location,
            'price':       float(self.price),
            'bedrooms':    self.bedrooms,
            'guests':      self.guests,
            'image_url':   self.image_url,
            'created_at':  self.created_at.isoformat()
        }


class Booking(db.Model):
    __tablename__ = 'bookings'

    id          = db.Column(db.Integer,        primary_key=True)
    user_id     = db.Column(db.Integer,        db.ForeignKey('users.id'),       nullable=False)
    property_id = db.Column(db.Integer,        db.ForeignKey('properties.id'),  nullable=False)
    check_in    = db.Column(db.Date,           nullable=False)
    check_out   = db.Column(db.Date,           nullable=False)
    guests      = db.Column(db.Integer,        nullable=False, default=1)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    status      = db.Column(db.String(20),     nullable=False, default='pending')
    created_at  = db.Column(db.DateTime,       default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':             self.id,
            'user_id':        self.user_id,
            'property_id':    self.property_id,
            'property_name':  self.property.name if self.property else None,
            'property_image': self.property.image_url if self.property else None,
            'location':       self.property.location if self.property else None,
            'check_in':       self.check_in.isoformat(),
            'check_out':      self.check_out.isoformat(),
            'guests':         self.guests,
            'total_price':    float(self.total_price),
            'status':         self.status,
            'created_at':     self.created_at.isoformat()
        }
