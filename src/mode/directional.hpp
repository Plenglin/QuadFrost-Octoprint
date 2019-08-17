#pragma once

#include <Arduino.h>
#include <FastLED.h>

#include "util.hpp"
#include "mode.hpp"

namespace quadfrost {
  template <int count>
  class DirectionalMode : public Mode {
  private:
    CRGB* leds;
    CRGB color_off = CRGB::Red;
    CRGB color_on = CRGB::Blue;

    bool enabled = false;
    unsigned int position = 0;

    void render() {
      position = position % count;
      fill_solid(leds, count, color_off);
      if (enabled) {
        leds[position] = color_on;
      }
      FastLED.show();
    }
  public:
    static const char ENABLE_DIRECTION = 0x80;
    static const char SET_DIRECTION = 0x81;
    static const char SET_COLOR_ON = 0x82;
    static const char SET_COLOR_OFF = 0x83;

    DirectionalMode(CRGB* leds) : leds(leds) {}
    
    void on_command(char command) override {
      switch (command) {
        case ENABLE_DIRECTION:
          enabled = (bool) Serial.read();
          acknowledge(command, (char) enabled);
          render();
          break;
        case SET_DIRECTION: {
          int high = Serial.read();
          int low = Serial.read();
          position = (high << 4) | low;
          acknowledge(command, (int) position);
          render();
          break;
        }
      }
    }
  };
}
