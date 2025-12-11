# Smart Door & HVAC Controller System

## Project Overview
This project is a prototype for an automated smart home system that actively monitors environmental conditions to control building access and climate systems. Built using a Raspberry Pi 5, the system reads real-time temperature and humidity data to make logic-based decisions—simulating the opening/closing of doors and the activation of AC or Heating units.

The goal was to create a responsive IoT device that not only provides visual feedback via LEDs but also keeps the homeowner informed through remote SMS and email alerts when conditions change.

## Video Demonstration
Watch the system in action: [YouTube Demo](https://youtu.be/zT-jLKNzJtE)

## System Design & Logic
The system uses a DHT22 sensor to constantly poll the environment. Based on the temperature readings, the Python control script places the system into one of three states:

### 1. High Temperature State (> 20°C)
* **Condition:** The room is too hot.
* **Action:** The system simulates **closing the door** (to keep cool air in) and **turning on the AC**.
* **Visual Output:** Red LED flashes (Door closing), followed by Yellow LED flashing (AC active).
* **Remote Alert:** Sends an SMS/Email warning: *"High Temp! Closing Door & Turning on AC."*

### 2. Comfortable State (15°C - 20°C)
* **Condition:** The temperature is ideal.
* **Action:** The system simulates **opening the door** for natural ventilation.
* **Visual Output:** Green LED flashes.
* **Remote Alert:** Sends a status update: *"Comfortable! Opening Door."*

### 3. Low Temperature State (< 15°C)
* **Condition:** The room is too cold.
* **Action:** The system simulates **closing the door** (to keep cold air out) and **turning on the Heater**.
* **Visual Output:** Red LED flashes (Door closing), followed by Yellow LED flashing (Heater active).
* **Remote Alert:** Sends an SMS/Email warning: *"Low Temp! Closing Door & Turning on Heat."*

> **Note on Alerts:** To prevent spamming the user, I implemented a "Cooldown Timer" that prevents the system from sending more than one alert every 60 seconds.

## Hardware Setup
### Components Used
* **Raspberry Pi 5** (8GB Model)
* **DHT22** Digital Temperature & Humidity Sensor
* **3x LEDs** (Red, Green, Yellow)
* **3x Resistors** (220Ω or 330Ω)
* **Breadboard & Jumper Wires**

### Wiring Pinout
The components are connected to the Raspberry Pi 5 GPIO header as follows:

| Component | Pin Function | GPIO Pin | Physical Pin |
| :--- | :--- | :--- | :--- |
| **DHT22 Sensor** | Data Signal | GPIO 4 | Pin 7 |
| **Red LED** | Output (Door/Heat) | GPIO 17 | Pin 11 |
| **Green LED** | Output (Door Open) | GPIO 27 | Pin 13 |
| **Yellow LED** | Output (AC/Heat) | GPIO 22 | Pin 15 |

*Note: The DHT22 is powered via the 3.3V rail (Pin 1) and Ground (Pin 6). The LEDs share a common Ground connection on the breadboard wired to Physical Pin 9.*

## Software Installation
The project uses Python 3 and requires a virtual environment on the Raspberry Pi 5 (Bookworm OS).

1.  **Clone the repo and enter the directory:**
    ```bash
    git clone [https://github.com/phamduyanminh/Smart-Door-System.git](https://github.com/phamduyanminh/Smart-Door-System.git)
    cd smart-door-system
    ```

2.  **Set up the Virtual Environment:**
    ```bash
    python3 -m venv venv --system-site-packages
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip3 install adafruit-circuitpython-dht
    ```

4.  **Network Configuration (Important for iPhone Hotspots):**
    If running off a mobile hotspot, you may need to force IPv4 to allow Gmail to connect:
    ```bash
    sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1
    ```

## Usage
To start the monitoring system, run the `main.py` script. Ensure you have updated the `SENDER_EMAIL` and `SENDER_PASSWORD` variables in the code with your own App Password credentials.

```bash
python3 main.py