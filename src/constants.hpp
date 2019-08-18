#pragma once
#include <Arduino.h>

namespace quadfrost {
  namespace pins {
    const int LED_PIN = 8;
    const int FILTER_PIN = 9;
    const int TEMPERATURE_PIN = A0;
    const int DOOR_SWITCH_PIN = A1;
  }
  
  namespace commands {
    const char SET_LED_MODE = 0x01;
    const char SET_LCD_BACKLIGHT = 0x02;
    const char SET_FILTER = 0x03;
    const char SET_PROGRESS = 0x04;
    const char SET_PRINTER_STATUS = 0x05;

    /** 0x80-0xff are reserved for modes to use */
  } 

  namespace events {
    const char READY = 0x00;
    const char ACK = 0x01;
    const char TEMPERATURE = 0x11;
    const char USER_INPUT = 0x12;
  }
}