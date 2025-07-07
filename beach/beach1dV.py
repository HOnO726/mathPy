import numpy as np
import matplotlib.pyplot as plt

#set sand
sand = np.ones(50)
for i in range(50):
    sand[i] = np.random.randn() * 0.3 + i * 0.1
amount = sand.sum()
# set flow
flow_speed = np.zeros(50)
flow_speed[0] = 1.0

epoch_num = 100
hop_value = 0.8

pic = []
flowing_sand = 0
for i in range(epoch_num):
    stop_idx = 0
    # forward
    for j in range(50):
        flow_force = sand[j+1] - sand[j] if j < 49 else 0
        flow_speed[j] = flow_speed[j-1] - flow_force * 0.3 if j > 0 else 1.0
        if flow_speed[j] < 0.01:
            sand[j] += flowing_sand * 0.8
            flowing_sand *= 0.2
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
        flow_force = sand[k] - sand[k-1] if k-1 > 0 else 0
        flow_speed[k] = flow_speed[k+1] + flow_force * 0.3 if k < stop_idx else 1.0
        flow_speed[k] = np.maximum(flow_speed[k], 0.02)
        if flow_speed[k] < flowing_sand:
            sand[k] += flowing_sand * 0.7
            flowing_sand *= 0.3
        else:
            sand[k] -= flow_speed[k] * 0.05
            flowing_sand += flow_speed[k] * 0.05
    # collapse
    diff = np.diff(sand)
    for j in range(49):
        if np.abs(diff[j]) > 2.0:
            mean = (sand[j] + sand[j+1]) / 2.0
            sand[j] = mean
            sand[j+1] = mean

    pic.append(sand.copy())
    sum = sand.sum()
    if sum > amount * 1.1:
        print(f"too much sand at epoch {i}, sum: {sum}, original sum: {amount}")
    flowing_sand = flowing_sand * 0.7 + 0.05

im = plt.imshow(pic)
plt.colorbar(im)
plt.savefig('picture/beach1dV.png')