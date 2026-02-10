import requests
import time
import random

# --- CONFIGURATION ---
SERVER_URL = 'http://127.0.0.1:5000/api/update_bin'
BIN_ID = "BIN-01"  # <--- IMPORTANT: Make sure this matches the ID you added in Admin Dashboard

print(f"Starting Hardware Simulation for {BIN_ID}...")
print("Press Ctrl+C to stop.")

try:
    while True:
        # 1. Simulate Sensor Reading
        # We generate a random number.
        # Sometimes we force it high to test the "Critical" status logic.
        simulated_distance = random.randint(0, 100)
        
        # Let's bias it towards being full so you can see the red alert faster
        if random.random() > 0.7: 
            simulated_distance = random.randint(80, 100) # High fill level

        # 2. Prepare Data Packet (JSON)
        payload = {
            "bin_id": BIN_ID,
            "fill_level": simulated_distance
        }
        
        # 3. Send to Server (HTTP POST)
        try:
            response = requests.post(SERVER_URL, json=payload)
            
            if response.status_code == 200:
                print(f"✅ Sent: {simulated_distance}% | Server Reply: {response.json()['priority']}")
            elif response.status_code == 404:
                print(f"❌ Error: Bin ID '{BIN_ID}' not found on Server. Add it in Admin Dashboard first!")
            else:
                print(f"⚠️ Server Error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Could not connect to server. Is app.py running?")

        # 4. Wait before next reading
        time.sleep(3) # Send data every 3 seconds

except KeyboardInterrupt:
    print("\nSimulation Stopped.")