import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation

sand =np.random.rand(50) * 0.5 + 1.0
flow_vector = np.zeros(50)
sand[0] = 1.0
flow_vector[0] = 1.0

pic = []
flow = []
moving_sand = 0
for i in range(200):
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
    for j in range(50):
        flow_vector[j] = 1 / sand[j]
        if flow_vector[j] > moving_sand:
            moving_sand += flow_vector[j] * 0.05
        else:
            sand[j] -= moving_sand * 0.7
            moving_sand *= 0.3
            sand[j] = np.maximum(sand[j], 0.01)
        if flow_vector[j] > 0.5:
            sand[j] += flow_vector[j] * 0.05
    for j in range(50):
        k = 49 - j
        flow_vector[k] = 1 / sand[k]
        if flow_vector[k] > moving_sand:
            moving_sand += flow_vector[k] * 0.05
        else:
            sand[k] -= moving_sand * 0.7
            moving_sand *= 0.3
            sand[k] = np.maximum(sand[k], 0.01)
        if flow_vector[k] > 0.5:
            sand[k] += flow_vector[k] * 0.05
    pic.append(sand.copy())
    flow.append(flow_vector.copy())
    
pic = np.array(pic)
"""
im = plt.imshow(pic)
plt.colorbar(im)
plt.savefig('beach1d_animation.png')
"""
plt.plot(pic[:, 20])
plt.savefig('beach1d_20trans.png')
