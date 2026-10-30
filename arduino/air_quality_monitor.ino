// Arduino Air Quality Monitoring System
//
// Hardware connections:
//
// MQ-135 gas sensor:
//   AO  -> A0
//   GND -> GND
//   VCC -> 5V
//
// Push button:
//   Signal -> D4
//   GND    -> GND
//
// LED:
//   Signal -> D9
//   GND    -> GND
//
// Buzzer:
//   Signal -> D5
//   GND    -> GND
//
// Serial communication:
//   Baud rate: 9600
//
// The Arduino sends MQ-135 sensor readings to the Python application.
// The Python application can send a value between 0 and 255 to control
// the LED intensity.

#include <Arduino.h>


// ============================================================
// Pin configuration
// ============================================================

const int SENSOR_PIN = A0;
const int BUTTON_PIN = 4;
const int LED_PIN = 9;
const int BUZZER_PIN = 5;


// ============================================================
// Air quality thresholds
// ============================================================

const int GAS_THRESHOLD_LOW = 200;
const int GAS_THRESHOLD_HIGH = 400;


// ============================================================
// Timing configuration
// ============================================================

const unsigned long DEBOUNCE_DELAY = 200;
const unsigned long SENSOR_INTERVAL = 100;


// ============================================================
// System state
// ============================================================

bool monitoringEnabled = false;
bool lastButtonState = HIGH;

int sensorValue = 0;

// Default LED intensity.
// Range: 0 - 255
int ledIntensity = 255;

unsigned long lastDebounceTime = 0;
unsigned long lastSensorRead = 0;


// ============================================================
// Setup
// ============================================================

void setup() {

  // Start serial communication with the Python application.
  Serial.begin(9600);

  // Configure hardware pins.
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  // Ensure actuators are disabled when the system starts.
  analogWrite(LED_PIN, 0);
  noTone(BUZZER_PIN);
}


// ============================================================
// Main loop
// ============================================================

void loop() {

  // Check whether the user pressed the monitoring button.
  handleButton();

  // Check whether the Python application sent a new
  // LED intensity value.
  readSerialInput();

  // Run the monitoring system only when enabled.
  if (monitoringEnabled) {

    monitorAirQuality();

  } else {

    // Turn off the actuators when monitoring is disabled.
    analogWrite(LED_PIN, 0);
    noTone(BUZZER_PIN);
  }
}


// ============================================================
// Button handling
// ============================================================

void handleButton() {

  bool currentButtonState = digitalRead(BUTTON_PIN);

  // Detect the transition from released to pressed.
  if (
    currentButtonState == LOW &&
    lastButtonState == HIGH &&
    millis() - lastDebounceTime >= DEBOUNCE_DELAY
  ) {

    // Toggle the monitoring system.
    monitoringEnabled = !monitoringEnabled;

    lastDebounceTime = millis();
  }

  lastButtonState = currentButtonState;
}


// ============================================================
// Serial input from Python
// ============================================================

void readSerialInput() {

  if (Serial.available() > 0) {

    // The Python interface sends a value between 0 and 255.
    int receivedValue = Serial.parseInt();

    if (
      receivedValue >= 0 &&
      receivedValue <= 255
    ) {

      ledIntensity = receivedValue;
    }
  }
}


// ============================================================
// Air quality monitoring
// ============================================================

void monitorAirQuality() {

  // Limit how often the sensor is read.
  if (
    millis() - lastSensorRead < SENSOR_INTERVAL
  ) {
    return;
  }

  lastSensorRead = millis();

  // Read the analog output of the MQ-135 sensor.
  sensorValue = analogRead(SENSOR_PIN);

  // Send the sensor value to the Python application.
  Serial.println(sensorValue);


  // ----------------------------------------------------------
  // Alert condition
  // ----------------------------------------------------------

  if (
    sensorValue >= GAS_THRESHOLD_LOW &&
    sensorValue < GAS_THRESHOLD_HIGH
  ) {

    // Turn on the LED using the intensity configured
    // from the Python interface.
    analogWrite(
      LED_PIN,
      ledIntensity
    );

    // Generate an audible alert.
    tone(
      BUZZER_PIN,
      225,
      2000
    );

  } else {

    // No alert condition.
    analogWrite(
      LED_PIN,
      0
    );

    noTone(
      BUZZER_PIN
    );
  }
}