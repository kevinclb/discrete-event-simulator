import numpy as np
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
# print(mean)
# print(variance)

# Question 2:

# See "des_mm1.py" for the simulation of M/M/1 queue.
# TODO: We have to write a detailed description (along with maybe some diagrams) of our code.
