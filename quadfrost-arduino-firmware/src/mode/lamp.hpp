#pragma once

#include "FastLED.h"
#include "mode.hpp"
#include "util.hpp"

namespace quadfrost {

  template<int count>
  class LampMode : public Mode {
    CRGB* leds;
    void render(CRGB color) {
      fill_solid(leds, count, color);
      FastLED.show();
    }
  public:
    const static char SET_COLOR = 0x80;

    LampMode(CRGB* leds) : leds(leds) {}

    void on_command(char command) override {
      switch (command) {
        case SET_COLOR: {
          byte data[3];
          render(read_color(data));
          acknowledge(command, reinterpret_cast<char*>(data), 3);
          break;
        }
      }
    }
  };
}