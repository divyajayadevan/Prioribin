import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import db, WasteBin

app = Flask(__name__, instance_relative_config=True)

# --- Config ---
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

# --- Web Routes ---
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin')
def admin_dashboard():
    # Sort by Critical first so they appear at the top
    bins = WasteBin.query.order_by(WasteBin.fill_level.desc()).all()
    return render_template('admin.html', bins=bins)

@app.route('/collector')
def collector_dashboard():
    # LOGIC: Only show bins that NEED collection (Warning/Critical)
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
            db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/manual_update', methods=['POST'])
def manual_update():
    """Allows Admin to manually set fill level for testing"""
    bin_id = request.form.get('bin_id')
    fill_level = request.form.get('fill_level')
    
    bin_obj = WasteBin.query.filter_by(bin_id=bin_id).first()
    if bin_obj and fill_level:
        bin_obj.fill_level = int(fill_level)
        bin_obj.status = calculate_status(int(fill_level))
        db.session.commit()
        
    return redirect(url_for('admin_dashboard'))

# --- API Endpoints ---
@app.route('/api/update_bin', methods=['POST'])
def update_bin():
    data = request.json
    if not data: return jsonify({"error": "No data"}), 400

    bin_obj = WasteBin.query.filter_by(bin_id=data['bin_id']).first()
    if bin_obj:
        bin_obj.fill_level = int(data['fill_level'])
        bin_obj.status = calculate_status(bin_obj.fill_level)
        db.session.commit()
        return jsonify({"status": bin_obj.status}), 200
    return jsonify({"error": "Bin not found"}), 404

@app.route('/api/collect_bin/<bin_id>', methods=['POST'])
def collect_bin(bin_id):
    bin_obj = WasteBin.query.filter_by(bin_id=bin_id).first()
    if bin_obj:
        bin_obj.fill_level = 0
        bin_obj.status = "Normal"
        db.session.commit()
        return jsonify({"message": f"{bin_id} Collected & Reset", "id": bin_id}), 200
    return jsonify({"error": "Bin not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)