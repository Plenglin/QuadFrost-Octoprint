import serial
import time
import struct

ser = serial.Serial("COM3", baudrate=19200, timeout=3)
assert ser.isOpen()

def read_ack(ser):
    if ser.read() != b'\x01':
        return None
    cmd = ser.read()
    size = ser.read()
    return cmd + ser.read(size[0])

print(ser.read())

ser.write(b'\x02\x01')  # Enable backlight

ser.write(b'\x01\x01')  # Mode 1
ser.write(b'\x80')
ser.write(struct.pack('>BBB', 255, 255, 255))
ser.write(b'\x05\x07')
ser.write('\x04\x00')

for i in range(100):
    ser.write(b'\x04')  # Set progress
    ser.write(chr(i))
    time.sleep(0.05)

ser.close()
