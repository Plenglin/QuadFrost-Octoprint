import serial
import time

ser = serial.Serial("COM4", baudrate=19200, timeout=3)
assert ser.isOpen()

def read_ack(ser):
    if ser.read() != b'\x01':
        return None
    cmd = ser.read()
    size = ser.read()
    return cmd + ser.read(size[0])

print(ser.read())

ser.write(b'\x01\x01')
print([hex(c) for c in read_ack(ser)])

ser.write(b'\x81\xff\x00\x00')
print([hex(c) for c in read_ack(ser)])

ser.write(b'\x03\xff')
print([hex(c) for c in read_ack(ser)])

time.sleep(3)

ser.write(b'\x03\x00')
print([hex(c) for c in read_ack(ser)])

ser.close()
