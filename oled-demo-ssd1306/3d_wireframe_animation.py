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

# Set screen dimensions
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64

# Set screen dimensions
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
utime.sleep_ms(50)  # delay to setup screen
oled = SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c)


# Function to get the center of the screen
def screen_center():
    return SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2


# Define Cube class
class Cube:
    def __init__(self, radius, location) -> None:
        self.points = []
        self.create_points()
        self.size = radius
        self.center = location
        self.edges = [
            (0, 1),
            (1, 3),
            (3, 2),
            (2, 0),
            (4, 5),
            (5, 7),
            (7, 6),
            (6, 4),
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),
        ]

    # Function to create cube vertices
    def create_points(self):
        i = (-1, 1)
        for x in i:
            for y in i:
                for z in i:
                    self.points.append((x, y, z))

    # Function to perform 3D rotation on cube vertices
    def rotate_3d(self, rotation_vector):
        nodes = [list(node) for node in self.points]
        x_theta, y_theta, z_theta = rotation_vector

        # Rotate around the Z-axis
        sin_theta = math.sin(z_theta)
        cos_theta = math.cos(z_theta)
        for node in nodes:
            x, y = node[0], node[1]
            node[0] = x * cos_theta - y * sin_theta
            node[1] = y * cos_theta + x * sin_theta

        # Rotate around the X-axis
        sin_theta = math.sin(x_theta)
        cos_theta = math.cos(x_theta)
        for node in nodes:
            y, z = node[1], node[2]
            node[1] = y * cos_theta - z * sin_theta
            node[2] = z * cos_theta + y * sin_theta

        # Rotate around the Y-axis
        sin_theta = math.sin(y_theta)
        cos_theta = math.cos(y_theta)
        for node in nodes:
            x, z = node[0], node[2]
            node[0] = x * cos_theta + z * sin_theta
            node[2] = z * cos_theta - x * sin_theta

        self.points = [tuple(node) for node in nodes]

    # Function to project 3D vertices onto a 2D plane
    def project_2d(self, nodes, draw_distance):
        flat_nodes = []

        for node in nodes:
            x, y, z = node
            flat_x = x * draw_distance / (draw_distance + z)
            flat_y = y * draw_distance / (draw_distance + z)
            flat_nodes.append([flat_x, flat_y])

        return flat_nodes

    # Function to shift the projected nodes to a new position
    def shift(self, nodes):
        shifted_nodes = [list(node) for node in nodes]
        for xy in shifted_nodes:
            x, y = xy
            xy[0] += round(x * self.size + center[0])
            xy[1] += round(y * self.size + center[1])

        return shifted_nodes

    # Function to draw the cube on the OLED display
    def draw(self, oled, distance):
        nodes = self.project_2d(self.points, distance)
        positioned_nodes = self.shift(nodes)

        for xy in positioned_nodes:
            x, y = xy
            oled.pixel(round(x), round(y), 1)

        for edge in self.edges:
            x1, y1 = positioned_nodes[edge[0]]
            x2, y2 = positioned_nodes[edge[1]]
            oled.line(round(x1), round(y1), round(x2), round(y2), 1)


def sleep(s: int = 0):
    # I'm lazy and I want my own sleep in seconds call.
    print(f"sleeping for {s} seconds...")
    utime.sleep_ms(s * 1000)


sleep(1)

# helpers
center = screen_center()
cx, cy = center

# Create a few cubes for the array
cubes = []
cubes.append(Cube(16, center))
cubes.append(Cube(10, center))
cubes.append(Cube(5, center))

# Clear the screen before starting
oled.fill(0)

# main loop
while True:
    # Clear the OLED display
    oled.fill(0)
    # Display banner
    oled.text("-Nathaniel Evry-", 0, 0, 1)

    # Rotate cubes 0,1,2 at visually interesting different speeds
    cubes[0].rotate_3d((0.03, 0.06, 0.09))
    cubes[1].rotate_3d((0.09, 0.03, 0.06))
    cubes[2].rotate_3d((0.06, 0.09, 0.03))

    # iterate over the cubes array and draw all of them
    for c in cubes:
        c.draw(oled, 5)

    # Show your work!
    oled.show()
