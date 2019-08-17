import serial
import time

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
print([hex(c) for c in read_ack(ser)])

ser.write(b'\x01\x02')  # Mode 2
print([hex(c) for c in read_ack(ser)])

ser.write(b'\x81\xff')  # Start hue 255
print([hex(c) for c in read_ack(ser)])

ser.write(b'\x82\x80')  # End hue 128
print([hex(c) for c in read_ack(ser)])

ser.write(b'\x83\x05')  # Step hue
print([hex(c) for c in read_ack(ser)])

ser.write(b'\x86\x00\x10')  # Period
print([hex(c) for c in read_ack(ser)])

ser.close()
