# # Just scratch paper. The project files are main.py and des_mm1.py
# # Only use this as a playground for testing functions.
#
#
# # number = np.random.exponential(1 / 385, 100000)
# # six_places = round(Decimal(0.000003), 6)
# # print(six_places == round(Decimal(0.0000030001), 6))
#
# if type(5) is int:
#     print("true, 5 is int")
#
#
# class Packet:
#     arrival_time = 0
#     time = arrival_time
#
#     def __init__(self, time):
#         self.arrival_time = time
#         self.departure_time = 0
#
#     def set_time(self, time):
#         self.departure_time = time
#         return self
#
#     def get_time(self):
#         return self.departure_time
#
#
# class Observation:
#     def __init__(self, time):
#         self.time = time
#         self.different_time = 0
#
#     def set_time(self, time):
#         self.different_time = time
#         return self
#
#     def get_time(self):
#         return self.different_time
#
#
# list = [Packet(0).set_time(4), Observation(0).set_time(1)]
# list.sort(key=lambda item: item.get_time())
# for i in list:
#     print(i)
# d = {'a': 0, 'b': 1, 'c': 2}
# values = list(d.items())
# print(values[len(values)-1][1])
import random
import math
import numpy as np
import statistics as stats
#

lam = 125
list1 = []
list2 = []
list3 = []
for i in range(1000):
    r = random.uniform(0, 1)
    list1.append(-((1 / lam) * math.log(1 - r)))
    list2.append(np.random.exponential(1 / 125))
    list3.append(np.random.exponential(1 / (125 * 5)))

print("mean list 1 (explicit formula) : ", stats.mean(list1))
print("mean list 2 (np.random.exponential) : ", stats.mean(list2))
print("mean list 3 (np.random.exponential) : ", stats.mean(list3))
