#include <Arduino.h>
#include <FastLED.h>

#include "mode/lamp.hpp"
#include "mode/hue.hpp"
#include "protocol.hpp"

#define COMM_BAUD 19200
#define LED_COUNT 16
#define LED_PIN 8
#define FILTER_PIN 9
#define TEMPERATURE_PIN A0
#define MODES_COUNT 3

using namespace quadfrost;

CRGB leds[LED_COUNT];
Mode* modes[MODES_COUNT] = {
  new Mode(),
  new LampMode<LED_COUNT>(leds),
  new HueMode<LED_COUNT>(leds)
};
Mode* mode = modes[0];

void setup() {
  Serial.begin(COMM_BAUD);
  FastLED.addLeds<WS2812B, LED_PIN, BRG>(leds, LED_COUNT);
  fill_solid(leds, LED_COUNT, CRGB::Black);
  FastLED.show();
  analogWrite(FILTER_PIN, 0);
  Serial.write(events::READY);
  pinMode(13, OUTPUT);
  //pinMode(FILTER_PIN, OUTPUT);
  digitalWrite(13, LOW);
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

void read_commands() {
  char command = Serial.read();
  if (command != -1) {
    delay(10);
    Serial.write(events::ACK);
    Serial.write(command);

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
        case commands::SET_FILTER: {
          int power = Serial.read();
          analogWrite(FILTER_PIN, power);
          Serial.write(1);
          Serial.write(power);
          break;
        }
        default:
          break;
      }
    }
  }
}

static unsigned long last_loop_time = 0;

void loop() {
  unsigned long current_loop_time = millis();
  unsigned long delta = millis() - last_loop_time;
  read_commands();
  mode->loop(delta);
  last_loop_time = current_loop_time;
}
