import serial
import time

class SerialConnection:
    _instance = None  # Singleton instance

    def __new__(cls, port="COM6", baudrate=4800, timeout=1):
        if cls._instance is None:
            cls._instance = super(SerialConnection, cls).__new__(cls)
            cls._instance.initialize(port, baudrate, timeout)
        return cls._instance

    def initialize(self, port, baudrate, timeout):
        self.ser = None
        retries = 3
        while retries > 0:
            try:
                self.ser = serial.Serial(port, baudrate, timeout=timeout)
                time.sleep(2)  # Allow Arduino time to stabilize
                print("Connected to Arduino.")
                break
            except serial.SerialException as e:
                print(f"Serial error: {e}")
                retries -= 1
                time.sleep(2)
            except PermissionError as e:
                print(f"Permission error: {e} - Ensure no other process is using {port}")
                break  # Stop retrying if it's a permission issue

    def read_lines(self, num_lines=3):
        if not self.ser:
            return {"error": "No serial connection."}

        data = []
        for _ in range(num_lines):
            try:
                line = self.ser.readline().decode("utf-8").strip()
                if line:
                    print(f"Received line: {line}")  # Log each line received
                    data.append(line)
            except serial.SerialException as e:
                print(f"Error reading serial data: {e}")

        return data

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Serial connection closed.")




















# import serial
# import time
# import serial.tools.list_ports

# class SerialConnection:
#     _instance = None

#     def __new__(cls, port, baudrate, timeout):
#         if cls._instance is None:
#             cls._instance = super(SerialConnection, cls).__new__(cls)
#             cls._instance.initialize(port, baudrate, timeout)
#         return cls._instance

#     def initialize(self, port, baudrate, timeout):
#         self.port = port
#         self.baudrate = baudrate
#         self.timeout = timeout
#         self.ser = None
#         self.initialize_serial()

#     def initialize_serial(self):
#         retries = 3
#         while retries > 0:
#             try:
#                 available_ports = [p.device for p in serial.tools.list_ports.comports()]
#                 if self.port not in available_ports:
#                     print(f"Port {self.port} not available. Available ports: {available_ports}")
#                     return

#                 self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
#                 time.sleep(5)  # Allow Arduino to initialize
#                 print(f"Connected to {self.port} at {self.baudrate} baud.")
#                 break
#             except serial.SerialException as e:
#                 print(f"Serial error: {e}")
#                 retries -= 1
#                 time.sleep(2)
#             except PermissionError as e:
#                 print(f"Permission error: {e} - Ensure no other process is using {self.port}")
#                 break  # Stop retrying if it's a permission issue
#         else:
#             print("Failed to connect after multiple attempts.")

#     def read_lines(self, num_lines=3):
#         if not self.ser or not self.ser.is_open:
#             return {"error": "No serial connection."}

#         data = []
#         for _ in range(num_lines):
#             try:
#                 line = self.ser.readline().decode("utf-8").strip()
#                 if line:
#                     print(f"Received line: {line}")  # Log each line received
#                     data.append(line)
#             except serial.SerialException as e:
#                 print(f"Error reading serial data: {e}")
#                 break
#         return data

#     def close(self):
#         if self.ser and self.ser.is_open:
#             self.ser.close()
#             print("Serial connection closed.")
