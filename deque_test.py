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

observer_event_times = []
arrival_event_times = []
departure_event_times = []
array_of_packets = []
count = 0
i = 0
j = 0
k = 0

for i in range(1000):
    observer_event_times.append(np.random.exponential(1/1000))

for i in range(1000):
    arrival_event_times.append(np.random.exponential(1/1000))

for i in range(1000):
    departure_event_times.append(np.random.exponential(1/1000))

while count < 1000:
    if arrival_event_times[i] < departure_event_times[j] and arrival_event_times[i] < observer_event_times[k]:
        ## increment 1 to arrivals, increment 1 to the counter i
    ## elif take the minimum of the next time
        ## check if theres any packets in the queue
print(observer_event_times)
