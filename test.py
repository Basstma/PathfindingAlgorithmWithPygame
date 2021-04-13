import numpy as np

arr = np.zeros((10, 10))

print(arr)

arr[-1:] = 1

print(arr)

arr[:,-1:] = 1

print(arr)