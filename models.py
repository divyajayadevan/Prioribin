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

# --- NEW TABLE FOR TRACKING COLLECTORS ---
class Collector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    lat = db.Column(db.Float, nullable=True)
    lon = db.Column(db.Float, nullable=True)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "name": self.name,
            "lat": self.lat,
            "lon": self.lon,
            "last_active": self.last_active.isoformat()
        }