import math
import time
"""
回転キューブの実装(2025/10/16)
参考にしたサイト
Channel name : Code Fiction
title        : 「スピニングキューブはどのように機能しますか？」
URL          : https://www.youtube.com/watch?v=0E0UBphVRhY

Channel name : Tarik Michel Follmer
title        : "I Made ASMR Spinning Cube with Python (Code Included)"
URL          : https://www.youtube.com/watch?v=ds97cgeFe54

"""

# --- 回転角度 ---
# A, B, Cはそれぞれ、x軸, y軸, z軸に対して反時計回りする回転角の大きさを表す。
A = B = C = 0

# --- 画面設定 ---
cube_widths = [20, 10, 5] # 複数サイズの立方体の半径(中心から各面までの距離)
offsets = [-40, 10, 40]   # 各立方体の水平オフセット
width, height = 160, 40   # コンソールの画面サイズ(文字単位)
distance_from_cam = 100   # カメラとキューブの距離(小さくすると迫力が増す)
K1 = 40                   # 投影スケール(遠近感の強さを調整)

# --- 表示設定 ---
background_ascii_code = ' ' # 背景を見やすくする文字列(半角スペース, アンダーバー, etc.)
increment_speed = 0.6       # キューブの点をサンプリングする間隔
target_fps = 60
target_dt = 1.0 / target_fps

# --- バッファ ---
# z_bufferは回転キューブの各点の中で、手前の点だけを描画できるようにする。
z_buffer = [0] * (width * height) # どの点が手前にあるかを記録する(Zバッファ法)
buffer = [' '] * (width * height) # 描画する文字を格納する(2D画面)


# ============================
# 回転計算の高速版
# ============================
def calculate_rotated(i, j, k):
    """(i, j, k) を角度 A,B,C で回転した(x', y', z') を返す"""
    sA, cA = math.sin(A), math.cos(A)
    sB, cB = math.sin(B), math.cos(B)
    sC, cC = math.sin(C), math.cos(C)

    x = j * (sA * sB * cC + cA * sC) + k * (-cA * sB * cC + sA * sC) + i * (cB * cC)
    y = j * (cA * cC - sA * sB * sC) + k * (sA * cC + cA * sB * sC) - i * (cB * sC)
    z = j * (-cA * cB) + k * (sA * cB) + i * (sB)
    return x, y, z

# ============================
# 投影とZバッファ描画
# ============================
def calculate_for_surface(cube_x, cube_y, cube_z, ch):
    global buffer, z_buffer
    x, y, z = calculate_rotated(cube_x, cube_y, cube_z)
    z += distance_from_cam

    ooz = 1 / z
    xp = int(width / 2 + K1 * ooz * x * 2)
    yp = int(height / 2 + K1 * ooz * y)

    idx = xp * yp * width
    if 0 <= idx < width * height:
        if ooz > z_buffer[idx]:
            z_buffer[idx] = ooz
            buffer[idx] = ch

# ============================
# 高速な画面クリア
# ============================
def clear_screen():
    """
    コンソールに表示した内容を削除する。
    \033 - ASCII エスケープ文字
    [H - ホームポジションにカーソルを移動する。
    [J - 現在の行から最後の行までに表示された内容を削除する。
    """
    print("\033[H\033[J", end="") # Linux/mac/Windows(ANSI対応)共通


# ============================

# ============================



# 各軸まわりの3次元回転行列の定義
def calculate_x(i, j, k):
    """
    3D回転で点(i, j, k)を回して得た新しいx座標を回転行列の展開形で直接計算する

    Args:
        i (_type_): _description_
        j (_type_): _description_
        k (_type_): _description_

    Returns:
        _type_: _description_
    """
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
    """
    3次元キューブの一面を2Dスクリーンに投影して、ある視点から見えるキューブの点を表示する
    Args:
        cube_x (_type_): _description_
        cube_y (_type_): _description_
        cube_z (_type_): _description_
        ch (_type_): _description_
    """
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


def main():
    global A, B, C, cube_width, horizontal_offset, buffer, z_buffer

    while True:
        buffer = [background_ascii_code] * (width * height)
        z_buffer = [0] * (width * height)
        cube_width = 20
        horizontal_offset = -2 * cube_width

        # キューブの大きさと配置する水平方向の位置座標を指定する
        for cube_width, offset in [(20, -40), (10, 10), (5, 40)]:
            horizontal_offset = offset
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

        clear_screen()
        print(''.join(buffer[k] + ('\n' if k % width == 0 else '') for k in range(width * height)))
        A += math.radians(3)
        B += math.radians(2)
        C += math.radians(1)
        time.sleep(0.016)

main()
