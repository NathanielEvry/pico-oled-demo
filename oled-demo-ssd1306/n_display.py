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

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

i2c = I2C(0, scl=Pin(1), sda=Pin(0))
time.sleep(0.1)  # wait for i2x to fully init
# oled = SSD1306_I2C(128, 32, i2c)  # Init oled display
oled = SSD1306_I2C(128, 64, i2c)  # Alternate 128 x 64 OLED

x = 0
y = 10

print(" demo status OK")

while True:
    oled.fill(0)
    # Upper banner
    # oled.text("1234567-7654321", 8, 8)
    oled.text("     title", 8, 0)

    # oled.text(f'x is {x} y is {y}', x, y)
    oled.text(f"x is {x} y is {y}", 10, 20)
    oled.hline(x, x, y, 1)

    pix = 0
    while pix < 100:
        oled.pixel(pix, y, 1)
        pix += 1

    oled.show()
    time.sleep(0.01)
    if x >= 128:
        x = 0
        y += 4
    if y >= 30:
        y = 10
    x += 3
