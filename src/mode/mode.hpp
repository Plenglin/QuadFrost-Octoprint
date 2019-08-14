#pragma once

namespace quadfrost {

  class Mode {
  public:
    virtual void begin() {};
    virtual void loop(int delta) {};
    virtual void on_command(char command) {};
    virtual void end() {};
  };

}
