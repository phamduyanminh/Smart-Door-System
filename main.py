import time
import board
import adafruit_dht
import digitalio
import smtplib
import ssl
from email.message import EmailMessage

# --- CONFIGURATION ---
# 1. The account SENDING the alerts (Must be Gmail)
SENDER_EMAIL = "phamduyanminh3120@gmail.com"
SENDER_PASSWORD = "YOUR_16_CHAR_APP_PASSWORD"  # <--- REPLACE THIS with your actual code

# 2. The List of People RECEIVING the alerts
# We use a list so we can send to both Email and SMS
RECIPIENTS = [
    "phamduyanminh3120@gmail.com",
    "6476075439@txt.freedommobile.ca"
]

# --- SETUP SENSOR & LEDS ---
dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

red_led = digitalio.DigitalInOut(board.D17)
red_led.direction = digitalio.Direction.OUTPUT

green_led = digitalio.DigitalInOut(board.D27)
green_led.direction = digitalio.Direction.OUTPUT

yellow_led = digitalio.DigitalInOut(board.D22)
yellow_led.direction = digitalio.Direction.OUTPUT

# --- ALERT SYSTEM SETUP ---
last_alert_time = 0
ALERT_DELAY = 60  

def send_alert(subject, body):
    print(f"Initiating Alert: {subject}...")
    
    context = ssl.create_default_context()
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context) # Secure the connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            
            for contact in RECIPIENTS:
                msg = EmailMessage()
                msg.set_content(body)
                msg['Subject'] = subject
                msg['From'] = SENDER_EMAIL
                msg['To'] = contact
                
                server.send_message(msg)
                print(f"Sent to: {contact}")
                
    except Exception as e:
        print(f"Failed to send: {e}")

def flash_led(led, duration=0.5):
    led.value = True
    time.sleep(duration)
    led.value = False
    time.sleep(0.1)

    print("Smart Door System (Final Version) starting... Press Ctrl+C to stop")

    while True:
        try:
            temp_c = dhtDevice.temperature
            humidity = dhtDevice.humidity
            print(f"\nTemp: {temp_c:.1f} C - Humidity: {humidity}%")

            
            # Condition 1: TOO HOT (> 20C)
            if temp_c > 20:
                print("Status: Too Hot -> Closing Door & AC On")
                flash_led(red_led)
                flash_led(yellow_led)
                
                if (time.time() - last_alert_time) > ALERT_DELAY:
                    send_alert("HOME ALERT: High Temp", f"Warning! Temp is {temp_c:.1f}C. Closing Door & Turning on AC.")
                    last_alert_time = time.time()

            # Condition 2: COMFORTABLE (15C - 20C)
            elif 15 <= temp_c <= 20:
                print("Status: Comfortable -> Opening Door")
                flash_led(green_led)
                
                if (time.time() - last_alert_time) > ALERT_DELAY:
                    send_alert("HOME STATUS: Comfortable", f"All good! Temp is {temp_c:.1f}C. Opening Door.")
                    last_alert_time = time.time()

            # Condition 3: TOO COLD (< 15C)
            else:
                print("Status: Too Cold -> Closing Door & Heat On")
                flash_led(red_led)
                flash_led(yellow_led)
                
                if (time.time() - last_alert_time) > ALERT_DELAY:
                    send_alert("HOME ALERT: Low Temp", f"Warning! Temp is {temp_c:.1f}C. Closing Door & Turning on Heat.")
                    last_alert_time = time.time()

        except RuntimeError as error:
            print(f"Sensor reading error: {error.args[0]}")
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error

        time.sleep(2.0)