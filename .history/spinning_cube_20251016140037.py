import math
import os
import time
A = B = C = 0

cube_width = 20
width, height = 160, 40
z_buffer = [0] * (width * height)
buffer = [' '] * (width * height)
background_ascil_code = '_'
distance_from_cam = 100
horizontal_offset = 0
K1 = 40

increment_speed = 0.6

def calculate_x(i, j, k):
    return j * math.sin(A) *\
                math.sin(B) *\
                math.cos(C) - k *\
                math.cos(A) *\
                math.sin(B) *\
                math.cos(C) + j *\
                math.cos(A) * math.sin(C) + k *\
                math.sin(A) *\
                math.sin(C) + i*\
                math.cos(B) *\
                math.cos(C)

def calculate_y(i, j, k):
    return j * math.cos(A) *\
                math.cos(C) + k*\
                math.sin(A) *\
                math.cos(C) - j *\
                math.sin(A) *\
                math.sin(B) *\
                math.sin(C) + k *\
                math.cos(A) *\
                math.sin(B) *\
                math.sin(C) - i *\
                math.cos(B) *\
                math.sin(C)

def calculate_z(i, j, k):
    return k * math.cos(A) * math.cos(B) - j * math.sin(A) * math.cos(B) + i * math.sin(B)

def calculate_for_surface(cube_x, cube_y, cube_z, ch):
    global buffer, z_buffer

    x = calculate_x(cube_x, cube_y, cube_z)
    y = calculate_y(cube_x, cube_y, cube_z)
    x = calculate_x(cube_x, cube_y, cube_z)
