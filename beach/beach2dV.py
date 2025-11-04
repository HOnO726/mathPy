import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# set sand
size = 50
sand_size = (size, size)
sand = np.ones(sand_size)
for i in range(sand_size[0]):
    sand[i, :] = np.random.randn() * 0.1 + i * 0.1

flow_speed_x = np.zeros(sand_size)
flow_speed_y = np.zeros(sand_size)
flow_speed_y[0] = 1.0

epoch_num = 15
anim = []
flow_sand = np.zeros(sand_size[1])


for i in range(epoch_num):
    stop_idxs = np.zeros(sand_size[1])
    water_stock = np.zeros(sand_size)
    water = np.ones(sand_size[1])
    # forward
    for j in range(sand_size[0]):
        # horizontal
        for k in range(sand_size[1]-1):
            watermove = ((water[k] + sand[j, k]) - (water[k+1] + sand[j, k+1])) / 2
            watermove = min([water[k], water[k+1], watermove])
            sandmove = flow_sand[k] * (abs(watermove) / (water[k]+1e-3)) - flow_sand[k+1] * (abs(watermove) / (water[k+1]+1e-3))
            water[k] -= watermove
            water[k+1] += watermove
            flow_sand[k] -= sandmove
            flow_sand[k+1] += sandmove
        # vertical
        flow_force = sand[j+1, :] - sand[j, :] if j < sand_size[0]-1 else np.zeros(sand_size[1])
        flow_speed_y[j, :] = flow_speed_y[j-1, :] - flow_force * 0.5 if j > 0 else np.ones(sand_size[1])
        if i==0 and j==0:
            print(f"flow_force:{flow_force}")
            print(f"flow_sand:{flow_sand}")
            print(f"water:{water}")
        for k in range(sand_size[1]):
            if flow_force[k] > 0.4:
                sand[j, k] += flow_sand[k] * 0.5
                flow_sand[k] *= 0.5
            elif flow_force[k] < -0.2:
                sand[j, k] -= flow_force[k] * water[k] * 0.1
                flow_sand[k] += flow_force[k] * water[k] * 0.1
            if flow_speed_y[j, k] < 0.01:
                sand[j, k] += flow_sand[k] * 0.9
                flow_sand[k] *= 0.1
                stop_idxs[k] = j
                water_stock[j, k] = water[k] * 0.7
                water[k] *= 0.3
                break
            if flow_speed_y[j, k] < flow_sand[k]:
                sand[j, k] += flow_sand[k] * 0.7
                flow_sand[k] *= 0.3
            else:
                sand[j, k] -= flow_speed_y[j, k] * water[k] * 0.05
                flow_sand[k] += flow_speed_y[j, k] * water[k] * 0.05
            if j==sand_size[0]-1:
                stop_idxs[k] = j
                water_stock[j, k] = water[k]
                water[k] = 0
    #backward
    for l in range(sand_size[0]):
        j = sand_size[0] - 1 - l
        water += water_stock[j, :]
        # horizontal
        for k in range(sand_size[1]-1):
            watermove = ((water[k] + sand[j, k]) - (water[k+1] + sand[j, k+1])) / 2
            watermove = min([water[k], water[k+1], watermove])
            sandmove = flow_sand[k] * (abs(watermove) / (water[k]+1e-3)) - flow_sand[k+1] * (abs(watermove) / (water[k+1]+1e-3))
            water[k] -= watermove
            water[k+1] += watermove
            flow_sand[k] -= sandmove
            flow_sand[k+1] += sandmove
        # vertical
        flow_force = sand[j-1, :] - sand[j, :] if j > 0 else np.zeros(sand_size[1])
        flow_speed_y[j, :] = flow_speed_y[j+1, :] - flow_force * 0.5 if j < sand_size[0]-1 else np.ones(sand_size[1])*0.1
        flow_speed_y[j, :] = np.maximum(flow_speed_y[j, :], 0.01)
        for k in range(sand_size[1]):
            if flow_force[k] > 0.4:
                sand[j, k] += flow_sand[k] * 0.5
                flow_sand[k] *= 0.5
            elif flow_force[k] < -0.2:
                sand[j, k] -= flow_force[k] * water[k] * 0.1
                flow_sand[k] += flow_force[k] * water[k] * 0.1
            if flow_speed_y[j, k] < flow_sand[k]:
                sand[j, k] += flow_sand[k] * 0.7
                flow_sand[k] *= 0.3
            else:
                sand[j, k] -= flow_speed_y[j, k] * water[k] * 0.05
                flow_sand[k] += flow_speed_y[j, k] * water[k] * 0.05
    pic = plt.imshow(sand)
    anim.append([pic])
    print(water)

fig = plt.figure()
ani = animation.ArtistAnimation(fig, anim, interval=100)      
ani.save('animation/beachline_animation.mp4', writer='ffmpeg', fps=10)