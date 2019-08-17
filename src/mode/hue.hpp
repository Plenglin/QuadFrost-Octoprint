#pragma once

#include "FastLED.h"
#include "mode.hpp"
#include "util/sleep.hpp"

namespace quadfrost {
  template <int count>
  class HueMode : public Mode {
    CRGB* leds;
    byte hue_start = 0;
    byte hue_end = 64;
    byte hue_step = 1;
    byte sat = 255;
    byte val = 255;
    unsigned int period = 50;
  public:
    static const char SET_HUE_START = 0x81;
    static const char SET_HUE_END = 0x82;
    static const char SET_HUE_STEP = 0x83;
    static const char SET_SAT = 0x84;
    static const char SET_VAL = 0x85;
    static const char SET_PERIOD = 0x86;

    HueMode(CRGB* leds) : leds(leds) {}

    unsigned int loop(int delta) override {
      hue_start += hue_step;
      hue_end += hue_step;
      fill_gradient(leds, 0, CHSV(hue_start, sat, val), count - 1, CHSV(hue_end, sat, val), FORWARD_HUES);
      FastLED.show();
      return period;
    }

    void on_command(char command) override {
      switch (command) {
      case SET_HUE_START:
        hue_start = Serial.read();
        Serial.write(1);
        Serial.write(hue_start);
        break;
      case SET_HUE_END:
        hue_end = Serial.read();
        Serial.write(1);
        Serial.write(hue_end);
        break;
      case SET_HUE_STEP:
        hue_step = Serial.read();
        Serial.write(1);
        Serial.write(hue_step);
        break;
      case SET_PERIOD: {
        int high = Serial.read();
        int low = Serial.read();
        period = (high << 4) | low;
        Serial.write(2);
        Serial.write(high);
        Serial.write(low);
        break;
      }
      case SET_SAT:
        sat = Serial.read();
        Serial.write(1);
        Serial.write(sat);
        break;
      case SET_VAL:
        val = Serial.read();
        Serial.write(1);
        Serial.write(val);
        break;
      default:
        break;
      }
    }
  };
}