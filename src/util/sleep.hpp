#pragma once

#include <Arduino.h>

namespace quadfrost {
  template <int compensation_rate = 1>
  class AdaptiveSleeper {
    int next_sleep;
  public:
    int target_sleep;
    AdaptiveSleeper(int target_sleep)
        : next_sleep(target_sleep), target_sleep(target_sleep) {}

    void sleep(unsigned long actual_period) {
      int error = target_sleep - actual_period;
      next_sleep += compensation_rate * error;
      delay(next_sleep);
    }
  };
}