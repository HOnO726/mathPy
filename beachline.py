import numpy as np
import matplotlib.pyplot as mpl
mpl.switch_backend('TkAgg')

sand = np.ones((500,500))
zeros = np.zeros((1,500))
epoch = 200
hop_value=1.1
hop_ratio = 0.002

def relu(x):
    return np.maximum(x,0)

for i in range(epoch):
    """
    grad_sand = np.diff(sand)
    left_grad = np.concatenate([grad_sand,zeros],1)
    right_grad = np.concatenate([zeros,grad_sand],1)
    """
    water = np.zeros(sand.shape)
    water_summin = 0
    for j in range(100):
        water_temp = np.ones(sand.shape)*3*j/100 - sand
        water_temp = relu(water_temp)
        if (water.sum()-2500) > 0 and water.sum() > water_summin:
            water_summin = water.sum()
            water = water_temp.copy()
    water += np.random.randn(*water.shape)*0.01
    water = relu(water)
    for k in range(water.shape[1]-1):
        water[k+1,:] += water[k,:]*1
    erode = np.maximum(water**2-hop_value,0) * hop_ratio
    sand -= erode

im = mpl.imshow(sand)
mpl.colorbar(im)
mpl.show()

