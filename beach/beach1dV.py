import numpy as np
import matplotlib.pyplot as plt

#set sand
sand = np.ones(50)
for i in range(50):
    sand[i] = np.random.randn() + i * 0.1

# set flow
flow_speed = np.zeros(50)
flow_speed[0] = 1.0

epoch_num = 50
hop_value = 0.8

pic = []

for i in range(epoch_num):
    flowing_sand = 0
    stop_idx = 0
    # forward
    for j in range(50):
        flow_force = sand[j] - sand[j+1] if j < 49 else 0
        flow_speed[j] = flow_speed[j-1] - flow_force * 0.25 if j > 0 else 1.0
        if flow_speed[j] < 0.01:
            sand[j] += flowing_sand * 0.9
            flowing_sand *= 0.1
            stop_idx = j
            break
        if flow_speed[j] < flowing_sand:
            sand[j] += flowing_sand * 0.7
            flowing_sand *= 0.3
        else:
            sand[j] -= flow_speed[j] * 0.05
            flowing_sand += flow_speed[j] * 0.05
        if j==49:
            stop_idx = 49
    # backward  
    for j in range(stop_idx+1):
        k = stop_idx - j
        flow_force = sand[k] - sand[k+1] if k < 49 else 0
        flow_speed[k] = flow_speed[k+1] + flow_force * 0.25 if j > 0 else 1.0
        flow_speed[k] = np.maximum(flow_speed[k], 0.02)
        if flow_speed[k] < flowing_sand:
            sand[k] += flowing_sand * 0.7
            flowing_sand *= 0.3
        else:
            sand[k] -= flow_speed[k] * 0.05
            flowing_sand += flow_speed[k] * 0.05
    pic.append(sand.copy())

im = plt.imshow(pic)
plt.colorbar(im)
plt.savefig('picture/beach1dV.png')