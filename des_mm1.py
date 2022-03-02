import numpy as np
import matplotlib.pyplot as plt


class SimulatorMM1:  # The answer to question 2 is this simulator
    def __init__(self, transmission_rate, link_rate, average_length):  # This simulator declares the necessary variables
        self.arrivals = 0  # keeps track of number of packets which have arrived in the queue
        self.departures = 0  # keeps track of the number of packets which have left the queue
        self.observations = 0  # keeps track of the number of observer events
        self.idle_counter = 0  # keeps track of number of times the queue is empty
        self.prev_departure_time = 0  # keeps track of the previous departure time, so we can generate the next one
        self.link_rate = link_rate  # Link rate in Mbps
        self.events = []  # queue of events containing Event object (arrival, departure or observer)
        self.snapshots = []  # list containing snapshots of relevant data from simulator
        self.rate = transmission_rate  # transmission rate, defined as lambda in the assignment doc
        self.average_packet_length = average_length  # sets the average packet length (L) to the given average length
        self.total_time = 0
        self.total_packets = 0

    def generate_arrival_events(self):  # generating random arrival events with lambda = self.rate
        e = Event("arrival", np.random.exponential(1 / self.rate))
        e.set_length(self.generate_random_length())  # giving them a random length with average 2000 size
        self.events.append(e)  # appending them to the events queue

    def generate_random_length(self):
        return np.random.exponential(self.average_packet_length)

    def generate_observation_events(self):
        self.events.append(Event("observer", np.random.exponential(1 / (self.rate * 5))))

    def generate_departure_events(self, events: list):  # generating departure events based upon
        for event in events:  # the computed service time of the existing
            if event.type == "arrival":  # arrival events,
                service_time = event.length / self.link_rate  # which is found by dividing L (random packet length)
                event.set_service_time(service_time)  # by C (the link rate, self.link_rate)
                if event.time + event.service_time > self.prev_departure_time:  # if this packet's (event) arrival time
                    departure_time = event.time + event.service_time  # and it's service time is greater than
                    self.prev_departure_time = departure_time  # the previous packet's departure time,
                    e = Event("departure", departure_time)  # then this packet's departure time
                    e.set_length(event.length)  # is based on only this packet's
                    self.events.append(e)  # arrival time + service time
                else:
                    departure_time = self.prev_departure_time + event.service_time  # else, this packet's departure time
                    self.prev_departure_time = departure_time  # is based on the previous packet's
                    e = Event("departure", departure_time)  # departure time + this packet's
                    e.set_length(event.length)  # service time. Either way,
                    self.events.append(e)  # set the prev departure time to
            else:  # this departure time and copy the
                pass  # packet's length to this length

    def deque_events(self, event):
        if event.type == "arrival":
            self.total_time += event.time
            self.handle_arrival_event()
        elif event.type == "departure":
            self.handle_departure_event()
        elif event.type == "observer":
            self.handle_observation_event()
        else:
            print("Event type not recognized. Moving on to next event.")

    def handle_arrival_event(self):
        self.arrivals += 1
        # print("arrival event handled")

    def handle_departure_event(self):
        self.departures += 1
        # print("departure event handled")

    def handle_observation_event(self):
        self.observations += 1
        if self.arrivals == self.departures:
            self.idle_counter += 1  # if queue is empty, we are incrementing the idle counter.
        self.snapshots.append(
            [self.observations, self.arrivals - self.departures, self.arrivals,
             self.departures, self.idle_counter])
        # print("observation event handled")

    def run_simulation(self, number):
        for i in range(number):
            self.generate_arrival_events()
            self.generate_observation_events()
        self.events.sort(key=lambda event: event.time, reverse=False)
        self.generate_departure_events(self.events)
        self.events.sort(key=lambda event: event.time, reverse=False)

        self.tabulate_results()
        for i in range(len(self.events)):
            e = self.events.pop(0)
            self.deque_events(e)

    def get_en(self):
        for snapshot in self.snapshots:
            self.total_packets += snapshot[1]
        En = self.total_packets / self.observations
        return En

    def get_pidle(self):
        return self.idle_counter / self.observations

    def tabulate_results(self):
        print("{:<17} {:<30} {:<35} {:<10}".format('Event Type', 'Event Time', 'Service Time', 'Packet Length'))
        print("{:<17} {:<30} {:<35} {:<10}".format('-----------', '---------------', '---------------', '------------'))
        for event in self.events:
            print("{:<17} {:<30} {:<35} {:<10}".format(event.type, event.time, event.service_time, event.length))


class Event:  # Event class: has variables type, time,
    def __init__(self, event_type, event_time):  # and an optional length variable (for packets)
        self.type = event_type
        self.time = event_time
        self.length = 0
        self.service_time = 0

    def set_length(self, packet_length):
        self.length = packet_length

    def set_service_time(self, service_time):
        self.service_time = service_time


# Calculating lambda based on specified rho range of 0.25 < p < 0.95
# Each simulation will be ran via these lambda values to then find E[N]
# Lambda is calculated by p * (C/L)
# E[N] is the "time-average number of packets in the queue
# pIDLE is the probability that the queue has no packets in it (idle)

rho_values = np.arange(0.25, 1, 0.1)
lambda_values = []

for i in range(len(rho_values)):
    lambda_values.append(int(rho_values[i] * (1000000 / 2000)))

print("\nLambda Values: ", lambda_values)

list_of_Ens = []
list_of_Pidles = []

# Running the simulator based on different lambda values calculated above.

for sims in range(len(rho_values)):
    sim = SimulatorMM1(lambda_values[sims], 1000000, 2000)
    sim.run_simulation(1000)
    list_of_Ens.append(sim.get_en())
    list_of_Pidles.append(sim.get_pidle())

print("\nLambda Values: ", lambda_values)
print("Rho Values: ", rho_values)
print("Length Of Rho List", len(rho_values))
print("List Of AVG Num Of Packets In System: ", list_of_Ens)
print("List Of pIDLE Values", list_of_Pidles)

# Creating Graph For E[N]
# X-Axis: Rho
# Y-Axis: E[N]
x = rho_values
y = list_of_Ens
plt.plot(x, y)
plt.title('Simulation Results: Question 3A')
plt.xlabel('Traffic Intensity p')
plt.ylabel('Average Number In System E[N]')
plt.show()

# Creating Graph For pIDLE
# X-Axis: Rho
# Y-Axis: pIDLE
x = rho_values
y = list_of_Pidles
plt.plot(x, y)
plt.title('Simulation Results: Question 3B')
plt.xlabel('Traffic Intensity p')
plt.ylabel('Probability The Queue Is Idle pIDLE')
plt.show()

