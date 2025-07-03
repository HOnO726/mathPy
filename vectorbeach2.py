import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# set sand
sand = np.ones((500, 500, 1))
for i in range(500):
    sand[i] += np.random.randn((500, 1)) * 0.05 + (500 - i)/500

epoch = 200

for i in range(epoch):
    flow_vector = np.zeros((1, 500, 2))
    water_amount = np.ones((1, 500, 1)) * 0.5

    for j in range(500):
        water_surface = np.mean(sand[j]+water_amount)
        water_amount = water_surface - sand[j]
        
