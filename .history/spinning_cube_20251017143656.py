import math
import time
from colorama import init
init()
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
# cube_widths = [20, 10, 5] # 複数サイズの立方体の半径(中心から各面までの距離)
# offsets = [-40, 10, 40]   # 各立方体の水平オフセット
cube_widths = [20]          # 複数サイズの立方体の半径(中心から各面までの距離)
offsets = [0]               # 各立方体の水平オフセット
width, height = 160, 40   # コンソールの画面サイズ(文字単位)
distance_from_cam = 100   # カメラとキューブの距離(小さくすると迫力が増す)
K1 = 40                   # 投影スケール(遠近感の強さを調整)
increment_speed = 0.6       # 点間のサンプリング間隔
target_fps = 60
target_dt = 1.0 / target_fps

# --- 背景文字 ---
background_ascii_code = '_' # 背景を見やすくする文字列(半角スペース, アンダーバー, etc.)

# --- バッファ ---
# z_bufferは回転キューブの各点の中で、手前の点だけを描画できるようにする。
z_buffer = [0] * (width * height) # どの点が手前にあるかを記録する(Zバッファ法)
buffer = [' '] * (width * height) # 描画する文字を格納する(2D画面)

# --- ANSIカラー定義 (ルービックキューブ6面) ---
colors = {
    "front":  "\033[31m@\033[0m",  # 赤
    "back":   "\033[35m+\033[0m",  # 紫(橙の代替)
    "right":  "\033[34m$\033[0m",  # 青
    "left":   "\033[32m~\033[0m",  # 緑
    "top":    "\033[37m#\033[0m",  # 白
    "bottom": "\033[33m;\033[0m",  # 黄
}

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

    idx = xp + yp * width
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
    windows10 以降の標準コンソール/Windows Terminal/PowerShellはANSIシーケンスに対応している。
    \033 - ESC(エスケープ)文字。エスケープシーケンスの開始を表すのに使う。
    \033[H - カーソルを(1,1)(左上)へ移動する。CUP(Cursor Position)の省略形。
    \033[J - カーソル位置から画面末尾までを削除する。ED(Erase in Display)のこと。

    エスケープシーケンスとは？
    エスケープシーケンス(escape sequence)とは、通常の文字ではなく特別な意味を持つ
    文字列のことである。
    str型のデータではなく、端末に対する命令を送るための"エスケープした文字列"である。
    """
    print("\033[H\033[J", end="") # Linux/mac/Windows(ANSI対応)共通

# ============================
# メインループ
# ============================
def main():
    global A, B, C, buffer, z_buffer
    prev_time = time.perf_counter()

    while True:
        frame_start = time.perf_counter()
        buffer = [background_ascii_code] * (width * height)
        z_buffer = [0] * (width * height)

        # --- 3つの立方体を描画 ---
        for cube_width, horizontal_offset in zip(cube_widths, offsets):
            cube_x = -cube_width
            while cube_x < cube_width:
                cube_y = -cube_width
                while cube_y < cube_width:
                    calculate_for_surface(cube_x + horizontal_offset, cube_y, -cube_width, colors["front"])
                    calculate_for_surface(cube_x + horizontal_offset, cube_y,  cube_width, colors["back"])
                    calculate_for_surface(cube_width + horizontal_offset, cube_y, cube_x, colors["right"])
                    calculate_for_surface(-cube_width + horizontal_offset, cube_y, -cube_x, colors["left"])
                    calculate_for_surface(cube_x + horizontal_offset, -cube_width, -cube_y, colors["bottom"])
                    calculate_for_surface(cube_x + horizontal_offset,  cube_width,  cube_y, colors["top"])
                    cube_y += increment_speed
                cube_x += increment_speed

        # --- 出力 (高速一括描画) ---
        clear_screen()
        output = ''.join(
            buffer[k] + ('\n' if (k + 1) % width == 0 else '')
            for k in range(width * height)
        )
        print(output)

        # --- 経過時間(dt)ベースで回転更新 ---
        now = time.perf_counter()
        dt = now - prev_time
        prev_time = now
        rotate_const = 10
        A += math.radians(rotate_const * 0) * dt # 1秒で180度回転
        B += math.radians(rotate_const * 2) * dt
        C += math.radians(rotate_const * 0) * dt

        # --- フレーム調整 ---
        elapsed = time.perf_counter() - frame_start
        to_sleep = target_dt - elapsed
        if to_sleep > 0:
            time.sleep(to_sleep)

if __name__ == '__main__':
    main()
