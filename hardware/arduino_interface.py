#Manages serial communication (pyserial) between Pi and Arduino Nano
# hardware/arduino_interface.py
import serial
import time

class ArduinoInterface:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600, timeout=1):
        try:
            self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
            time.sleep(2)  # Give time for Arduino to reset
            print(f"Connected to Arduino on {port} at {baudrate} baud")
        except serial.SerialException as e:
            print(f"[ERROR] Could not open serial port: {e}")
            self.ser = None

    def send_command(self, command):
        """Send a string command to the Arduino."""
        if self.ser and self.ser.is_open:
            cmd = (command + '\n').encode('utf-8')
            self.ser.write(cmd)
            print(f"[TX] {command}")

    def read_response(self):
        """Read a response line from Arduino (non-blocking)."""
        if self.ser and self.ser.in_waiting:
            response = self.ser.readline().decode('utf-8').strip()
            print(f"[RX] {response}")
            return response
        return None

    def close(self):
        if self.ser:
            self.ser.close()
            print("Serial connection closed")

# Usage example:
if __name__ == "__main__":
    arduino = ArduinoInterface(port='/dev/ttyUSB0')
    arduino.send_command("PING")
    time.sleep(1)
    arduino.read_response()
    arduino.close()