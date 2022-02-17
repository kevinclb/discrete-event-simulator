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
        self.events.append(Event("observer", np.random.exponential(1 / 75)))

    def generate_departure_events(self, events: list):  # generating departure events based upon
        for event in events:  # the computed service time of the existing
            if event.type == "arrival":  # arrival events,
                service_time = event.length / 1000000  # which is found by dividing L (random packet length
                departure_time = event.time + service_time  # with average 2000) by C (1 Mbps = 1000000)
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
        print("arrival event handled")

    def handle_departure_event(self):
        self.departures += 1
        print("departure event handled")

    def handle_observation_event(self):
        self.observations += 1
        if self.arrivals == self.departures:
            self.idle_counter += 1  # if queue is empty, we are incrementing the idle counter.
            self.snapshots.append({"number of packets at observation " + str(self.observations)+ ": " : self.arrivals - self.departures})
        else:
            self.snapshots.append({"number of packets at observation "+ str(self.observations)+ ": ": self.arrivals - self.departures})
        print("observation event handled")


class Event:  # Event class: has variables type, time,
    def __init__(self, event_type, event_time):  # and an optional length variable (for packets)
        self.type = event_type
        self.time = event_time
        self.length = 0

    def __str__(self):  # for returning a string representation of
        return "event type: " + str(self.type) + "        time: " + str(self.time) + "      packet length: " + str(
            self.length)

    def set_length(self, packet_length):
        self.length = packet_length


sim = SimulatorMM1()

print("generated and sorted (by time) events: ")
for i in range(10):  # generating arrival events,
    sim.generate_arrival_events()  # observation events,
for i in range(30):  # and departure events
    sim.generate_observation_events()
sim.generate_departure_events(sim.events)
sim.events.sort(key=lambda event: event.time, reverse=False)  # sorting the events by time

for event in sim.events:  # printing the contents of each event (for double-checking)
    print(str(event))

for i in range(len(sim.events)):  # de-queueing each event (popping the event at the 0th index)
    sim.deque_events(sim.events.pop(0))

for snapshot in sim.snapshots:  # printing the log of snapshots from each observer event
    print(snapshot)

print(sim.arrivals, " ", sim.departures)
