import asyncio
from datetime import datetime
from bleak import BleakScanner, BleakClient
import time
import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

# Configuration variables
DEVICE_NAME = "YourDeviceName"      # Replace with the exact name of your BLE device
QUERY_DELAY = 30                    # Delay in seconds between each query

# I2C display setup
I2C_WIDTH = 128
I2C_HEIGHT = 32
i2c = busio.I2C(board.SCL, board.SDA)
display = SSD1306_I2C(I2C_WIDTH, I2C_HEIGHT, i2c)

# Create a blank image to draw on
image = Image.new("1", (I2C_WIDTH, I2C_HEIGHT))
draw = ImageDraw.Draw(image)

# Font settings
font = ImageFont.load_default()

# List of queries to send and their corresponding descriptions
queries = {
    ";QT\r\n": "NTC Temperature",
    ";QH\r\n": "Humidity"
}

# Store the responses for querying
response_data = {}

async def find_device_by_name():
    print(f"Searching for BLE device named '{DEVICE_NAME}'...")
    devices = await BleakScanner.discover()

    for device in devices:
        if device.name == DEVICE_NAME:
            print(f"Device found: {device.name} - {device.address}")
            return device
    print("Device not found.")
    return None

async def connect_and_send_queries(device):
    async with BleakClient(device.address) as client:
        print(f"Connected to {device.name} - {device.address}")

        services = client.services
        if not services:
            await client.get_services()

        write_characteristic = None
        notify_characteristic = None

        # Find writable and notify characteristics
        for service in services:
            for characteristic in service.characteristics:
                if "write" in characteristic.properties:
                    write_characteristic = characteristic
                if "notify" in characteristic.properties:
                    notify_characteristic = characteristic
                if write_characteristic and notify_characteristic:
                    break
            if write_characteristic and notify_characteristic:
                break

        if not write_characteristic or not notify_characteristic:
            print("Necessary characteristics not found.")
            return None, None

        query_iterator = iter(queries.items())
        received_response_event = asyncio.Event()

        # Notification handler to process data
        def notification_handler(sender, data):
            response_str = data.decode().strip()
            current_query_key, current_query_desc = current_query
            response_data[current_query_desc] = response_str
            received_response_event.set()

        await client.start_notify(notify_characteristic.uuid, notification_handler)

        # Send each query and wait for responses
        for current_query in query_iterator:
            query_command, query_desc = current_query
            try:
                print(f"Sending query: {query_command.strip()}")
                await client.write_gatt_char(write_characteristic.uuid, query_command.encode())
                await received_response_event.wait()
                received_response_event.clear()

                # Parse temperature and humidity
                temperature_str = response_data.get("NTC Temperature", "")
                humidity_str = response_data.get("Humidity", "")

                if temperature_str.startswith(";RT "):
                    temperature_value = int(temperature_str.replace(";RT ", "")) / 100
                else:
                    temperature_value = None

                if humidity_str.startswith(";RH "):
                    humidity_value = int(humidity_str.replace(";RH ", "")) / 100
                else:
                    humidity_value = None

                # Display temperature and humidity on I2C display
                draw.rectangle((0, 0, I2C_WIDTH, I2C_HEIGHT), outline=0, fill=0)  # Clear the display
                draw.text((0, 0), f"Temp: {temperature_value:.2f}C" if temperature_value else "Temp: N/A", font=font, fill=255)
                draw.text((0, 16), f"Hum: {humidity_value:.2f}%" if humidity_value else "Hum: N/A", font=font, fill=255)
                display.image(image)
                display.show()

            except Exception as e:
                print(f"Failed to send query {query_command.strip()}: {e}")

        await client.stop_notify(notify_characteristic.uuid)
        return response_data, write_characteristic

async def run_queries(device):
    while True:
        try:
            await connect_and_send_queries(device)
            await asyncio.sleep(QUERY_DELAY)  # Delay before next query cycle
        except Exception as e:
            print(f"An error occurred: {e}. Retrying in a few seconds...")
            await asyncio.sleep(10)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        selected_device = loop.run_until_complete(find_device_by_name())
        if selected_device:
            loop.run_until_complete(run_queries(selected_device))
        else:
            print("Device not found. Exiting.")
    except Exception as e:
        print(f"Critical error: {e}")
