
import requests
import random
import time

base_url = "http://localhost:8081/insertTemperature"

def send_data():
    # Generate random values for voltage, current, power, and battery charge percentage
    voltage = random.uniform(0, 5)  # Assuming voltage range from 0 to 5 volts
    current = random.uniform(0, 10)  # Assuming current range from 0 to 10 amps
    power = voltage * current
    battery_charge_percentage = random.uniform(0, 100)  # Assuming battery charge percentage range from 0 to 100

    # Construct the URL with random values
    new_url = f"{base_url}/{voltage}/{current}/{power}/{battery_charge_percentage}"
    print("Sending data to:", new_url)

    # Send HTTP GET request
    response = requests.get(new_url)
    if response.status_code == 200:
        print("Data sent successfully.")
    else:
        print("Failed to send data. Response code:", response.status_code)

if __name__ == "__main__":
    while True:
        send_data()
        time.sleep(1)  # Wait for 1 second before sending next data

