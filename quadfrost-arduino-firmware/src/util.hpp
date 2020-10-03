#pragma once

#include <Arduino.h>

#include "constants.hpp"

namespace quadfrost {
  void acknowledge(char cmd, char* data, int length) {
    Serial.write(events::ACK);
    Serial.write(cmd);
    Serial.write(length);
    for (int i = 0; i < length; i++) {
      Serial.write(data[i]);
    }
  }

  void acknowledge(char cmd, char data) {
    acknowledge(cmd, reinterpret_cast<char*>(&data), 1);
  }

  void acknowledge(char cmd, int data) {
    char buf[2] = {(char) ((data & 0xff00) >> 8), (char) (data & 0xff)};
    acknowledge(cmd, buf, 2);
  }

  CRGB read_color(byte buf[3]) {
    buf[0] = Serial.read();
    buf[1] = Serial.read();
    buf[2] = Serial.read();
    return CRGB(buf[0], buf[1], buf[2]);
  }

  class AdaptiveSleeper {
    long next_sleep;

  public:
    long target_sleep;
    AdaptiveSleeper(long target_sleep)
      : next_sleep(target_sleep)
      , target_sleep(target_sleep)
    {}

    void sleep(long actual_period) {
      long error = target_sleep - actual_period;
      if (error > 0 || next_sleep > 0) {
        next_sleep += error;
      }
      if (next_sleep > 0) {
        delayMicroseconds(next_sleep);
      }
    }
  };

  class RunEvery {
    long msTotal;
    long msLeft;
    void (*func)();
  public:
    RunEvery(long ms, void (*func)())
      : msTotal(ms)
      , msLeft(ms)
      , func(func)
    {}
    void update(long delta) {
      msLeft -= delta;
      if (msLeft < 0) {
        (*func)();
        while (msLeft < 0) {
          msLeft += msTotal;
        }
      }
    }
  };
}