import serial
import time

ser = serial.Serial("COM4", baudrate=19200, timeout=3)
assert ser.isOpen()
print(ser.read())
ser.write(b'\x01\x01\x81\xff\x00\x00')
res = ser.read(9)
print([hex(c) for c in res])
ser.close()
