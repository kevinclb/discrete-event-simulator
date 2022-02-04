import simpy


# Generator function that defines the working of the traffic light
# "timeout()" function makes next yield statement wait for a
# given time passed as the argument
def traffic_light(env):
    while True:
        print("Light turns GRN at " + str(env.now))

        # Light is green for 25 seconds
        yield env.timeout(25)

        print("Light turns YEL at " + str(env.now))

        # Light is yellow for 5 seconds
        yield env.timeout(5)

        print("Light turns RED at " + str(env.now))

        # Light is red for 60 seconds
        yield env.timeout(60)

    # env is the environment variable


env = simpy.Environment()

# The process defined by the function Traffic_Light(env)
# is added to the environment
env.process(traffic_light(env))

# The process is run for the first 180 seconds (180 is not included)
env.run(until=180)
