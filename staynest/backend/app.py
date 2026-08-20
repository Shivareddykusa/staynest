import os
import bcrypt
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv

from models import db, User, Property
from routes import api

load_dotenv()


def seed_data(app):
    with app.app_context():
        try:
            if User.query.count() == 0:
                print("Seeding initial StayNest database...")
                hashed_pw = bcrypt.hashpw('password123'.encode(), bcrypt.gensalt()).decode()
                host_user = User(name='Demo Host', email='host@staynest.com', password=hashed_pw, role='host')
                guest_user = User(name='Demo Guest', email='guest@staynest.com', password=hashed_pw, role='guest')
                db.session.add_all([host_user, guest_user])
                db.session.commit()

                sample_properties = [
                    Property(
                        host_id=host_user.id,
                        name='Cozy Beach House',
                        description='A beautiful beachfront property with stunning ocean views. Perfect for a relaxing getaway. Enjoy sunsets from the private deck, walk to the beach in minutes, and unwind in a fully equipped home.',
                        location='Goa, India',
                        price=4500.00,
                        bedrooms=2,
                        guests=4,
                        image_url='https://images.unsplash.com/photo-1499793983690-e29da59ef1c2?w=800&q=80'
                    ),
                    Property(
                        host_id=host_user.id,
                        name='Mountain Retreat Cabin',
                        description='Escape to the mountains in this charming wooden cabin surrounded by pine trees. Ideal for couples and small families who love nature, hiking, and fresh mountain air.',
                        location='Manali, Himachal Pradesh',
                        price=3200.00,
                        bedrooms=1,
                        guests=2,
                        image_url='https://images.unsplash.com/photo-1449158743715-0a90ebb6d2d8?w=800&q=80'
                    ),
                    Property(
                        host_id=host_user.id,
                        name='Heritage City Apartment',
                        description='A tastefully decorated apartment in the heart of the old city. Walking distance to museums, restaurants, and local markets. Great base for city exploration.',
                        location='Jaipur, Rajasthan',
                        price=2800.00,
                        bedrooms=2,
                        guests=3,
                        image_url='https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&q=80'
                    ),
                    Property(
                        host_id=host_user.id,
                        name='Luxury Villa with Pool',
                        description='Indulge in this stunning villa featuring a private swimming pool, lush garden, and spacious interiors. Ideal for groups and families looking for a premium experience.',
                        location='Udaipur, Rajasthan',
                        price=9500.00,
                        bedrooms=4,
                        guests=8,
                        image_url='https://images.unsplash.com/photo-1613977257363-707ba9348227?w=800&q=80'
                    ),
                    Property(
                        host_id=host_user.id,
                        name='Backwater Houseboat',
                        description='Experience the famous Kerala backwaters from a traditional wooden houseboat. Includes meals, guided boat tours, and breathtaking scenic views.',
                        location='Alleppey, Kerala',
                        price=6000.00,
                        bedrooms=2,
                        guests=4,
                        image_url='https://images.unsplash.com/photo-1578645510447-e20b4311e3ce?w=800&q=80'
                    ),
                    Property(
                        host_id=host_user.id,
                        name='Forest Eco Cottage',
                        description='An eco-friendly cottage nestled deep in the forest. Solar-powered, with organic meals and guided nature walks. Perfect for those seeking peace and sustainability.',
                        location='Coorg, Karnataka',
                        price=3800.00,
                        bedrooms=1,
                        guests=2,
                        image_url='https://images.unsplash.com/photo-1510798831971-661eb04b3739?w=800&q=80'
                    )
                ]
                db.session.add_all(sample_properties)
                db.session.commit()
                print("Seeding complete: 2 users, 6 properties created.")
        except Exception as e:
            print(f"Note on initial seed/table verification: {e}")


def create_app():
    app = Flask(__name__)

    # ── Database ──────────────────────────────────────────────────────────────
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '3306')
    db_name = os.getenv('DB_NAME', 'staynest')
    db_user = os.getenv('DB_USER', 'root')
    db_pass = os.getenv('DB_PASS', '')

    if db_pass:
        mysql_uri = f'mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
    else:
        mysql_uri = f'mysql+pymysql://{db_user}@{db_host}:{db_port}/{db_name}'

    db_uri = os.getenv('DATABASE_URL', mysql_uri)
    final_uri = db_uri

    # Test if MySQL is reachable on localhost; if not, fallback to SQLite for local mode
    if ('localhost' in db_uri or '127.0.0.1' in db_uri) and not os.getenv('FORCE_MYSQL'):
        from sqlalchemy import create_engine
        try:
            test_engine = create_engine(db_uri, connect_args={'connect_timeout': 1})
            with test_engine.connect() as conn:
                pass
            test_engine.dispose()
        except Exception as ex:
            print(f"[*] MySQL not active on localhost ({ex}). Using local SQLite for standalone mode.")
            final_uri = 'sqlite:///staynest.db'

    app.config['SQLALCHEMY_DATABASE_URI'] = final_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ── JWT ────────────────────────────────────────────────────────────────────
    app.config['JWT_SECRET_KEY'] = os.getenv(
        'JWT_SECRET_KEY', 'staynest-super-secret-jwt-key-2026'
    )
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False   # no expiry for demo

    # ── Extensions ────────────────────────────────────────────────────────────
    CORS(app, resources={r'/api/*': {'origins': '*'}})
    db.init_app(app)
    JWTManager(app)

    app.register_blueprint(api)

    @app.get('/')
    def root():
        return {
            'service': 'StayNest REST API Backend',
            'version': '1.0.0',
            'frontend_url': 'http://localhost:8000',
            'endpoints': {
                'health': '/api/health',
                'properties': '/api/properties',
                'property_by_id': '/api/properties/1',
                'login': 'POST /api/login',
                'register': 'POST /api/register',
                'bookings': 'GET/POST /api/bookings'
            }
        }

    # ── Create tables & seed data ─────────────────────────────────────────────
    with app.app_context():
        db.create_all()
        seed_data(app)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(
        host  = '0.0.0.0',
        port  = int(os.getenv('PORT', 5000)),
        debug = os.getenv('FLASK_DEBUG', '1') == '1'
    )

