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

SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64

i2c = I2C(0, scl=Pin(1), sda=Pin(0))
utime.sleep_ms(50)  # delay to setup screen
oled = SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c)


def sleep(s: int = 0):
    # I'm lazy and I want my own sleep in seconds call.
    print(f"sleeping for {s} seconds...")
    utime.sleep_ms(s * 1000)


sleep(1)


def screen_center():
    return SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2


def shape_offset(height, width):
    center = screen_center()
    h2 = height / 4
    w2 = width / 4
    return (
        center[0] - w2,
        center[1] - h2,
    )


def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    sin_angle = math.sin(angle)
    cos_angle = math.cos(angle)

    qx = ox + cos_angle * (px - ox) - sin_angle * (py - oy)
    qy = oy + sin_angle * (px - ox) + cos_angle * (py - oy)
    return qx, qy


square_size = 16
radius = int(square_size / 2)
source_points = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
# print(f"source:{source_points}")
newxy = []

offset_x, offset_y = shape_offset(square_size, square_size)
# offset_x, offset_y = screen_center()
# print(f"radius:{radius},offset_x:{offset_x},offset_y{offset_y}")

# scale up to radius
for xy in source_points:
    x, y = xy
    x = x * radius
    y = y * radius
    newxy.append((x, y))

for xy in source_points:
    x, y = xy
    x = x * radius + 10
    y = y * radius + 5
    newxy.append((x, y))


center_point = screen_center()
angle = 0.05
while True:
    oled.fill(0)
    curxy = newxy

    # 4 lines, for a square
    lines = [
        (curxy[0], curxy[1]),
        (curxy[1], curxy[2]),
        (curxy[2], curxy[3]),
        (curxy[3], curxy[0]),
        (curxy[4], curxy[5]),
        (curxy[5], curxy[6]),
        (curxy[6], curxy[7]),
        (curxy[7], curxy[0]),
        (curxy[0], curxy[4]),  # here be dragons, connecting lines
        (curxy[1], curxy[5]),  # here be dragons, connecting lines
        (curxy[2], curxy[6]),  # here be dragons, connecting lines
        (curxy[3], curxy[7]),  # here be dragons, connecting lines
    ]
    newxy = []
    for xy in curxy:
        # print(f"working on {curxy}")
        # rotxy = rotate(center_point, xy, angle)
        rotxy = rotate((0, 0), xy, angle)
        newxy.append(rotxy)

        oled.pixel(round(rotxy[0] + offset_x), round(rotxy[1] + offset_y), 1)

    for line in lines:
        p1, p2 = line
        x1 = round(p1[0] + offset_x)
        y1 = round(p1[1] + offset_y)
        x2 = round(p2[0] + offset_x)
        y2 = round(p2[1] + offset_y)
        oled.line(x1, y1, x2, y2, 1)

    oled.show()
    # sleep(1)
    # angle += 0.1
