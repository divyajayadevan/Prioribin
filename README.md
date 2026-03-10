# Prioribin

![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Leaflet](https://img.shields.io/badge/Leaflet.js-Maps-199900?style=for-the-badge&logo=leaflet&logoColor=white)
![License](https://img.shields.io/badge/License-Apache_2.0-10b981?style=for-the-badge)

**Prioribin** is an intelligent, priority-based waste management system that uses edge-simulated IoT sensors, real-time interactive mapping, and dynamic route optimization to revolutionize how facilities handle waste collection.

> Built by **Divya Jayadevan**, **Anna Sony**, **Grace Mariya C J**, **Arjun Raj Anies**

---

## Features

| Feature | Description |
|---|---|
| **Admin Dashboard** | Central command center to monitor all bins across the facility in real-time on an interactive map |
| **Collector App** | Mobile-responsive portal for waste collectors with secure login and GPS tracking |
| **Dynamic Routing** | Calculates the optimal route from the collector's live GPS location to the most critical bins |
| **Edge Intelligence** | Hardware simulator mimics real IoT sensors processing data locally and pushing events to the cloud |
| **Analytics** | Logs all fill events and collections into interactive charts for historical analysis |
| **Authentication** | Secure collector registration and login system managed by the admin |

---

## Technology Stack

### Backend
- **Python** — Core application logic and scripting
- **Flask** — Lightweight web framework for routing and REST APIs
- **Flask-SQLAlchemy** — ORM for clean, Pythonic database interactions
- **SQLite** — Serverless, zero-config database stored in a single file
- **Werkzeug** — Password hashing for secure collector authentication

### Frontend
- **HTML5 & Jinja2** — Server-side templating with dynamic data injection
- **Vanilla CSS** — Custom styling with CSS variables, animations, and responsive design
- **JavaScript (ES6)** — Asynchronous data fetching, real-time UI updates, and scroll interactions

### Mapping & Navigation
- **Leaflet.js** — Open-source interactive maps for bin and collector visualization
- **Leaflet-Routing-Machine** — Turn-by-turn route calculation for collector navigation

### Analytics & Simulation
- **Chart.js** — Client-side rendering of historical bin data into line graphs
- **Python `requests`** — Simulates HTTPS POST payloads identical to real ESP32/Raspberry Pi sensors

### Deployment
- **PythonAnywhere** — Cloud hosting optimized for Python web applications
- **Git & GitHub** — Version control and code deployment pipeline

---

## Project Structure

```
Prioribin/
├── app.py
├── models.py
├── simulate_hardware.py
├── requirements.txt
├── instance/
│   └── prioribin.db
├── static/
│   └── style.css
└── templates/
    ├── home.html
    ├── admin.html
    ├── collector.html
    ├── collector_login.html
    └── history.html
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone https://github.com/divyajayadevan/Prioribin.git
cd Prioribin
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the Web Server
```bash
python app.py
```
> The app will be live at `http://127.0.0.1:5000`

### 5. Start the Hardware Simulator
Open a **second terminal** and run:
```bash
python simulate_hardware.py
```
> Bins will automatically start filling up on the dashboard.

---

## Deployment (PythonAnywhere)

1. Clone the repo into your PythonAnywhere Bash console
2. Configure the WSGI file to point to `app.py`
3. Run the simulator against your live site:
```bash
python simulate_hardware.py --url https://prioribin.pythonanywhere.com
```

---

## Live Demo

[https://prioribin.pythonanywhere.com](https://prioribin.pythonanywhere.com)
