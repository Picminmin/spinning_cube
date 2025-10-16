import math
import os
import time
# A, B, Cはそれぞれ、x軸, y軸, z軸に対して反時計回りする回転角の大きさを表す。
A = B = C = 0

cube_width = 20         # キューブの半径 (中心から各面までの距離)
width, height = 160, 40 # コンソールの画面サイズ(文字単位)

# z_bufferは回転キューブの各点の中で、手前の点だけを描画できるようにする。
z_buffer = [0] * (width * height) # どの点が手前にあるかを記録する(Zバッファ法)
buffer = [' '] * (width * height) # 描画する文字を格納する(2D画面)
background_ascii_code = ' '       # 背景を見やすくする文字列(半角スペース, アンダーバー, etc.)
distance_from_cam = 200           # カメラとキューブの距離(小さくすると迫力が増す)
horizontal_offset = 0
K1 = 40                     # 投影スケール(遠近感の強さを調整)

# increment_speed = 0.6       # キューブの点をサンプリングする間隔
increment_speed = 1.5       # キューブの点をサンプリングする間隔(こっちのほうがスムーズに動く)

# 各軸まわりの3次元回転行列の定義
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

    # 遠近法の「逆深度」, 遠くにある点を小さく映すのに使う
    ozz = 1 / z 

    xp = int(width / 2 + horizontal_offset + K1 * ozz * x * 2)
    yp = int(height / 2 + K1 * ozz * y)

    idx = xp + yp * width
    if 0<= idx < width * height:
        if ozz > z_buffer[idx]:
            # より手前(小さいz)の点だけを描画する
            z_buffer[idx] = ozz
            buffer[idx] = ch

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

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
                # キューブの各面を描画する
                calculate_for_surface(cube_x, cube_y, -cube_width, '@')
                calculate_for_surface(cube_width, cube_y, cube_x, '$')
                calculate_for_surface(-cube_width, cube_y, -cube_x, '~')
                calculate_for_surface(-cube_x, cube_y, cube_width, '#')
                calculate_for_surface(cube_x, -cube_width, -cube_y, ';')
                calculate_for_surface(cube_x, cube_width, cube_y, '+')
                cube_y += increment_speed
            cube_x += increment_speed

        cube_width = 10
        horizontal_offset = 1 * cube_width
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
                cube_y += increment_speed
            cube_x += increment_speed

        cube_width = 5
        horizontal_offset = 8 * cube_width
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
                cube_y += increment_speed
            cube_x += increment_speed

        clear_screen()
        for k in range(width * height):
            if k % width == 0 and k != 0:
                print()
            print(buffer[k], end='')


        A += 0.05
        B += 0.05
        C += 0.01
        time.sleep(0.016)

main()
