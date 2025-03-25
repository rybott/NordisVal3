import numpy as np


'''Numpy Arrays
Array[x,y] -> Used to Access Variables
    X = Col Index
    Y = Row Index

np.array([
   X0 [y0,y1,y2,y3],
   X1 [y0,y1,y2,y3],
   X2 [y0,y1,y2,y3]
])

'''



data = np.array([
    [1, 2,2],
    ["t2", 0, "t4"],
    [7, "t1", 9],
    [10, "t3", 0]
])


indec = list(data[0]).index("t1")
print(indec)

output = data[2, indec]

print(type(output))
print(output)

output = data[1, 2]

print(type(output))
print(output)