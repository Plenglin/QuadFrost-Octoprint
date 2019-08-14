import pyserial

MODE_LAMP = 1
MODE_HUE = 2

class EmptyMode:
    def __init__(self, parent):
        self.parent = parent

class LampMode:
    def __init__(self, parent):
        self.parent = parent

    def set_color(self, r, g, b):
        self.ser.write(0x81)
        self.ser.write(r)
        self.ser.write(g)
        self.ser.write(b)

class HueMode:
    def __init__(self, parent):
        self.parent = parent

    def set_hue_range(self, hue_start, hue_end):
        self.ser.write(0x81)
        self.ser.write(hue_start)
        self.ser.write(0x82)
        self.ser.write(hue_end)

    def set_rate(self, step, period):
        self.ser.write(0x83)
        self.ser.write(step)
        self.ser.write(0x86)
        self.ser.write(period)

    def set_sat_val(self, sat, val):
        self.ser.write(0x84)
        self.ser.write(sat)
        self.ser.write(0x85)
        self.ser.write(val)

class QuadFrost:
    def __init__(self, port, baudrate=19200):
        self.ser = pyserial.Serial(port, baudrate=baudrate)
        self.modes = [
            EmptyMode(),
            LampMode(self),
            HueMode(self)
        ]
    
    def _read_response(self):
        cmd = self.ser.read()[0]
        size = self.ser.read()[0]
        data = self.ser.read(size)
        return cmd, data

    def set_mode(self, mode_i):
        mode = self.modes[mode_i]
        self.ser.write(0x01)
        self.ser.write(mode_i)
        return mode
