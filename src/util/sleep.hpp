#pragma once

#include <Arduino.h>

namespace quadfrost {
  class AdaptiveSleeper {
    int next_sleep;
  public:
    int target_sleep;
    AdaptiveSleeper(int target_sleep)
        : next_sleep(target_sleep), target_sleep(target_sleep) {}

    void sleep(long actual_period) {
      int error = target_sleep - actual_period;
      if (error > 0 || next_sleep > 0) {
        next_sleep += error;
      }
      if (next_sleep > 0) {
        delayMicroseconds(next_sleep);
      }
    }
  };
}