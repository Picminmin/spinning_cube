import math
import os
import time
A = B = C = 0

cube_width = 20
width, height = 160, 40
z_buffer = [0] * (width * height)
buffer = [' '] * (width * height)
background_ascii_code = '_'
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
    z = calculate_z(cube_x, cube_y, cube_z) + distance_from_cam

    ozz = 1 / z

    xp = int(width / 2 + horizontal_offset + K1 * ozz * x * 2)
    yp = int(height / 2 + K1 * ozz * y)

    idx = xp + yp * width
    if 0<= idx < width * height:
        if ozz > z_buffer[idx]:
            z_buffer[idx] = ozz
            buffer[idx] = ch

def clear_screen():
    os. system('cls' if os.name == 'nt' else 'clear')

def main():
    global A, B, C, cube_width, horizontal_offset, buffer, z_buffer

    while True:
        buffer = [background_ascii_code] * (width * height)
        z_buffer = [0] * (width * height)
        cube_width = 20
        horizontal_offset = -2 * cube_width

        cube_x = -cube_width
        while cube_x < cube_width:
            cube_y = -cube_width
            while cube_y < cube_width:
                calculate_for_surface(cube_x, cube_y, -cube_width, '@')
                calculate_for_surface(cube_width, cube_y, cube_x, '$')
                calculate_for_surface(-cube_width, cube_y, -cube_x, '~')
                calculate_for_surface(-cube_x, cube_y, cube_width, '#')
                calculate_for_surface(cube_x, -cube_width, -cube_y, ';')
                calculate_for_surface(cube_x, cube_width, cube_y, '+')
