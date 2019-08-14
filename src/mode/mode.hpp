#pragma once

#include <Arduino.h>

namespace quadfrost {

  class Mode {
  public:
    virtual void begin() {};
    virtual void loop(int delta) {
      delay(50);
    };
    virtual void on_command(char command) {};
    virtual void end() {};
  };

}
