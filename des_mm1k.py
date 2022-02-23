import numpy as np
from decimal import Decimal


class Event:
    # initialize an event with an event type parameter, and an event time
    # event_type should be one of 3 strings: "arrival", "observer", "departure"
    def __init__(self, event_type, time):
        self.type = event_type
        self.time = time
        self.packet_length = 0
        self.service_time = 0
        self.departure_time = 0

    def set_packet_length(self, length):
        self.packet_length = length
        return self

    def set_service_time(self):
        self.service_time = round(Decimal(self.packet_length / 1000000), 8)
        return self

    def get_time(self):
        return self.time


class SimulatorMM1K:
    def __init__(self, transmission_rate, link_rate, buffer_size):
        # Declaring the necessary variables for this simulator
        # including total time, counters, and structures for holding the events (pre-queue)
        # and structures for holding event data such as an event_log and snapshots
        # event logs are created after every handler function,
        # and snapshots are created only during handle_observer_events() function
        self.total_time = 0
        self.total_idle_time = 0
        self.arrivals = 0
        self.departures = 0
        self.drops = 0
        self.observations = 0
        self.idle_counter = 0
        self.link_rate = link_rate
        self.events = []
        self.event_log = []
        self.snapshots = []
        self.transmission_rate = transmission_rate
        self.latest_departure = 0
        self.buffer_limit = buffer_size

    # generate_arrival_events() is a function that takes an integer number as a parameter
    # then, it creates that number of arrival packets with random exponential arrival times
    # with lamda (set by user) and random exponential length with L = 2000
    # it appends all these events to self.events (the DES).
    def generate_arrival_events(self, number, lamda):
        for i in range(number):
            e = Event("arrival", np.random.exponential(1 / lamda))
            e.packet_length = np.random.exponential(self.link_rate)
            e.service_time = e.packet_length / self.transmission_rate
            self.events.append(e)
        pass

    # generate_observer_events() is a function that takes an integer number as a parameter
    # then, it creates that number of observer events with random exponential times
    # with (1 / 5 * lamda). Lamda is set by the user. It then appends the observer
    # events to self.events (the DES).
    def generate_observer_events(self, number, lamda):
        for i in range(number):
            self.events.append(Event("observer", np.random.exponential(1 / (5 * lamda))))
        pass

    # handle_arrival_events() first increments the total time
    # then, it takes an event and either drops it or adds it to the queue,
    # depending on whether the queue has size
    # then, it generates a departure event with a departure time that is dependent

    def handle_arrival_events(self, event):
        self.total_time += abs(event.time - self.total_time)

        # if the queue is full, drop the packet, increment the drop counter,
        # and create a log of the drop in the event log
        if self.arrivals - self.departures >= self.buffer_limit:
            self.drops += 1
            self.event_log.append(["drop " + str(self.drops), event.time])
            pass

        # if the queue is empty
        # increment the arrival counter, and create a log of that arrival
        # calculate the departure time to equal event time + service time
        # create a new departure event and add it to the DES (self.events)
        # then sort the DES to keep events in order.
        elif self.arrivals - self.departures == 0:
            self.arrivals += 1
            self.event_log.append(["arrival " + str(self.arrivals), event.time])
            departure_time = event.time + event.service_time
            e = Event("departure", departure_time)
            self.events.append(e)
            self.events.sort(key=lambda item: item.get_time())
            self.latest_departure = departure_time

        # if the queue has packets but is not full
        # check if the latest departure time is greater than the current arrival time
        # create a departure time based on the greater of the two
        # then create a departure event with that departure time
        # finally, append that departure event to the DES (self.events)
        # and sort the DES.
        else:
            if self.latest_departure > event.time:
                departure_time = self.latest_departure + event.service_time
            else:
                departure_time = event.time + event.service_time
            self.arrivals += 1
            e = Event("departure", departure_time)
            self.events.append(e)
            self.events.sort(key=lambda item: item.get_time())
            self.event_log.append(["arrival " + str(self.arrivals), event.time])

    # handle_departure_events() increments the departure counter,
    # and adds a departure event to the event log.
    def handle_departure_events(self, event):
        self.departures += 1
        self.event_log.append(["departure " + str(self.departures), event.time])

    # handle_observer_events() increments the observation counter,
    # adds an observation event to the event log,
    # and if the queue is empty, should increment the idle counter and
    # record the appropriate idle time metrics.
    def handle_observer_events(self, event):
        self.observations += 1
        self.event_log.append(["observer " + str(self.observations + 1), event.time])
        # if the queue is empty, increment idle counter
        if self.arrivals - self.departures == 0:
            self.idle_counter += 1
            self.total_idle_time += abs(event.time - self.event_log[len(self.event_log) - 1][1])
        # TODO: add metrics to self.snapshot list here

    # run the simulation with this function.
    def run_simulation(self):
        while len(self.events) > 0:
            if len(self.events) == 0:
                break
            current_event = self.events.pop(0)
            if current_event.type == "arrival":
                self.handle_arrival_events(current_event)
            if current_event.type == "observer":
                self.handle_observer_events(current_event)
            if current_event.type == "departure":
                self.handle_departure_events(current_event)
            pass
        self.event_log.append(["simulation over. total time:", self.total_time])
        print("simulation run  successfully.")

    # test_queue() helps us to test the queue by populating
    # it with a specified number of packets,
    # set by the user with the "queue_size" parameter.
    # each event occurs at a preset time with a preset increment for predictability.
    def test_queue(self, queue_size):
        for i in range(queue_size):
            self.events.append(Event(
                "arrival", round(Decimal(2 * i * 0.00001), 8)).set_packet_length(2000).set_service_time())
        for i in range(queue_size):
            self.events.append(Event(
                "observer", round(Decimal(2 * i * 0.00000001), 8)))

    # print_event_log() will print metrics from the simulation.
    def print_event_log(self):
        for event in self.event_log:
            print("event: " + str(event))
        print("total num of events: " + str(len(self.event_log)))
        print("arrivals: ", self.arrivals)
        print("drops: ", self.drops)
        print("departures:", self.departures)
        print("observations: ", self.observations)
        print("idle counter: ", self.idle_counter)
        print("events remaining: " + str(len(self.events)))
        print("total time: " + str(self.total_time))


sim = SimulatorMM1K(transmission_rate=1000000, link_rate=2000, buffer_size=10)
sim.generate_arrival_events(number=10000, lamda=75)
sim.generate_observer_events(number=50000, lamda=75)
sim.events.sort(key=lambda item: item.get_time())
sim.run_simulation()
sim.print_event_log()
