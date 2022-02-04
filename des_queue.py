# the actual lab assignment will go here.
import numpy as np

class Simulation:
    def __init__(self):
        self.num_in_system = 0
        self.clock = 0.0
        self.t_arrival = self.generate_interarrival()
        self.t_depart = float('inf')
        self.t_observer = self.generate_observer_event()
        self.num_arrivals = 0
        self.num_departs = 0
        self.total_wait = 0.0
        self.num_of_observer_events = 0
        self.log_of_arrivals = []
        self.log_of_departures = []

    def advance_time(self):
        t_event = min(self.t_arrival, self.t_depart)

        self.total_wait += self.num_in_system*(t_event - self.clock)
        self.clock = t_event


        if self.t_arrival <= self.t_depart:
            self.handle_arrival_event()
        else:
            self.handle_departure_event()

    def handle_arrival_event(self):
        self.num_in_system += 1
        self.num_arrivals += 1

        if self.num_in_system <= 1:
            self.t_depart = self.clock + self.generate_service()
        self.t_arrival = self.clock + self.generate_interarrival()

    def handle_departure_event(self):
        self.num_in_system -= 1
        self.num_departs += 1
        if self.num_in_system > 0:
            self.t_depart = self.clock + self.generate_service()
        else:
            self.t_depart = float('inf')

    def handle_observer_event(self):
        self.num_of_observer_events += 1

    def generate_interarrival(self):
        return np.random.exponential(1./75)

    def generate_service(self):
        return np.random.exponential(1./1000)

    def generate_observer_event(self):
        return np.random.exponential(1./75)/5



np.random.seed(0)

sim = Simulation()

for i in range(52):
    sim.advance_time()
    print(sim.clock)

# Todo: 1) Create list for arrival time, length (bits), service time, departure time
# Service time = departure time - arrival time
