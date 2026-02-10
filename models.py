from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# This is the variable 'db' that app.py is looking for!
db = SQLAlchemy()

class WasteBin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bin_id = db.Column(db.String(50), unique=True, nullable=False) # e.g., "BIN-001"
    location_lat = db.Column(db.Float, nullable=False)
    location_lon = db.Column(db.Float, nullable=False)
    fill_level = db.Column(db.Integer, default=0) # Percentage 0-100
    status = db.Column(db.String(20), default="Normal") # Normal, Warning, Critical
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "bin_id": self.bin_id,
            "location": {"lat": self.location_lat, "lon": self.location_lon},
            "fill_level": self.fill_level,
            "status": self.status,
            "last_updated": self.last_updated.strftime("%Y-%m-%d %H:%M:%S")
        }