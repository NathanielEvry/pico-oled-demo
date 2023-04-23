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


def bootlogo():
    print("running bootlogo")

    ### Effect
    # word    word    word   ->#
    # --------------------------#
    # <- word    word    word  #
    # word    word    word   ->#
    # <- word    word    word  #
    #                          #

    msg = "word    word    word    word    word    word    word    word    word    word    word    word    word    word    word    word    word    word    word    word    word"
    x = SCREEN_WIDTH + 10
    y = 0

    x2 = -1000
    x3 = SCREEN_WIDTH + 10 + 100
    x4 = -1100

    timeOfwordScroll = 5.00

    while x > SCREEN_WIDTH * -timeOfwordScroll:
        oled.fill(0)
        oled.text(msg, x, y)
        oled.text(msg, x2, y + 17)
        oled.text(msg, x3, y + 34)
        oled.text(msg, x4, y + 51)

        oled.show()
        utime.sleep_ms(50)
        x -= 5
        x2 += 5
        x3 -= 5
        x4 += 5

    print("bootlogo complete")


bootlogo()
