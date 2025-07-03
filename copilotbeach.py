import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from noise import pnoise2

# 地形サイズとパラメータ
size = 128
scale = 50
erosion_rate = 0.05
steps = 100

# 初期地形の生成（Perlinノイズを使う）
def generate_terrain(size, scale):
    return np.array([[pnoise2(x/scale, y/scale, octaves=6) for x in range(size)] for y in range(size)])

# 単純な水の流れ：標高が低い方向へ移動（8方向を比較）
def calculate_flow(terrain):
    flow = np.zeros_like(terrain)
    for y in range(1, size-1):
        for x in range(1, size-1):
            center = terrain[y, x]
            min_val = center
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    neighbor = terrain[y + dy, x + dx]
                    if neighbor < min_val:
                        min_val = neighbor
            flow[y, x] = max(0, center - min_val)
    return flow

# 浸食処理：流量に応じて地形を削る
def erode(terrain, flow, rate):
    return terrain - flow * rate

# 可視化
def plot_terrain(terrain, step=None, images=[]):
    im = plt.imshow(terrain)
    images.append([im])
    return images

ims = []
# メインループ
terrain = generate_terrain(size, scale)
for step in range(steps):
    flow = calculate_flow(terrain)
    terrain = erode(terrain, flow, erosion_rate)
    ims = plot_terrain(terrain, step, ims)
# アニメーションの保存
fig = plt.figure()
ani = animation.ArtistAnimation(fig, ims, interval=100)
ani.save('terrain_erosion.mp4', writer='ffmpeg', fps=10)
plt.close(fig)  # グラフを閉じる