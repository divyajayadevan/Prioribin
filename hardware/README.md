# Prioribin - Hardware (Edge Intelligence)

![Arduino](https://img.shields.io/badge/Arduino-IDE_2.x-00979D?style=for-the-badge&logo=arduino&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-DevKit_V1-E7352C?style=for-the-badge&logo=espressif&logoColor=white)
![NodeMCU](https://img.shields.io/badge/NodeMCU-ESP8266-1A81C2?style=for-the-badge&logo=espressif&logoColor=white)
![License](https://img.shields.io/badge/License-Apache_2.0-10b981?style=for-the-badge)

This directory contains the embedded firmware that runs on physical IoT sensor nodes deployed inside waste bins. Each microcontroller reads an ultrasonic sensor, calculates the fill level locally (edge intelligence), and pushes the data to the Prioribin cloud server over HTTPS.

> Built by **Divya Jayadevan**, **Anna Sony**, **Grace Mariya C J**, **Arjun Raj Anies**

---

## Supported Boards

| Board | File | Bin ID | Libraries |
|---|---|---|---|
| **ESP32 DevKit V1** | `prioribinesp32.ino` | BIN-01 | WiFi, HTTPClient, WiFiClientSecure |
| **NodeMCU (ESP8266)** | `prioribinnodemcu.ino` | BIN-02 | ESP8266WiFi, ESP8266HTTPClient, WiFiClientSecureBearSSL |

---

## How It Works

```
Ultrasonic Sensor (HC-SR04)
        |
        v
  Read Distance (7 samples, median filter)
        |
        v
  Calculate Fill % (distance -> percentage)
        |
        v
  Edge Logic (classify priority: Normal / Med / High)
        |
        v
  POST JSON to Server (/api/update_bin)
        |
        v
  Prioribin Dashboard (real-time map update)
```

1. **Sensor Reading** -- The HC-SR04 ultrasonic sensor takes 7 distance readings. Invalid readings are discarded and the median of the valid readings is used for accuracy.
2. **Fill Calculation** -- The raw distance in cm is converted to a percentage using configurable bin dimensions (`BIN_EMPTY_CM` and `BIN_FULL_CM`).
3. **Edge Processing** -- Priority classification happens on-device:
   - `>= 90%` -- CRITICAL (Priority HIGH)
   - `>= 70%` -- WARNING (Priority MED)
   - `< 70%` -- Normal
4. **Event Detection** -- If the fill level drops to 0 from a non-zero state, the firmware recognizes that a collector has emptied the bin.
5. **Cloud Push** -- A JSON payload `{"bin_id": "BIN-XX", "fill_level": N}` is sent via HTTPS POST to the server. Failed requests are retried up to 3 times.

---

## Wiring Diagram

### HC-SR04 to ESP32

| HC-SR04 Pin | ESP32 Pin |
|---|---|
| VCC | 5V |
| GND | GND |
| TRIG | GPIO 5 |
| ECHO | GPIO 18 |

### HC-SR04 to NodeMCU

| HC-SR04 Pin | NodeMCU Pin |
|---|---|
| VCC | VIN (5V) |
| GND | GND |
| TRIG | D5 |
| ECHO | D6 |

---

## Configuration

Before uploading, update these constants at the top of each `.ino` file:

```cpp
const char* ssid       = "YOUR_WIFI_SSID";
const char* password   = "YOUR_WIFI_PASSWORD";
const char* serverURL  = "https://prioribin.pythonanywhere.com/api/update_bin";
const char* BIN_ID     = "BIN-01";   // Must match a bin registered in Admin Dashboard
```

Adjust the bin dimensions to match your physical bin:

```cpp
const float BIN_EMPTY_CM = 77.0;   // Distance reading when bin is empty
const float BIN_FULL_CM  =  2.0;   // Distance reading when bin is full
```

---

## Getting Started

### Prerequisites
- Arduino IDE 2.x
- ESP32 or ESP8266 board package installed in Arduino IDE
- HC-SR04 ultrasonic sensor
- USB cable for flashing

### 1. Install Board Packages

**ESP32** -- In Arduino IDE, go to File > Preferences and add this URL to Additional Board Manager URLs:
```
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```

**NodeMCU (ESP8266)** -- Add this URL instead:
```
http://arduino.esp8266.com/stable/package_esp8266com_index.json
```

Then go to Tools > Board > Board Manager and install the respective package.

### 2. Select Your Board
- **ESP32**: Tools > Board > ESP32 Dev Module
- **NodeMCU**: Tools > Board > NodeMCU 1.0 (ESP-12E Module)

### 3. Update Configuration
Edit the WiFi credentials, server URL, and bin dimensions in the `.ino` file as described above.

### 4. Upload
1. Connect the board via USB
2. Select the correct COM port under Tools > Port
3. Click Upload

### 5. Monitor
Open Serial Monitor at **115200 baud** to view live sensor output:
```
PRIORIBIN ESP32 - BIN-01
--------------------------------
Connecting to WiFi....
WiFi connected! IP: 192.168.1.42
[Wake-Up] Server awake!
--------------------------------------------------
BIN ID   : BIN-01
Distance : 45.2 cm
Fill     : 42%
STATUS   : Normal
Sending: {"bin_id": "BIN-01", "fill_level": 42}
Sent! Code: 200
Waiting 5 seconds...
```

---

## Project Structure

```
hardware/
├── README.md
├── prioribinesp32.ino
└── prioribinnodemcu.ino
```

---

## Key Design Decisions

| Decision | Rationale |
|---|---|
| **Median filter (7 samples)** | Eliminates erratic ultrasonic reflections from irregular waste surfaces |
| **On-device priority classification** | Reduces server load and enables future offline alerting |
| **3-attempt retry with backoff** | Handles intermittent WiFi or server cold-starts on PythonAnywhere |
| **Server wake-up ping on boot** | PythonAnywhere free-tier apps sleep after inactivity; a GET request wakes the server before data is sent |
| **5-second loop interval** | Balances real-time responsiveness with power efficiency |

---

## Relationship to the Simulator

The main project includes `simulate_hardware.py`, a Python script that mimics this hardware behavior for development and demo purposes. The simulator deliberately **ignores** `BIN-01` and `BIN-02` so that real hardware and simulated bins can coexist on the same dashboard without conflicts.

---

## API Reference

The firmware communicates with a single endpoint:

**POST** `/api/update_bin`

```json
{
  "bin_id": "BIN-01",
  "fill_level": 42
}
```

| Field | Type | Description |
|---|---|---|
| `bin_id` | string | Unique identifier matching a bin registered in the Admin Dashboard |
| `fill_level` | integer | Fill percentage (0 -- 100) |
