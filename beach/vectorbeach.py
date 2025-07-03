import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation

sand = np.ones((500, 500))
flow_vector = np.zeros((500, 500, 2))
zeros_horizontal = np.zeros((500, 1))
zeros_vertical = np.zeros((1, 500))
# sand set
for i in range(500):
    sand[i, 230:270] -= 0.5

flow_speed = np.zeros((500, 500))
flow_speed[0, :] = 1.0

epoch = 200
hop_value = 0.8
ims = []
fig = plt.figure()
for i in range(epoch):
    flow_vector[:, :, 0] = np.diff(np.concatenate([zeros_horizontal, np.diff(sand, axis=-1), zeros_horizontal], 1), axis=-1)  # horizontal gradient
    flow_vector[:, :, 1] = np.diff(np.concatenate([zeros_vertical, np.diff(sand, axis=0), zeros_vertical], 0), axis=0) + 1  # vertical flow
    for j in range(500):
        water_amount = np.ones_like(sand[j]) * 1.0
        water_surface = np.mean(sand[j] + water_amount)
        water_amount = water_surface - sand[j]
        water_amount = np.maximum(water_amount, 0.1)  # prevent negative
        water_amount = np.maximum(water_amount, 0)
        flow_vector[j] *= np.repeat((water_amount / np.sqrt(flow_vector[j, :, 0]**2 + flow_vector[j, :, 1]**2))[:, np.newaxis], 2, axis=1)
        if j > 0:
            flow_vector[j] += flow_vector[j - 1] * 0.5
    erode_or_not = np.where(flow_vector[:, :, 0]**2 + flow_vector[:, :, 1]**2 > hop_value**2, 1, 0)
    move_forward = np.zeros_like(sand[0])
    for j in range(500):
        move_const = move_forward * erode_or_not[j]
        sand[j] += move_forward - move_const
        move_vector = flow_vector[j] * np.repeat(erode_or_not[j].copy()[:, np.newaxis], 2, axis=1) * 0.01
        move_amount = np.sqrt(move_vector[:, 0]**2 + move_vector[:, 1]**2)
        sand[j] -= move_amount
        move_vector *= np.repeat(move_amount[:, np.newaxis], 2, axis=1)  / (np.sum(move_vector, axis=1, keepdims=True) + 1e-7)
        move_left = np.maximum(np.insert(move_vector[:, 0], 0, 0)[:-1], 0)
        move_right = np.maximum(np.insert(move_vector[:, 0]*(-1), -1, 0)[1:], 0)
        move_forward = move_vector[:, 1] + move_left + move_right
    im = plt.imshow(sand)
    ims.append([im])
    
ani = animation.ArtistAnimation(fig, ims, interval=100)      
ani.save('beachline_animation.mp4', writer='ffmpeg', fps=10)
