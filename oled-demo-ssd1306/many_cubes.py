# Pico OLED Demo
#
# This project is a demo of using the RP2040 Pi Pico and a SSD1306 OLED display with Micropython.
# It demos creating and moving rectangles on the screen!
#
# Created by Nathaniel Evry @NathanielEvry on 2023-04-22
# My GitHub: https://github.com/altometer
# GitHub Project Repo: https://github.com/altometer/pico-oled-demo
#
# Web-hosted Pico2040 simulator for this project:
# https://wokwi.com/projects/362799539846585345

import random
import math
import utime
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C

SCREEN_HEIGHT = 128
SCREEN_WIDTH = 64

i2c = I2C(0, scl=Pin(1), sda=Pin(0))
utime.sleep_ms(50)  # delay to setup screen
oled = SSD1306_I2C(SCREEN_HEIGHT, SCREEN_WIDTH, i2c)


def sleep(s: int = 0):
    # I'm lazy and I want my own sleep in seconds call.
    print(f"sleeping for {s} seconds...")
    utime.sleep_ms(s * 1000)


print("starting script - making many squares")
oled.fill(0)


class Card:
    def __init__(self, coordinates=(0, 16), size=16) -> None:
        self.position = coordinates
        self.hp = size * 5
        self.metabolism = 3

    def wander(self):
        x = self.metabolism * (random.random() + 1) / 8
        y = self.metabolism * (random.random() + 1)
        return x, y

    def step(self):
        dpos = self.wander()
        self.hp -= self.metabolism * 0.15
        self.move(dpos)

    def move(self, dpos):
        self.position = self.position[0] + dpos[0], self.position[0] + dpos[1]

    def draw(self):
        x, y = self.position
        x = round(x)
        y = round(y)
        size = math.ceil(self.hp / 5)
        oled.rect(x, y, size, size, 1)
        oled.fill_rect(x + 1, y + 1, size - 2, size - 2, 0)


deck = []

while True:
    oled.fill(0)
    if random.random() >= 0.97:
        oled.fill_rect(0, 0, 16, 16, 1)  # topleft start position cube
        r1 = Card()
        deck.append(r1)
    else:
        oled.fill_rect(0, 0, 16, 16, 0)  # topleft start position cube

    for box in deck:
        if box.hp <= 0.1:
            deck.remove(box)
        box.step()
        box.draw()

    oled.rect(0, 0, 16, 16, 1)  # topleft start position cube
    # utime.sleep_ms(100)
    oled.show()
