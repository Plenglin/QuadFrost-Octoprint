import serial
import struct
import logging
import time


_logger = logging.getLogger(__name__)

MODE_EMPTY = 0
MODE_LAMP = 1
MODE_HUE = 2
MODE_DIRECTION = 3


class EmptyMode:
    pass


class LampMode:
    def __init__(self, parent):
        self.parent = parent
        self.ser = parent.ser

    def set_color(self, r, g, b):
        self.ser.write('\x80')
        self.ser.write(struct.pack('>BBB', r, g, b))
        self.parent.read_response()
        return self


class HueMode:
    def __init__(self, parent):
        self.parent = parent
        self.ser = parent.ser
    
    def set_hue_range(self, hue_start, hue_end):
        self.ser.write('\x81')
        self.ser.write(chr(hue_start))
        self.ser.write('\x82')
        self.ser.write(chr(hue_end))
        self.parent.read_response()
        return self

    def set_rate(self, step, period):
        self.ser.write('\x83')
        self.ser.write(chr(step))
        self.ser.write('\x80')
        self.ser.write(struct.pack('>H', period))
        self.parent.read_response()
        return self

    def set_sat_val(self, sat, val):
        self.ser.write('\x84')
        self.ser.write(chr(sat))
        self.ser.write('\x85')
        self.ser.write(chr(val))
        self.parent.read_response()
        return self


class DirectionMode:
    def __init__(self, parent):
        self.parent = parent
        self.ser = parent.ser

    def enable_direction(self, pos):
        if pos is None:
            self.ser.write('\x80\x00')
        else:
            self.ser.write('\x80\x01\x81')
            self.ser.write(struct.pack('>h', pos))
        self.parent.read_response()
        return self

    def set_on_color(self, r, g, b):
        self.ser.write('\x82')
        self.ser.write(struct.pack('>BBB', r, g, b))
        self.parent.read_response()
        return self

    def set_off_color(self, r, g, b):
        self.ser.write('\x83')
        self.ser.write(struct.pack('>BBB', r, g, b))
        self.parent.read_response()
        return self

class ConnectionFailedError(Exception):
    pass

class QuadFrost:
    def __init__(self, port, baudrate=19200):
        _logger.info("Opening on %s baud=%s", port, baudrate)
        self.ser = serial.Serial(port, baudrate=baudrate, timeout=10)
        
        self.modes = [
            EmptyMode(),
            LampMode(self),
            HueMode(self),
            DirectionMode(self)
        ]
        self.set_mode(MODE_EMPTY)
        self.set_status(1)
        self.set_filter(0)
        self.set_progress(0)
    
    def read_response(self):
        ev = ord(self.ser.read())
        if ev != 0x01:
            return None
        cmd = ord(self.ser.read())
        size = ord(self.ser.read())
        return cmd, [ord(i) for i in self.ser.read(size)]

    def set_mode(self, mode_i):
        self.mode = self.modes[mode_i]
        self.ser.write('\x01')
        self.ser.write(chr(mode_i))
        self.read_response()
        _logger.debug("Mode changed: i=%s, %s", mode_i, self.mode)
        return self.mode
    
    def set_empty_mode(self):
        return self.set_mode(MODE_EMPTY)
    
    def set_lamp_mode(self):
        return self.set_mode(MODE_LAMP)
    
    def set_hue_mode(self):
        return self.set_mode(MODE_HUE)
    
    def set_direction_mode(self):
        return self.set_mode(MODE_DIRECTION)
    
    def set_status(self, status_i):
        self.ser.write('\x05')
        self.ser.write(chr(status_i))
        self.read_response()
        return self
    
    def set_progress(self, progress):
        self.ser.write('\x04')
        self.ser.write(chr(progress))
        self.read_response()
        return self
    
    def get_mode(self):
        return self.mode

    def set_filter(self, power):
        self.ser.write('\x03')
        self.ser.write(chr(power))
        self.read_response()
        return self

    def set_lcd_backlight(self, state):
        self.ser.write('\x02')
        self.ser.write('\x01' if state else '\x00')
        self.read_response()
        return self

    def close(self):
        if self.ser.isOpen():
            _logger.info("Closing")
            try:
                self.set_status(0)
            except Exception as e:
                _logger.warn("Failure while attempting to reset status")
                _logger.warn(e)
            finally:
                self.ser.close()
        else:
            _logger.warn("Failed to close: already disconnected")
