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
                math.sin()
