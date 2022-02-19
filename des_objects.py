import numpy as np


class SimulatorMM1:  # The answer to question 2 is this simulator
    def __init__(self):  # This simulator declares the necessary variables
        self.arrivals = 0
        self.departures = 0
        self.observations = 0
        self.idle_counter = 0
        self.prev_departure_time = 0
        self.prev_service_time = 0
        self.events = []
        self.snapshots = []

    def generate_arrival_events(self):  # generating random arrival events with lambda = 75
        e = Event("arrival", np.random.exponential(1 / 75))
        e.set_length(np.random.exponential(2000))  # giving them a random length with average 2000 size
        self.events.append(e)  # appending them to the events queue

    def generate_observation_events(self):
        self.events.append(Event("observer", np.random.exponential(1 / 25)))

    def generate_departure_events(self, events: list):  # generating departure events based upon
        for event in events:  # the computed service time of the existing
            if event.type == "arrival":  # arrival events,
                service_time = event.length / 1000000  # which is found by dividing L (random packet length
                event.set_service_time(service_time)
                if event.time + event.service_time > self.prev_departure_time:  # queue is empty
                    departure_time = event.time + event.service_time  # with average 2000) by C (1 Mbps = 1000000)
                    self.prev_departure_time = departure_time
                    e = Event("departure", departure_time)
                    e.set_length(event.length)
                    self.events.append(e)
                else:
                    departure_time = self.prev_departure_time + event.service_time
                    self.prev_departure_time = departure_time
                    e = Event("departure", departure_time)
                    e.set_length(event.length)
                    self.events.append(e)
            else:
                pass

    def deque_events(self, event):
        if event.type == "arrival":
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
                [self.observations, self.arrivals - self.departures, self.arrivals, self.departures])
        else:
            self.snapshots.append(
                [self.observations, self.arrivals - self.departures, self.arrivals, self.departures])
        # print("observation event handled")

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


sim = SimulatorMM1()

print("generated and sorted (by time) events: ")
for i in range(1000):  # generating arrival events,
    sim.generate_arrival_events()  # observation events,
for i in range(5000):  # and departure events
    sim.generate_observation_events()

sim.events.sort(key=lambda event: event.time, reverse=False)  # sorting the events by time
sim.generate_departure_events(sim.events)
sim.events.sort(key=lambda event: event.time, reverse=False)  # sorting the events again, after adding the departures


sim.tabulate_results()

for i in range(len(sim.events)):  # de-queueing each event (popping the event at the 0th index)
    sim.deque_events(sim.events.pop(0))

print("Observer Event Log")
for snapshot in sim.snapshots:  # printing the log of snapshots from each observer event
    print("{:<30} {:<30} {:<35} {:<30}".format("Observer Event: " + str(snapshot[0]), "Packets in Queue: " + str(snapshot[1]), "Arrivals: " + str(snapshot[2]), "Departures: " + str(snapshot[3])))
