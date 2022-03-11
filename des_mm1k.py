import numpy as np
import matplotlib.pyplot as plt


class SimulatorMM1:  # The answer to question 2 is this simulator
    def __init__(self, transmission_rate, link_rate, buffer_limit):  # This simulator declares the necessary variables
        self.drops = 0
        self.arrivals = 0  # keeps track of number of packets which have arrived in the queue
        self.departures = 0  # keeps track of the number of packets which have left the queue
        self.observations = 0  # keeps track of the number of observer events
        self.idle_counter = 0  # keeps track of number of times the queue is empty
        self.prev_departure_time = 0  # keeps track of the previous departure time, so we can generate the next one
        self.link_rate = link_rate  # Link rate in Mbps
        self.events = []  # queue of events containing Event object (arrival, departure or observer)
        self.snapshots = []  # list containing snapshots of relevant data from simulator
        self.rate = transmission_rate  # transmission rate, defined as lambda in the assignment doc
        self.average_packet_length = 2000  # sets the average packet length (L) to the given average length
        self.total_time = 0
        self.total_packets = 0
        self.buffer_limit = buffer_limit
        self.packet_lengths = []

    def generate_arrival_events(self, time):  # generating random arrival events with lambda = self.rate
        e = Event("arrival", time)
        e.set_length(self.generate_random_length())  # giving them a random length with average 2000 size
        self.events.append(e)  # appending them to the events queue

    def generate_random_length(self):
        return np.random.exponential(self.average_packet_length)

    def generate_observation_events(self, time):
        self.events.append(Event("observer", time))

    def generate_departure_events(self, events: list):  # generating departure events based upon
        for event in events:  # the computed service time of the existing
            if event.type == "arrival":  # arrival events, 1000000
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
            if self.arrivals - self.departures < self.buffer_limit:
                self.handle_arrival_event()
            else:
                self.drops += 1
                self.packet_lengths.append(event.length)
                # for i in range(len(self.events)-1):
                #     if self.events[i].length == event.length and self.events[i].type == "departure":
                #         self.events.pop(i)
        elif event.type == "departure":
            if self.packet_lengths.__contains__(event.length):
                pass
            else:
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
             self.departures, self.idle_counter, self.drops])
        # print("observation event handled")

    def run_simulation(self, time):
        arrival_time = 0
        observation_time = 0
        while arrival_time < time:
            arrival_time += np.random.exponential(1 / self.rate)
            self.generate_arrival_events(arrival_time)
        while observation_time < time:
            observation_time += np.random.exponential(1 / (5 * self.rate))
            self.generate_observation_events(observation_time)
        self.events.sort(key=lambda event: event.time, reverse=False)
        self.generate_departure_events(self.events)
        self.events.sort(key=lambda event: event.time, reverse=False)

        # self.tabulate_results()
        for i in range(len(self.events)):
            if len(self.events) > 1:
                e = self.events.pop(0)
                self.deque_events(e)
            else:
                break

        print("done with simulation")

    def get_en(self):
        for snapshot in self.snapshots:
            self.total_packets += snapshot[1]
        En = self.total_packets / self.observations
        return En

    def get_pidle(self):
        return self.idle_counter / self.observations

    def get_ploss(self):
        return self.drops / (self.drops + self.departures)


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

#
# sim = SimulatorMM1(transmission_rate=250, link_rate=1000000, buffer_limit=10)
# sim.run_simulation(100)
# print("number of drops 1: ", sim.drops)
# e1 = sim.get_en()
#
# sim = SimulatorMM1(transmission_rate=325, link_rate=1000000, buffer_limit=10)
# sim.run_simulation(100)
# print("number of drops 2: ", sim.drops)
# e2 = sim.get_en()
#
# print(e1, e2)
# Creating Graph For E[N]
# X-Axis: Rho
# Y-Axis: E[N]

# -----------------Question 6-----------------
# Calculating lambda based on specified rho range of 0.5 < p < 1.5
# Each simulation will be ran via these lambda values to then find E[N] & pLOSS
# Lambda is calculated by p * (C/L)
# E[N] is the "time-average number of packets in the queue
# pLOSS is the ratio of the total number of packets lost due to buffer full condition...
# to the total number of generated packets.


