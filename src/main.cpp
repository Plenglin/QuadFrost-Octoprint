#include <Arduino.h>
#include <FastLED.h>

#include "protocol.hpp"
#include "mode/lamp.hpp"

#define COMM_BAUD 19200
#define LED_COUNT 16
#define LED_PIN 8
#define FILTER_PIN 9
#define TEMPERATURE_PIN A0
#define MODES_COUNT 2

using namespace quadfrost;

CRGB leds[LED_COUNT];
Mode* modes[MODES_COUNT] = {
  new Mode(),
  new LampMode<LED_COUNT>(leds)
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
  digitalWrite(13, LOW);
}

void switch_mode(unsigned char target_mode) {
  if (target_mode <= MODES_COUNT) {
    mode = modes[target_mode];
  }
}

void read_commands() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    delay(10);
    digitalWrite(13, HIGH);
    Serial.write(events::ACK);
    Serial.write(command);

    if ((command & 0x80) != 0) {
      mode->on_command(command);
    } else {
      switch (command) {
        case commands::SET_MODE: {
          int mode = Serial.read();
          switch_mode(mode);
          Serial.write(mode);
          break;
        }
        case commands::FILTER_ON:
          analogWrite(FILTER_PIN, 200);
        case commands::FILTER_OFF:
          analogWrite(FILTER_PIN, 0);
        default:
          break;
      }
    }
  }
}

void loop() {
  read_commands();
  delay(1000);
}
