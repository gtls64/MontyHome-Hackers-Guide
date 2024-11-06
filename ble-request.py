import asyncio
from bleak import BleakScanner, BleakClient


async def scan_and_select_device():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()

    if not devices:
        print("No devices found.")
        return None

    for i, device in enumerate(devices):
        print(f"[{i}] {device.name} - {device.address}")

    device_index = int(input("Select the device index to connect: "))
    selected_device = devices[device_index]

    return selected_device


async def connect_and_prompt_query(device):
    print(f"Connecting to {device.name}...")

    async with BleakClient(device.address) as client:
        print(f"Connected to {device.name} - {device.address}")

        # Use the services property instead of get_services() to remove the FutureWarning
        services = client.services
        if not services:
            await client.get_services()  # Use this to trigger service discovery

        write_characteristic = None
        notify_characteristic = None

        # Find the first writable and notify characteristics
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

        if not write_characteristic:
            print("No writable characteristic found.")
            return

        if not notify_characteristic:
            print("No notify characteristic found.")
            return

        print(f"Using characteristic {write_characteristic.uuid} for sending queries.")
        print(f"Using characteristic {notify_characteristic.uuid} for reading responses.")

        # Use client.is_connected as a property to avoid the FutureWarning
        if client.is_connected:
            def notification_handler(sender, data):
                print(f"Received data from {sender}: {data.decode()}")

            # Subscribe to notifications
            await client.start_notify(notify_characteristic.uuid, notification_handler)

            while True:
                query = input("Enter the BLE query (or 'exit' to quit): ")

                if query.lower() == 'exit':
                    print("Exiting...")
                    break

                try:
                    # Send the query to the BLE device
                    await client.write_gatt_char(write_characteristic.uuid, query.encode())
                    print(f"Query '{query}' sent.")

                    # Give some time to receive the response
                    await asyncio.sleep(2)

                except Exception as e:
                    print(f"Failed to send query: {e}")

            await client.stop_notify(notify_characteristic.uuid)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    selected_device = loop.run_until_complete(scan_and_select_device())

    if selected_device:
        loop.run_until_complete(connect_and_prompt_query(selected_device))
