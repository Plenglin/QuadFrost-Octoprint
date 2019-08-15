import serial


MODE_LAMP = 1
MODE_HUE = 2


class EmptyMode:
    def __init__(self, parent):
        self.parent = parent


class LampMode:
    def __init__(self, parent):
        self.parent = parent

    def set_color(self, r, g, b):
        self.parent.ser.write('\x81')
        self.parent.ser.write(chr(r))
        self.parent.ser.write(chr(g))
        self.parent.ser.write(chr(b))


class HueMode:
    def __init__(self, parent):
        self.parent = parent

    def set_hue_range(self, hue_start, hue_end):
        self.parent.ser.write('\x81')
        self.parent.ser.write(chr(hue_start))
        self.parent.ser.write('\x82')
        self.parent.ser.write(chr(hue_end))

    def set_rate(self, step, period):
        self.parent.ser.write('\x83')
        self.parent.ser.write(chr(step))
        self.parent.ser.write('\x86')
        self.parent.ser.write(chr(period))

    def set_sat_val(self, sat, val):
        self.parent.ser.write('\x84')
        self.parent.ser.write(chr(sat))
        self.parent.ser.write('\x85')
        self.parent.ser.write(chr(val))


class QuadFrost:
    def __init__(self, port, baudrate=19200):
        self.ser = serial.Serial(port, baudrate=baudrate)
        self.modes = [
            EmptyMode(self),
            LampMode(self),
            HueMode(self)
        ]
    
    def read_response(self):
        ev = ord(ser.read())
        if ev != 0x01:
            return None
        cmd = ord(ser.read())
        size = ord(ser.read())
        return cmd, [ord(i) for i in ser.read(size)]

    def set_mode(self, mode_i):
        mode = self.modes[mode_i]
        self.ser.write('\x01')
        self.ser.write(chr(mode_i))
        return mode

    def close(self):
        self.ser.close()
