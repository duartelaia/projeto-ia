import numpy as np

x = np.array([[[0, 10], [3, 10], [0, 10]], [[0, 10], [0, 10], [0, 10]]])
y = np.copy(x)

y[0][0][1] = 100

print(x)
print()
print(y)