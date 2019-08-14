#pragma once

namespace quadfrost {
  namespace commands {
    const char SET_MODE = 0x01;
    const char SET_FILTER = 0x03;

    /** 0x80-0xff are reserved for modes to use */
  }

  namespace events {
    const char READY = 0x00;
    const char ACK = 0x01;
    const char TEMPERATURE = 0x11;
    const char USER_INPUT = 0x12;
  }
}
