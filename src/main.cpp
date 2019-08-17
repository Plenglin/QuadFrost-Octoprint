#include <Arduino.h>
#include <Wire.h>

#include <FastLED.h>
#include <LiquidCrystal_PCF8574.h>

#include "constants.hpp"
#include "mode/hue.hpp"
#include "mode/lamp.hpp"

#define COMM_BAUD 19200
#define LED_COUNT 16
#define MODES_COUNT 3

using namespace quadfrost;

CRGB leds[LED_COUNT];
Mode* modes[MODES_COUNT] = {
  new Mode(),
  new LampMode<LED_COUNT>(leds),
  new HueMode<LED_COUNT>(leds)
};
Mode* mode = modes[0];

LiquidCrystal_PCF8574 lcd(0x3f);

void setup() {
  FastLED.addLeds<WS2812B, pins::LED_PIN, BRG>(leds, LED_COUNT);
  pinMode(pins::FILTER_PIN, OUTPUT);
  pinMode(pins::DOOR_SWITCH_PIN, INPUT_PULLUP);
  
  lcd.begin(16, 2);
  lcd.setBacklight(1);

  analogWrite(pins::FILTER_PIN, 0);
  fill_solid(leds, LED_COUNT, CRGB::Black);
  FastLED.show();

  Serial.begin(COMM_BAUD);
  Serial.write(events::READY);
}

bool switch_mode(unsigned char target_mode) {
  if (target_mode <= MODES_COUNT) {
    mode->end();
    mode = modes[target_mode];
    mode->begin();
    return true;
  }
  return false;
}

void execute_command(char command) {
  if ((command & 0x80) != 0) {
    mode->on_command(command);
  } else {
    switch (command) {
      case commands::SET_MODE: {
        int mode = Serial.read();
        bool success = switch_mode(mode);
        Serial.write(1);
        Serial.write(success);
        break;
      }
      case commands::SET_LCD_BACKLIGHT: {
        bool state = Serial.read();
        lcd.setBacklight(state);
        Serial.write(1);
        Serial.write((char)state);
        break;
      }
      case commands::SET_FILTER: {
        int power = Serial.read();
        analogWrite(pins::FILTER_PIN, power);
        Serial.write(1);
        Serial.write(power);
        break;
      }
      default:
        break;
    }
  }
}

void read_commands() {
  if (Serial.available() > 0) {
    delay(10);
    while (Serial.available() > 0) {
      char command = Serial.read();
      Serial.write(events::ACK);
      Serial.write(command);
      execute_command(command);
    }
  }
}

/**
 * Returns the result in degrees C.
 */
int get_temperature() {
  long x = analogRead(pins::TEMPERATURE_PIN);
  x *= 500;
  x /= 1024;
  x -= 50;
  return x;
}

static unsigned long last_loop_time = 0;
AdaptiveSleeper sleeper(50000);

void loop() {
  unsigned long current_loop_time = millis();
  unsigned long delta = millis() - last_loop_time;
  last_loop_time = current_loop_time;

  read_commands();

  sleeper.target_sleep = mode->loop(delta) * 1000;

  lcd.setCursor(0, 0);
  lcd.print(String(digitalRead(pins::DOOR_SWITCH_PIN)));
  lcd.setCursor(0, 1);
  lcd.print(String(get_temperature()));
  lcd.print((char)0xdf);
  lcd.print("C");

  sleeper.sleep(delta);
}

