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

d = {'a': 0, 'b': 1, 'c': 2}
values = list(d.items())
print(values[len(values)-1][1])