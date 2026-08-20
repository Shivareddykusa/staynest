from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from datetime import date
import bcrypt

from models import db, User, Property, Booking

api = Blueprint('api', __name__, url_prefix='/api')


# ─── helpers ────────────────────────────────────────────────────────────────

def ok(data, code=200):
    return jsonify({'success': True,  'data': data}), code

def err(msg, code=400):
    return jsonify({'success': False, 'message': msg}), code


# ─── health ─────────────────────────────────────────────────────────────────

@api.get('/health')
def health():
    return ok({'status': 'ok', 'service': 'StayNest API'})


# ─── auth ────────────────────────────────────────────────────────────────────

@api.post('/register')
def register():
    body = request.get_json(silent=True) or {}
    name  = (body.get('name')  or '').strip()
    email = (body.get('email') or '').strip().lower()
    pwd   = (body.get('password') or '')
    role  = (body.get('role') or 'guest').strip().lower()

    if not name or not email or not pwd:
        return err('Name, email and password are required')
    if len(pwd) < 6:
        return err('Password must be at least 6 characters')
    if role not in ('guest', 'host'):
        role = 'guest'

    if User.query.filter_by(email=email).first():
        return err('Email already registered', 409)

    hashed = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()
    user   = User(name=name, email=email, password=hashed, role=role)
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id))
    return ok({'token': token, 'user': user.to_dict()}, 201)


@api.post('/login')
def login():
    body  = request.get_json(silent=True) or {}
    email = (body.get('email')    or '').strip().lower()
    pwd   = (body.get('password') or '')

    if not email or not pwd:
        return err('Email and password are required')

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.checkpw(pwd.encode(), user.password.encode()):
        return err('Invalid email or password', 401)

    token = create_access_token(identity=str(user.id))
    return ok({'token': token, 'user': user.to_dict()})


@api.get('/me')
@jwt_required()
def me():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return err('User not found', 404)
    return ok(user.to_dict())


# ─── properties ──────────────────────────────────────────────────────────────

@api.get('/properties')
def list_properties():
    props = Property.query.order_by(Property.created_at.desc()).all()
    return ok([p.to_dict() for p in props])


@api.get('/properties/<int:pid>')
def get_property(pid):
    prop = Property.query.get_or_404(pid)
    return ok(prop.to_dict())


@api.post('/properties')
@jwt_required()
def create_property():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return err('User not found', 404)
    if user.role != 'host':
        return err('Only hosts can create properties', 403)

    body = request.get_json(silent=True) or {}
    name     = (body.get('name')        or '').strip()
    location = (body.get('location')    or '').strip()
    price    =  body.get('price')

    if not name or not location or price is None:
        return err('Name, location and price are required')

    try:
        price = float(price)
        if price <= 0:
            raise ValueError
    except (TypeError, ValueError):
        return err('Price must be a positive number')

    prop = Property(
        host_id     = user.id,
        name        = name,
        description = (body.get('description') or '').strip() or None,
        location    = location,
        price       = price,
        bedrooms    = int(body.get('bedrooms', 1)),
        guests      = int(body.get('guests',   2)),
        image_url   = (body.get('image_url') or '').strip() or None
    )
    db.session.add(prop)
    db.session.commit()
    return ok(prop.to_dict(), 201)


# ─── bookings ─────────────────────────────────────────────────────────────────

@api.post('/bookings')
@jwt_required()
def create_booking():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return err('User not found', 404)

    body        = request.get_json(silent=True) or {}
    property_id = body.get('property_id')
    check_in_s  = body.get('check_in')
    check_out_s = body.get('check_out')
    guests      = int(body.get('guests', 1))

    if not property_id or not check_in_s or not check_out_s:
        return err('property_id, check_in and check_out are required')

    try:
        ci = date.fromisoformat(check_in_s)
        co = date.fromisoformat(check_out_s)
    except ValueError:
        return err('Dates must be in YYYY-MM-DD format')

    if ci >= co:
        return err('check_out must be after check_in')
    if ci < date.today():
        return err('check_in cannot be in the past')

    prop = Property.query.get(property_id)
    if not prop:
        return err('Property not found', 404)
    if guests > prop.guests:
        return err(f'Maximum {prop.guests} guests allowed')

    nights      = (co - ci).days
    total_price = nights * float(prop.price)

    booking = Booking(
        user_id     = user.id,
        property_id = prop.id,
        check_in    = ci,
        check_out   = co,
        guests      = guests,
        total_price = total_price
    )
    db.session.add(booking)
    db.session.commit()
    return ok(booking.to_dict(), 201)


@api.get('/bookings')
@jwt_required()
def list_bookings():
    user     = User.query.get(int(get_jwt_identity()))
    bookings = Booking.query.filter_by(user_id=user.id).order_by(Booking.created_at.desc()).all()
    return ok([b.to_dict() for b in bookings])
