from collections import deque as dq
import numpy as np
import time
# Set a maximum queue length
# this_deque = dq(maxlen=5)

# print(this_deque.maxlen)

# Generate a random time (75 packets per second)
current_time = time.time()
print(current_time)
time.sleep(np.random.exponential(1/75))
print(time.time())

