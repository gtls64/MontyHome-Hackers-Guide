

# Monty Home Device Hacking Guide

Welcome to the **Monty Home Device Hacking Guide** repository! This guide provides step-by-step instructions for extending the functionality of the Monty Home BLE device using a Raspberry Pi. Originally designed for compost monitoring, the Monty Home device collects valuable data on temperature, humidity, and other environmental metrics. Through this guide, you’ll learn how to retrieve, display, and automate actions based on this data.

## Table of Contents

- [Overview](#overview)
- [Projects](#projects)
  - [Project 1: Temperature-Based LED Control](#project-1-temperature-based-led-control)
  - [Project 2: Display Temperature and Humidity on I2C Display](#project-2-display-temperature-and-humidity-on-i2c-display)
  - [Project 3: Temperature Alert via IFTTT](#project-3-temperature-alert-via-ifttt)
- [Setup](#setup)
  - [Hardware Requirements](#hardware-requirements)
  - [Software Requirements](#software-requirements)
- [BLE Commands](#ble-commands)
- [Running the Code](#running-the-code)
- [Customization](#customization)
- [Additional Resources](#additional-resources)

---

## Overview

This guide is designed for anyone interested in working with Bluetooth Low Energy (BLE) devices, IoT applications, or environmental monitoring. The Monty Home device communicates over BLE, providing real-time data on temperature, humidity, battery level, and more. In this repository, you’ll find three projects that use Python, BLE, and Raspberry Pi to interact with the Monty Home device.

Each project covers different functionalities:
1. **Basic LED Control Based on Temperature Thresholds**
2. **Displaying Data on an OLED Screen Using I2C**
3. **Sending Notifications via IFTTT When Conditions Are Met**

---

## Projects

### Project 1: Temperature-Based LED Control

**Objective**: Use the temperature data from the Monty Home device to control an LED on the Raspberry Pi. If the temperature exceeds a specified threshold, the LED lights up to indicate a warning.

**Skills Gained**:
- Setting up GPIO control for an LED.
- Querying BLE data.
- Basic Python programming and condition handling.

**Hardware Needed**:
- Raspberry Pi with BLE support
- LED and 330-ohm resistor

---

### Project 2: Display Temperature and Humidity on I2C Display

**Objective**: Display real-time temperature and humidity data from the Monty Home device on an OLED screen connected to the Raspberry Pi.

**Skills Gained**:
- Working with I2C devices.
- Displaying dynamic data using the SSD1306 OLED display.
- Implementing BLE data retrieval and display updates.

**Hardware Needed**:
- Raspberry Pi with BLE support
- SSD1306 OLED Display (128x32 or 128x64)

---

### Project 3: Temperature Alert via IFTTT

**Objective**: Configure the Raspberry Pi to send a notification via IFTTT if the temperature from the Monty Home device exceeds a specific threshold.

**Skills Gained**:
- Integrating with IFTTT for IoT automation.
- Sending HTTP requests with the `requests` library.
- Combining BLE data with cloud-based notifications.

**Hardware Needed**:
- Raspberry Pi with Wi-Fi
- IFTTT account

---

## Setup

### Hardware Requirements

1. **Raspberry Pi** (Zero 2 or another model with BLE support).
2. **Monty Home BLE Device**.
3. Additional hardware specific to each project, such as an LED, OLED display, and IFTTT account.

### Software Requirements

1. **Raspberry Pi OS**: Install Raspberry Pi OS Lite (for headless) or Raspberry Pi OS with Desktop (for graphical interface).
2. **Python 3**: Make sure Python 3 and `pip` are installed.
3. **Libraries**:
   - **Bleak** for BLE communication: `pip install bleak`
   - **Requests** for IFTTT integration: `pip install requests`
   - **Adafruit CircuitPython SSD1306** for OLED control: `pip install adafruit-circuitpython-ssd1306`
   - **Pillow** for image manipulation on OLED: `pip install pillow`

---

## BLE Commands

Use these commands to interact with the Monty Home device. Each command requests specific data or performs an action. You can replace or modify commands in the Python scripts as needed.

| Command   | Description                                             |
|-----------|---------------------------------------------------------|
| `;QA\r\n` | Returns the index of all data in flash memory.          |
| `;QP\r\n` | Returns index of pending data in flash memory.          |
| `;QR\r\n` | Returns a record by index, NACK if index not found.     |
| `;QS\r\n` | Returns the status of the device.                       |
| `;QL\r\n` | Returns the battery level as a percentage.              |
| `;QT\r\n` | Returns the temperature reading from the NTC sensor.    |
| `;QH\r\n` | Returns the relative humidity reading.                  |
| `;QO\r\n` | Returns the most recent TVOC reading.                   |
| `;QC\r\n` | Returns the most recent CO2 reading.                    |
| `;QU\r\n` | Returns the unique ID of the device.                    |
| `;QV\r\n` | Returns the firmware version of the device.             |
| `;CR\r\n` | Reboots the device.                                     |
| `;CF\r\n` | Performs a factory reset.                               |

---

## Running the Code

Each project contains a Python script that establishes a BLE connection, sends queries, and processes data. To run a script:

1. Open a terminal on the Raspberry Pi.
2. Navigate to the project folder:
   ```bash
   cd /path/to/project
   ```
3. Run the script:
   ```bash
   python3 project_script.py
   ```
   Replace `project_script.py` with the actual script file name, such as `project1_temperature_led.py`.

---

## Customization

### Adjusting BLE Commands
You can modify the BLE commands in the code to retrieve different types of data from the Monty Home device. For example, to query humidity instead of temperature, replace:
```python
command = ";QT\r\n"
```
with:
```python
command = ";QH\r\n"
```

### Expanding Notification Handlers
To process multiple types of data (e.g., temperature, humidity), add conditions within the `notification_handler` function to decode and display different readings.

### Integrating with Other Platforms
Consider integrating data into IoT platforms or dashboards for real-time data visualization, logging, or further automation.

---

## Additional Resources

- [Python on Raspberry Pi](https://realpython.com/python-raspberry-pi/)
- [BLE on Raspberry Pi Guide](https://www.instructables.com/Control-Bluetooth-LE-Devices-From-A-Raspberry-Pi/)
- [IFTTT Webhooks Documentation](https://ifttt.com/maker_webhooks)
- [Adafruit CircuitPython SSD1306 Guide](https://learn.adafruit.com/monochrome-oled-breakouts)

---


## Contributing

Feel free to submit pull requests, report issues, or suggest features. Any contributions to improve this guide and add new projects are welcome!

---

This README provides everything needed for users to get started with BLE communication, project setup, and code customization. Let me know if you need further details or additional sections!
