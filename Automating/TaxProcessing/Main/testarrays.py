import numpy as np


data = np.array([
    [1, 2,2],
    [4, 0, 6],
    [7, 8, 0],
    [10, 11, 0]
])

firstrow = data[0]
indec = list(firstrow).index(2)

output = data[2, indec]





print(type(output))
print(output)
