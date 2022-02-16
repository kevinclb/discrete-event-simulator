from collections import deque as dq
import numpy as np
import time


# Set a maximum queue length
# this_deque = dq(maxlen=5)

# print(this_deque.maxlen)

# # Generate a random time (75 packets per second)
# current_time = time.time()
# print(current_time)
# time.sleep(np.random.exponential(1/75))
# print(time.time())
#
## TODO: Create the logic for the simulation to run
class Simulation:
    def __init__(self):
        self.num_of_arrivals = 0
        self.num_of_departures = 0
        self.num_of_observers = 0
        self.events_log = []


## TODO: Create a structure, like an array, in Simulation to keep track of events
class Event:
    def __init__(self, type, time):
        self.type = type
        self.time = time
        self.length = np.random.exponential(1 / 75)


## TODO: Fix the Lambda's here
class Packet:
    def __init__(self):
        self.length = np.random.exponential(1 / 5)
    # def NewEvent(self):
    #


observer_event_times = []
arrival_event_times = []
departure_event_times = []
array_of_packets = [] # should be randomly generated
array_of_events = []
count = 0
i = 0 #arrival counter
j = 0 #departure counter
k = 0 #observer counter

# Generating the times and populating their respective arrays
# TODO: These are temporary lambda's, fix later
for i in range(5000):
    observer_event_times.append(np.random.exponential(1 / 75))
for i in range(5000):
    arrival_event_times.append(np.random.exponential(1 / 1000))
for i in range(5000):
    departure_event_times.append(np.random.exponential(1 / 1000))

while count < 3000:
    if arrival_event_times[i] < departure_event_times[j] and arrival_event_times[i] < observer_event_times[k]:
        ## increment 1 to arrivals, increment 1 to the counter i
        i+=1
        count+=1
    ## elif take the minimum of the next time
        ## check if theres any packets in the queue
print(observer_event_times)
