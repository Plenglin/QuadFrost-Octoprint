#pragma once

#include <Arduino.h>

namespace quadfrost {

  class Mode {
  public:
    virtual void begin() {};
    virtual unsigned int loop(int delta) {
      return 50;
    };
    virtual void on_command(char command) {};
    virtual void end() {};
  };

}
