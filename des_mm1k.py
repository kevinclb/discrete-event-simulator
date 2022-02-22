import numpy as np
from decimal import Decimal
# import random as rand
# from numpy import sort


def rounded_decimal(num):
    return round(Decimal(num), 4)


class Packet:
    def __init__(self):
        self.id: int
        self.length = np.random.exponential(2000)  # random length exponential distribution L = 2000
        self.arrival_time = rounded_decimal(np.random.exponential(75))  # arrival time is random with rate lambda = 125
        self.service_time = rounded_decimal(
            self.length / 1000000)  # divide packet length / link rate to calculate service time
        self.departure_time = 0  # departure time will be calculated later
        pass


class Observation:
    def __init__(self, simulation, observation_time):
        self.system_time = simulation.time
        self.arrivals = simulation.arrivals
        self.departures = simulation.departures
        self.idle_counter = simulation.idle_counter
        self.packets_generated = simulation.packets_generated
        self.packets_dropped = simulation.packets_dropped
        self.queue_length = len(simulation.queue)
        self.observation_time = observation_time
        pass

    def set_observation_time(self, time):
        self.observation_time = time


class SimulationMM1K:
    def __init__(self, buffer_limit, transmission_rate):
        self.arrivals = 0
        self.departures = 0
        self.idle_counter = 0
        self.time = rounded_decimal(0)
        self.packets_generated = 0
        self.packets_dropped = 0
        self.queue = []
        self.observation_times = []
        self.observation_data = []
        self.packets = []
        self.buffer_limit = buffer_limit
        self.transmission_rate = transmission_rate
        pass

    def generate_packets(self, count):  # generate "count" number of packets, sort them by arrival time
        for i in range(count):
            self.packets.append(Packet())
        self.packets.sort(key=lambda packet: packet.arrival_time, reverse=False)
        self.packets_generated = count
        pass

    def queue_packet(self, packet):
        if len(self.queue) < self.buffer_limit:  # if the queue has room, add a packet and set it's service time
            self.arrivals += 1
            packet.id = self.arrivals
            packet.service_time = rounded_decimal(packet.length / self.transmission_rate)
            if len(self.queue) == 0:        # calculate it's service time based on whether it already contains a packet
                packet.departure_time = rounded_decimal(packet.arrival_time + packet.service_time)
            else:
                packet.departure_time = rounded_decimal(
                    max(self.queue[(len(self.queue) - 1)].departure_time, packet.arrival_time) + packet.service_time)
            self.queue.append(packet)
            print("queueing packet")
        else:
            self.packets_dropped += 1
            print("dropping packet")
            pass

    def generate_observation_times(self, number_of_observations):
        # print("returning an array filled with random observation times")
        arr = []
        for i in range(number_of_observations):
            arr.append(rounded_decimal(np.random.exponential(75)))
        arr.sort()
        self.observation_times = arr
        pass

    def dequeue_packet(self):               # pop packet from index 0 (the front of the queue) and increment departures
        self.queue.pop(0)
        self.departures += 1
        pass

    def observe(self, observation_time):    # create an Observation object which contains a snapshot of the system data
        o = Observation(self, observation_time)
        if len(self.queue) == 0:
            self.idle_counter += 1
        self.observation_data.append(o)
        pass

    def run_simulation(self, simulation_time):
        while self.time <= rounded_decimal(simulation_time):
            if len(self.packets) > 0 and (self.time == self.packets[0].arrival_time):
                self.queue_packet(self.packets.pop(0))
                pass
            if len(self.queue) > 0 and (self.time == self.queue[0].departure_time):
                self.dequeue_packet()
                pass
            if len(self.observation_times) > 0 and (self.time == self.observation_times[0]):
                self.observe(self.observation_times.pop(0))
            self.time += rounded_decimal(.0001)

    def print_log(self):
        print("total number of snapshots: " + str(len(self.observation_data)))
        print("total number of arrivals: " + str(self.arrivals))
        print("total number of departures: " + str(self.departures))
        print("total number of generated packets: " + str(self.packets_generated))
        print("total number of dropped packets: " + str(self.packets_dropped))
        print("idle counter: " + str(self.idle_counter))

    def print_packets(self):
        for packet in self.packets:
            print("Packet arrival time: " + str(packet.arrival_time) + "    Packet length: " + packet.length)

    def print_queue(self):
        print("current queue status")
        for packet in self.queue:
            print("Packet id: " + str(packet.id) + "Packet arrival time: " + str(packet.arrival_time) + "Packet service time: " + str(packet.service_time) + "Packet departure time: " + str(packet.departure_time))


sim = SimulationMM1K(buffer_limit=5, transmission_rate=1000000)
sim.generate_packets(100)
sim.generate_observation_times(number_of_observations=500)
sim.run_simulation(1000)
sim.print_log()
sim.print_queue()
for observations in sim.observation_data:
    assert observations.observation_time == observations.system_time
# print(sim.observation_times)
# for packet in sim.packets:
#     print(packet.id, end=" ")
#
# sim.generate_packets(100)
#
# sim.run_simulation(1000)

# for packet in sim.packets:
#     print("packet arrival time: " + packet.arrival_time)
# sim.print_packets()
#
# print(sim.time)
# print(sim.packets[0].arrival_time)
# print(sim.idle_counter)
# array_packets = []
# for i in range(10):
#     array_packets.append(Packet())

# for packet in array_packets:
#     print(packet.length)
