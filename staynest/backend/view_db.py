"""
StayNest Database Viewer
Run: python view_db.py
"""
import sys

# Ensure UTF-8 output on Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from app import app
from models import db, User, Property, Booking

with app.app_context():
    print("=" * 65)
    print("                    STAYNEST DATABASE VIEWER")
    print("=" * 65)

    # 1. Users
    print("\n--- [1] USERS TABLE ---")
    users = User.query.all()
    if not users:
        print("  (No users found)")
    else:
        for u in users:
            print(f"  [ID {u.id}] Name: {u.name:<15} Email: {u.email:<22} Role: {u.role}")

    # 2. Properties
    print("\n--- [2] PROPERTIES TABLE ---")
    properties = Property.query.all()
    if not properties:
        print("  (No properties found)")
    else:
        for p in properties:
            print(f"  [ID {p.id}] {p.name:<25} | {p.location:<25} | Rs. {float(p.price):,.2f}/night")

    # 3. Bookings
    print("\n--- [3] BOOKINGS TABLE ---")
    bookings = Booking.query.all()
    if not bookings:
        print("  (No bookings made yet)")
    else:
        for b in bookings:
            print(f"  [ID {b.id}] User {b.user_id} -> Property {b.property_id} ({b.check_in} to {b.check_out}) | Total: Rs. {float(b.total_price):,.2f} | Status: {b.status}")

    print("\n" + "=" * 65)