rho_values = np.arange(0.5, 1.5, 0.1)
lambda_values = []

for i in range(len(rho_values)):
    lambda_values.append(int((rho_values[i] * 1000000) / 2000))

print("\nLambda Values: ", lambda_values)
print("Rho Values: ", rho_values)
print("Length Of Rho List", len(rho_values))

k_values = [10, 25, 50]
list_of_EN10 = []
list_of_pLOSS10 = []
list_of_EN25 = []
list_of_pLOSS25 = []
list_of_EN50 = []
list_of_pLOSS50 = []

# Running the simulator for k = 10 based on different lambda values calculated above.

for sims in range(len(rho_values)):
    sim = SimulatorMM1(transmission_rate=lambda_values[sims], link_rate=1000000, buffer_limit=k_values[0])
    sim.run_simulation(time=100)
    list_of_EN10.append(sim.get_en())
    list_of_pLOSS10.append(sim.get_ploss())

print("List Of AVG Num Of Packets In System For K = 10: ", list_of_EN10)
print("Total Packets Dropped: ", sim.drops)
print("Total Packets Departed: ", sim.departures)
print("List Of Ploss Values For K = 10: ", list_of_pLOSS10)


# Running the simulator for k = 25 based on different lambda values calculated above.

for sims in range(len(rho_values)):
    sim = SimulatorMM1(transmission_rate=lambda_values[sims], link_rate=1000000, buffer_limit=k_values[1])
    sim.run_simulation(100)
    list_of_EN25.append(sim.get_en())
    list_of_pLOSS25.append(sim.get_ploss())

print("List Of AVG Num Of Packets In System For K = 25: ", list_of_EN25)
print("Total Packets Dropped: ", sim.drops)
print("Total Packets Departed: ", sim.departures)
print("List Of Ploss Values For K = 25: ", list_of_pLOSS25)

# Running the simulator for k = 50 based on different lambda values calculated above.

for sims in range(len(rho_values)):
    sim = SimulatorMM1(transmission_rate=lambda_values[sims], link_rate=1000000, buffer_limit=k_values[2])
    sim.run_simulation(100)
    list_of_EN50.append(sim.get_en())
    list_of_pLOSS50.append(sim.get_ploss())

print("List Of AVG Num Of Packets In System For K = 50: ", list_of_EN50)
print("Total Packets Dropped: ", sim.drops)
print("Total Packets Departed: ", sim.departures)
print("List Of Ploss Values For K = 50: ", list_of_pLOSS50)

# Creating Graph For E[N]
# X-Axis: Rho
# Y-Axis: E[N] @ every K
x = rho_values
y1 = list_of_EN10
y2 = list_of_EN25
y3 = list_of_EN50
plt.plot(x, y1, marker = '^', label = 'K = %s'% k_values[0])
plt.plot(x, y2, marker = 'o', label = 'K = %s'% k_values[1])
plt.plot(x, y3, marker = '*', label = 'K = %s'% k_values[2])
plt.xticks(np.arange(x[0], x[9]+0.2, 0.1))
plt.yticks(np.arange(0, y3[9]+1, 5))
plt.title('Simulation Results: Question 6A')
plt.xlabel('Traffic Intensity p')
plt.ylabel('Average Number In System E[N]')
plt.legend()
plt.show()

# Creating Graph For pLOSS
# X-Axis: Rho
# Y-Axis: pLOSS @ every K
x = rho_values
y1 = list_of_pLOSS10
y2 = list_of_pLOSS25
y3 = list_of_pLOSS50
plt.plot(x, y1, marker = '^', label = 'K = %s'% k_values[0])
plt.plot(x, y2, marker = 'o', label = 'K = %s'% k_values[1])
plt.plot(x, y3, marker = '*', label = 'K = %s'% k_values[2])
plt.xticks(np.arange(x[0], x[9]+0.2, 0.1))
plt.yticks(np.arange(0, y3[9]+0.1, 0.1))
plt.title('Simulation Results: Question 6B')
plt.xlabel('Traffic Intensity p')
plt.ylabel('Probability Of Packet Loss pLoss')
plt.legend()
plt.show()
