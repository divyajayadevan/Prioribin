from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class WasteBin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bin_id = db.Column(db.String(50), unique=True, nullable=False)
    location_lat = db.Column(db.Float, nullable=False)
    location_lon = db.Column(db.Float, nullable=False)
    fill_level = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default="Normal")
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "bin_id": self.bin_id,
            "lat": self.location_lat,
            "lon": self.location_lon,
            "fill_level": self.fill_level,
            "status": self.status
        }

class BinHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bin_id = db.Column(db.String(50), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    collector_name = db.Column(db.String(50), nullable=True)  # NEW: Who did it?
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

from werkzeug.security import generate_password_hash, check_password_hash
import re

def validate_password_policy(password):
    prefix = "The password is not in the right format. "
    if len(password) < 8:
        return False, prefix + "It must be at least 8 characters long."
    if not re.search(r"[a-z]", password):
        return False, prefix + "It must contain at least one lowercase letter."
    if not re.search(r"[A-Z]", password):
        return False, prefix + "It must contain at least one uppercase letter."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>\-_+=\[\]\\/']", password):
        return False, prefix + "It must contain at least one special character."
    return True, ""

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# --- NEW TABLE FOR TRACKING COLLECTORS ---
class Collector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    lat = db.Column(db.Float, nullable=True)
    lon = db.Column(db.Float, nullable=True)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "name": self.name,
            "username": self.username,
            "lat": self.lat,
            "lon": self.lon,
            "last_active": self.last_active.isoformat()
        }