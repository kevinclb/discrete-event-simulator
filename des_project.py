import numpy as np
from collections import deque as dq
import time
import statistics as stat

# Question 1:

count = 0
var_list = []
while count < 1000:
    count += 1
    var_list.append(np.random.exponential(1 / 75))

# for i in var_list:
#     print(i)
mean = stat.mean(var_list)
variance = stat.variance(var_list)
print(mean)
print(variance)

# Question 2:
