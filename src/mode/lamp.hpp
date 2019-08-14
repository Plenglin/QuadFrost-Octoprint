#pragma once

#include "FastLED.h"
#include "mode.hpp"

namespace quadfrost {

  template<int count>
  class LampMode : public Mode {
    CRGB* leds;
    void write_color(CRGB color) {
      fill_solid(leds, count, color);
      FastLED.show();
    }
  public:
    const static char SET_COLOR = 0x81;

    LampMode(CRGB* leds) : leds(leds) {}

    void on_command(char command) override {
      switch (command) {
        case SET_COLOR: {
          byte r = Serial.read();
          byte g = Serial.read();
          byte b = Serial.read();
          auto color = CRGB(r, g, b);
          write_color(color);
          Serial.write(color.r);
          Serial.write(color.g);
          Serial.write(color.b);
          break;
        }
      }
    }
  };
}