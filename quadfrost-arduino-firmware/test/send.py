import serial
import time
import struct
import quadfrost

qf = quadfrost.QuadFrost('COM3')

qf.set_status(2).set_progress(0).set_hue_mode().set_rate(1, 10).set_sat_val(100, 192).set_hue_range(0, 192)

qf.close()
