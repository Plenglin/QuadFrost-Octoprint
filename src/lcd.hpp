#pragma once

#include <LiquidCrystal_PCF8574.h>


namespace quadfrost {
  static const String DISPLAY_STATUS_NAMES[] = {
    "No Signal",
    "Ready    ",
    "Printing ",
    "Cancelled",
    "Error    ",
    "Complete ",
    "Paused   ",
    "No Device"
  };

  class StatusDisplay {
    LiquidCrystal_PCF8574 lcd;
  public:
    StatusDisplay(LiquidCrystal_PCF8574 lcd) : lcd(lcd) {}

    void begin() {
      lcd.begin(16, 2);
      lcd.clear();
      lcd.setBacklight(true);
      set_status(0);
      set_progress(0);
    }

    void set_temperature(int temperature) {
      auto str = String(temperature);
      lcd.setCursor(14 - str.length(), 0);
      lcd.print(str);
      lcd.print((char)0xdf);
      lcd.print("C");
    }
    
    void set_status(int mode) {
      lcd.setCursor(0, 0);
      lcd.print(DISPLAY_STATUS_NAMES[mode]);
    }

    void set_backlight(bool state) {
      lcd.setBacklight(state);
    }

    void set_progress(int progress) {
      progress = min(max(progress, 0), 99);

      lcd.setCursor(0, 1);
      lcd.print("[");
      int ticks = (progress + 5) / 10;
      for (int i = 1; i <= 10; i++) {
        if (i <= ticks) {
          lcd.write((char) 0xff);
        } else {
          lcd.print(" ");
        }
      }
      lcd.print("]");

      auto str = String(progress);
      lcd.setCursor(15 - str.length(), 1);
      lcd.print(str);
      lcd.print("%");
    }
  };
}
