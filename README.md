# Arduino Air Quality Monitor

Arduino-based air quality monitoring system using an **MQ-135 gas sensor**, **buzzer**, **LED control**, serial communication and a **PyQt6 desktop interface** for real-time visualization.

The system reads the analog output of an MQ-135 sensor, sends the data to a Python application through a serial connection and displays the measurements in a graphical interface.

## Overview

This project integrates embedded hardware and desktop software in a simple monitoring system.

The Arduino is responsible for:

- Reading the MQ-135 gas sensor
- Managing the monitoring state with a push button
- Activating an LED when the sensor value reaches the configured range
- Activating a buzzer as an audible alert
- Sending sensor data through the serial port
- Receiving LED intensity values from the Python application

The Python application is responsible for:

- Detecting available serial ports
- Connecting to the Arduino
- Reading sensor values in real time
- Displaying the current sensor value
- Plotting the measurements
- Controlling LED intensity from the interface
- Displaying an animation in the graphical interface

## Technologies

- Arduino
- C++
- Python
- PyQt6
- PySerial
- Matplotlib
- NumPy
- MQ-135 gas sensor
- Serial communication

## Hardware

The project uses the following components:

- Arduino board
- MQ-135 gas sensor
- Push button
- LED
- Buzzer
- Breadboard and jumper wires
- USB connection between Arduino and computer

## Hardware Connections

### MQ-135

```text
MQ-135 AO  -> Arduino A0
MQ-135 GND -> Arduino GND
MQ-135 VCC -> Arduino 5V
```

### Push Button

```text
Signal -> Arduino D4
GND    -> Arduino GND
```

The Arduino uses the internal pull-up resistor with `INPUT_PULLUP`.

### LED

```text
Signal -> Arduino D9
GND    -> Arduino GND
```

Pin D9 supports PWM and is used to control the LED intensity.

### Buzzer

```text
Signal -> Arduino D5
GND    -> Arduino GND
```

## Arduino Firmware

The Arduino firmware continuously checks the push button and manages the monitoring state.

When monitoring is enabled, the MQ-135 analog value is read from pin `A0`.

The sensor reading is then sent to the Python application through the serial port at:

```text
9600 baud
```

The main alert range is configured using:

```cpp
const int GAS_THRESHOLD_LOW = 200;
const int GAS_THRESHOLD_HIGH = 400;
```

When the sensor value is inside this range:

- The LED is activated
- The LED intensity is determined by the value received from the Python interface
- The buzzer generates an audible alert

The Python application can send values between:

```text
0 - 255
```

to control the LED PWM intensity.

## Python Application

The desktop application was developed using PyQt6.

The interface provides:

- Serial port selection
- Connect and disconnect controls
- Real-time MQ-135 sensor reading
- Real-time graph
- LED intensity control
- Animation controls

The application communicates with the Arduino using PySerial.

## Real-Time Visualization

Sensor readings received from the Arduino are displayed numerically in the interface and stored in a rolling data buffer.

Matplotlib is used to continuously update the graph.

The graph displays the raw analog value returned by the Arduino ADC.

The expected Arduino analog range is:

```text
0 - 1023
```

## LED Intensity Control

The graphical interface contains a dial with values between:

```text
0 - 255
```

When the dial is changed, the selected value is sent to the Arduino through the serial connection.

The Arduino uses this value with PWM to control the LED intensity.

## Installation

Clone the repository:

```bash
git clone https://github.com/gaboguti270601/arduino-air-quality-monitor.git
cd arduino-air-quality-monitor
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

The required Python packages are:

```text
PyQt6
pyserial
matplotlib
numpy
```

## Uploading the Arduino Firmware

Open:

```text
arduino/air_quality_monitor.ino
```

using the Arduino IDE.

Select your Arduino board and serial port.

Then upload the firmware to the board.

## Running the Python Application

After uploading the Arduino firmware, move to the Python directory:

```bash
cd python
```

Run:

```bash
python main.py
```

The application will detect the available serial ports.

Select the Arduino port from the drop-down menu and press:

```text
Connect
```

Once connected, the application will begin receiving sensor readings.

## Important Note About MQ-135 Measurements

The project displays the **raw analog output of the MQ-135 sensor**.

The values shown by the application should not automatically be interpreted as calibrated CO₂ concentration in ppm.

Obtaining reliable gas concentration measurements requires additional sensor calibration and conversion based on the MQ-135 response characteristics.

For this reason, the interface identifies the measurement as an **MQ-135 sensor value** rather than a calibrated CO₂ measurement.

## Features

- MQ-135 gas sensing
- Real-time serial communication
- Desktop interface with PyQt6
- Real-time Matplotlib graph
- Automatic serial port detection
- LED PWM intensity control
- Audible buzzer alert
- Push-button monitoring control
- Configurable sensor thresholds
- Real-time sensor value display

## Possible Improvements

Possible future improvements include:

- MQ-135 calibration
- Gas concentration estimation
- Data logging to CSV
- Historical data visualization
- Configurable alert thresholds from the GUI
- Automatic serial reconnection
- Multiple sensor support
- MQTT integration
- Remote monitoring
- Database storage
- IoT dashboard integration

## Project Context

Academic engineering project developed as part of the Telecommunications Engineering curriculum at the University of Concepción.

The project combines:

- Embedded systems
- Sensor acquisition
- Serial communications
- Python programming
- Graphical interfaces
- Real-time data visualization
- Hardware control

## Author

**Gabriel Gutiérrez Leal**  
Civil Engineer in Telecommunications  
University of Concepción
