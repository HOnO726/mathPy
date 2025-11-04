import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import os

# Parameters
size = 100
alpha = 0.2
beta = 0.1
ganma = 2.1
speed_rate = 0.3
speed_min = 0.2
epoch = 500
collide = 0.05

sand =np.zeros((epoch, size))
speed_vector = np.zeros((2, epoch, size))
# Initial condition
for x in range(size):
    sand[0,x] = 1.0 + x * 0.02 #+ np.random.rand() * 0.1

moving_sand = 0
sand_diffs = []
moving_sands = []

def sand_calc(sand_instance, speed_instance, moving_sand_instance):
    #sand_diff = speed_instance * alpha - moving_sand_instance / speed_instance * beta
    #sand_diff = speed_instance * alpha - moving_sand * np.log(ganma-speed_instance)  * beta
    sand_diff = speed_instance * alpha - moving_sand * beta
    sand_diff = np.maximum(sand_diff, -moving_sand_instance)
    sand_instance -= sand_diff
    moving_sand_instance += sand_diff
    sand_diffs.append(sand_diff)
    moving_sands.append(moving_sand_instance)
    return sand_instance, moving_sand_instance

for t in range(epoch-1):
    """
    flow_vector = 1 / sand
    erode_or_not = np.where(flow_vector > 0.5, 1, 0)
    depo_or_not = np.ones_like(sand) - erode_or_not
    move = flow_vector * erode_or_not * 0.05
    sand += move
    sand = np.maximum(sand, 0.01)
    pic.append(sand.copy())
    flow.append(flow_vector.copy())
    """
    #moving_sand = 0.5
    speed = 1.0
    for x in range(size):
        #speed += (sand[t,x] - sand[t,x+1]) * speed_rate if x < 49 and 0 < t else 0
        speed -= (1.0 - speed_min) / size
        #speed = np.maximum(speed, speed_min)
        sand[t+1,x], moving_sand = sand_calc(sand[t,x], speed, moving_sand)
        speed_vector[0,t+1,x] = speed
    speed = 0
    for x in range(size):
        x_ = size - 1 - x
        #speed += (sand[t+1,x_] - sand[t+1,x_-1]) * speed_rate if x_ > 0 else 0
        speed += (1.0 - speed_min) / size
        #speed = np.maximum(speed, speed_min)
        sand[t+1,x_], moving_sand = sand_calc(sand[t+1,x_], speed, moving_sand)
        speed_vector[1,t+1,x_] = speed
    # Smooth with zero-flux boundary conditions
    sand_item = sand[t+1].copy()
    for x in range(size):
        if 0 < x < size-1:
            # Interior points: standard diffusion
            sand[t+1,x] += (sand_item[x-1] + sand_item[x+1] - 2 * sand_item[x]) * collide
        elif x == 0:
            # Left boundary: zero-flux (du/dx = 0)
            sand[t+1,x] += (sand_item[x+1] - sand_item[x]) * collide
        elif x == size-1:
            # Right boundary: zero-flux (du/dx = 0)
            sand[t+1,x] += (sand_item[x-1] - sand_item[x]) * collide

    # for x in range(size):
    #     diff = sand[t+1,x] - sand[t+1,x+1] if x < 49 else 0
    #     if diff > 0.0:
    #         sand[t+1,x] -= diff / 2.0
    #         sand[t+1,x+1] += diff / 2.0
    # for x in range(size):
    #     x_ = 49 - x
    #     diff = sand[t+1,x_] - sand[t+1,x_-1] if x_ > 0 else 0
    #     if diff > 0.0:
    #         sand[t+1,x_] -= diff / 2.0
    #         sand[t+1,x_-1] += diff / 2.0
"""
im = plt.imshow(pic)
plt.colorbar(im)
plt.savefig('beach1d_animation.png')
"""
print(sand[1])
time_name = time.strftime("%Y%m%d-%H%M%S")
if not os.path.exists('results'):
    os.makedirs('results')
os.makedirs('results/beach2_1D_' + time_name)
plt.imshow(sand, aspect='auto')
plt.colorbar()
plt.savefig(f'results/beach2_1D_{time_name}/beach2_1D_200_{time_name}.png')
plt.close()
plt.imshow(speed_vector[0], aspect='auto')
plt.colorbar()
plt.savefig(f'results/beach2_1D_{time_name}/beach2_1D_speed1_200_{time_name}.png')
plt.close()
plt.imshow(speed_vector[1], aspect='auto')
plt.colorbar()
plt.savefig(f'results/beach2_1D_{time_name}/beach2_1D_speed2_200_{time_name}.png')
plt.close()
plt.plot(sand[-1], label='sand')
plt.plot(speed_vector[0,-1]*2.0, label='speed_forward')
plt.plot(speed_vector[1,-1]*2.0, label='speed_backward')
plt.legend()
plt.savefig(f'results/beach2_1D_{time_name}/beach2_1D_last_200_{time_name}.png')
plt.close()

sand_diffs = np.array(sand_diffs).reshape((epoch-1, size*2))
plt.imshow(sand_diffs, aspect='auto')
plt.colorbar()
plt.savefig(f'results/beach2_1D_{time_name}/beach2_1D_sand_diffs_{time_name}.png')
plt.close()

moving_sands = np.array(moving_sands).reshape((epoch-1, size*2))
plt.imshow(moving_sands, aspect='auto')
plt.colorbar()
plt.savefig(f'results/beach2_1D_{time_name}/beach2_1D_moving_sands_{time_name}.png')
plt.close()

plt.plot(sand[:,0], label='sand_0')
plt.plot(sand[:,size//2], label='sand_50')
plt.plot(sand[:,-1], label='sand_99')
plt.legend()
plt.savefig(f'results/beach2_1D_{time_name}/beach2_1D_sand_positions_{time_name}.png')
plt.close()