import requests
import time
import random

# --- CONFIGURATION ---
SERVER_URL = 'http://127.0.0.1:5000/api/update_bin'
# We are simulating 3 separate hardware units
BINS = ["BIN-01", "BIN-02", "BIN-03"]

print("----------------------------------------")
print("🚀 Starting Hardware Simulation (3 Bins)")
print("----------------------------------------\n")

try:
    while True:
        # Loop through each bin to simulate them one by one
        for bin_id in BINS:
            
            # 1. Generate Random Fill Level (0 to 100%)
            # We bias it slightly higher so you see more alerts for testing
            fill_level = random.randint(0, 100)
            
            # 2. PRINT OUTPUT (Matching your screenshot style)
            print("-" * 40)
            
            # Simulate the "Sensor error" message occasionally (e.g., if level is very low)
            if fill_level < 5:
                print("Sensor error or bin empty")

            print(f"Bin: {bin_id}")
            print(f"Fill Level: {fill_level}%")

            # Logic for the status messages
            if fill_level >= 90:
                print("🚨 CRITICAL: Immediate collection required")
            elif fill_level >= 70:
                print("⚠️  WARNING: Schedule collection soon")
            else:
                print("✅ Status normal")

            # 3. Send Data to Flask Server
            payload = {
                "bin_id": bin_id,
                "fill_level": fill_level
            }

            try:
                requests.post(SERVER_URL, json=payload, timeout=1)
            except requests.exceptions.ConnectionError:
                print("❌ [Network Error] Could not reach server.")

            # Short pause between bins to make it readable
            time.sleep(2)

        # Wait a few seconds before checking all bins again
        print("\n... Cycling sensors ...\n")
        time.sleep(4)

except KeyboardInterrupt:
    print("\nSimulation Stopped.")