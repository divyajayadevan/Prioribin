from flask import Flask, request, jsonify, render_template
from models import db, WasteBin
from flask_cors import CORS
from datetime import datetime

# --- 1. SETUP & CONFIGURATION ---
app = Flask(__name__)
CORS(app) # Allows the frontend/hardware to talk to the backend

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prioribin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create Database tables (Run once)
with app.app_context():
    db.create_all()

# --- 2. LOGIC & ALGORITHMS ---
def calculate_status(fill_level):
    if fill_level >= 90:
        return "Critical" # High Priority
    elif fill_level >= 70:
        return "Warning"  # Medium Priority
    else:
        return "Normal"   # Low Priority

# --- 3. ROUTES (PAGES) ---

# Landing Page
@app.route('/')
def home():
    return render_template('home.html')

# Admin Interface (Add Bins & View Map)
@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    # Logic to Add a New Bin manually
    if request.method == 'POST':
        b_id = request.form.get('bin_id')
        lat = request.form.get('lat')
        lon = request.form.get('lon')
        
        # Check if bin exists, if not create it
        if not WasteBin.query.filter_by(bin_id=b_id).first():
            new_bin = WasteBin(bin_id=b_id, location_lat=float(lat), location_lon=float(lon), fill_level=0)
            db.session.add(new_bin)
            db.session.commit()
            
    bins = WasteBin.query.all()
    return render_template('admin.html', bins=bins)

# Collector Interface (Optimized Route)
@app.route('/collector')
def collector_dashboard():
    # Only show bins that need attention (Warning or Critical)
    priority_bins = WasteBin.query.filter(WasteBin.status != 'Normal').all()
    return render_template('collector.html', bins=priority_bins)

# --- 4. API ENDPOINTS (FOR HARDWARE & JS) ---

# Receive Data from Hardware (Event-Triggered)
@app.route('/api/update_bin', methods=['POST'])
def update_bin():
    data = request.json
    
    b_id = data.get('bin_id')
    level = data.get('fill_level') 
    
    bin_obj = WasteBin.query.filter_by(bin_id=b_id).first()
    
    if bin_obj:
        bin_obj.fill_level = level
        bin_obj.status = calculate_status(level)
        bin_obj.last_updated = datetime.utcnow()
        db.session.commit()
        return jsonify({"message": "Data Updated", "priority": bin_obj.status}), 200
    else:
        return jsonify({"error": "Bin not found"}), 404

# Mark as Collected (Reset Bin)
@app.route('/api/collect_bin/<bin_id>', methods=['POST'])
def collect_bin(bin_id):
    bin_obj = WasteBin.query.filter_by(bin_id=bin_id).first()
    if bin_obj:
        bin_obj.fill_level = 0
        bin_obj.status = "Normal"
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False}), 404

# Get all bins (For Map updates)
@app.route('/api/get_bins', methods=['GET'])
def get_bins():
    bins = WasteBin.query.all()
    return jsonify([b.to_dict() for b in bins])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)