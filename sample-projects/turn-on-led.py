import asyncio
from bleak import BleakScanner, BleakClient
import RPi.GPIO as GPIO

# Configuration variables
DEVICE_NAME = "YourDeviceName"      # Replace with the exact name of your BLE device
TEMPERATURE_THRESHOLD = 26.0        # Temperature threshold in Celsius
LED_PIN = 17                        # GPIO pin where the LED is connected
QUERY_DELAY = 30                    # Delay in seconds between each query

# List of queries to send and their corresponding descriptions
queries = {
    ";QT\r\n": "NTC Temperature"
}

# GPIO setup for the LED
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

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

                # Check if temperature exceeds threshold
                temperature_str = response_data.get("NTC Temperature", "")
                if temperature_str.startswith(";RT "):
                    temperature_value = int(temperature_str.replace(";RT ", "")) / 100
                    print(f"Current Temperature: {temperature_value}°C")

                    if temperature_value > TEMPERATURE_THRESHOLD:
                        GPIO.output(LED_PIN, GPIO.HIGH)
                        print(f"LED ON - Temperature is above {TEMPERATURE_THRESHOLD}°C")
                    else:
                        GPIO.output(LED_PIN, GPIO.LOW)
                        print(f"LED OFF - Temperature is below or equal to {TEMPERATURE_THRESHOLD}°C")

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
    finally:
        GPIO.cleanup()  # Ensure GPIO cleanup on exit
