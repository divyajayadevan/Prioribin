import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
# Import BinHistory here
from models import db, WasteBin, BinHistory

app = Flask(__name__, instance_relative_config=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prioribin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'

db.init_app(app)

with app.app_context():
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    db.create_all()

# --- Logic ---
def calculate_status(fill_level):
    if fill_level >= 90: return "Critical"
    elif fill_level >= 70: return "Warning"
    return "Normal"

def log_event(bin_id, event_type, description):
    """Helper function to add a record to history"""
    new_log = BinHistory(bin_id=bin_id, event_type=event_type, description=description)
    db.session.add(new_log)
    # We commit in the main function calling this

# --- Web Routes ---
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin')
def admin_dashboard():
    bins = WasteBin.query.order_by(WasteBin.fill_level.desc()).all()
    return render_template('admin.html', bins=bins)

# NEW: History Route
@app.route('/history/<bin_id>')
def bin_history(bin_id):
    # Get logs sorted by newest first
    logs = BinHistory.query.filter_by(bin_id=bin_id).order_by(BinHistory.timestamp.desc()).all()
    return render_template('history.html', logs=logs, bin_id=bin_id)

@app.route('/collector')
def collector_dashboard():
    priority_bins = WasteBin.query.filter(WasteBin.status.in_(['Warning', 'Critical'])).all()
    return render_template('collector.html', bins=priority_bins)

@app.route('/add_bin', methods=['POST'])
def add_bin():
    bin_id = request.form.get('bin_id')
    lat = request.form.get('lat')
    lon = request.form.get('lon')
    
    if bin_id and lat and lon:
        existing = WasteBin.query.filter_by(bin_id=bin_id).first()
        if not existing:
            new_bin = WasteBin(bin_id=bin_id, location_lat=float(lat), location_lon=float(lon))
            db.session.add(new_bin)
            log_event(bin_id, "System", "Bin initialized")
            db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/delete_bin/<bin_id>', methods=['POST'])
def delete_bin(bin_id):
    bin_obj = WasteBin.query.filter_by(bin_id=bin_id).first()
    if bin_obj:
        # Delete history first to avoid orphan records
        BinHistory.query.filter_by(bin_id=bin_id).delete()
        db.session.delete(bin_obj)
        db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/manual_update', methods=['POST'])
def manual_update():
    bin_id = request.form.get('bin_id')
    fill_level = request.form.get('fill_level')
    
    bin_obj = WasteBin.query.filter_by(bin_id=bin_id).first()
    if bin_obj and fill_level:
        lvl = int(str(fill_level).replace('%', ''))
        
        # Log if status changes to Critical
        new_status = calculate_status(lvl)
        if bin_obj.status != "Critical" and new_status == "Critical":
            log_event(bin_id, "Critical Alert", f"Manual override: Level set to {lvl}%")

        bin_obj.fill_level = lvl
        bin_obj.status = new_status
        bin_obj.last_updated = datetime.utcnow()
        db.session.commit()
        
    return redirect(url_for('admin_dashboard'))

# --- API Endpoints ---
@app.route('/api/update_bin', methods=['POST'])
def update_bin():
    data = request.json
    if not data: return jsonify({"error": "No data"}), 400

    bin_obj = WasteBin.query.filter_by(bin_id=data['bin_id']).first()
    if bin_obj:
        new_level = int(data['fill_level'])
        new_status = calculate_status(new_level)

        # LOG HISTORY: Only log if we just entered Critical state
        if bin_obj.status != "Critical" and new_status == "Critical":
            log_event(bin_obj.bin_id, "Critical Alert", f"Sensor detected high capacity: {new_level}%")
        
        bin_obj.fill_level = new_level
        bin_obj.status = new_status
        bin_obj.last_updated = datetime.utcnow()
        db.session.commit()
        return jsonify({"status": bin_obj.status}), 200
    return jsonify({"error": "Bin not found"}), 404

@app.route('/api/collect_bin/<bin_id>', methods=['POST'])
def collect_bin(bin_id):
    bin_obj = WasteBin.query.filter_by(bin_id=bin_id).first()
    if bin_obj:
        # LOG HISTORY: Collection Event
        log_event(bin_id, "Collection", "Waste collected by truck")
        
        bin_obj.fill_level = 0
        bin_obj.status = "Normal"
        bin_obj.last_updated = datetime.utcnow()
        db.session.commit()
        return jsonify({"success": True, "message": f"{bin_id} Reset", "id": bin_id}), 200
    return jsonify({"error": "Bin not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)