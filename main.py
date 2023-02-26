import random
import simpy
import statistics

time_running = []
totaltime = 0


class OS(object):

    def __init__(self, env, ram_available, cpu_cores):
        self.env = env
        self.ram_available = simpy.Container(env, init=ram_available, capacity=ram_available)
        self.cpu_cores = simpy.Resource(env, cpu_cores)
        self.cpu_queue = simpy.Resource(env, cpu_cores)

    def Software_usage(self, process, instructions, ram_needed):
        global totaltime
        yield env.timeout(random.expovariate(1.0 / 10))
        total_time = env.now
        # Ejecucion NEW
        print("Process {} needs {} units of RAM".format(process, ram_needed))
        yield self.ram_available.get(ram_needed)
        print("Process {} got {} units of RAM at time {}".format(process, ram_needed, self.env.now))

        # Ejecucion Ready
        print("Process {} has {} number of instructions".format(process, instructions))

        # Ejecucion running
        instructionsDone = 0
        instructionsLeft = instructions
        cpu_speed = 3

        while instructionsLeft != 0:
            with self.cpu_cores.request() as request:
                yield request

            if cpu_speed > instructionsLeft:
                instructionsDone = instructionsDone + instructionsLeft
                instructionsLeft = 0
            else:
                instructionsLeft = instructionsLeft - cpu_speed
                instructionsDone = instructionsDone + cpu_speed

            print("Process {}  has finished {} of {} instructions until this cpu clock cycle at t = {}".format(process,
                                                                                                               instructionsDone,
                                                                                                               instructions,
                                                                                                               env.now))
            yield env.timeout(1)

            finished_status = random.randint(1, 2)
            if finished_status == 1 and (instructionsLeft != 0):
                print("Process {} got the status WAITING".format(process))
                with self.cpu_queue.request() as request:
                    yield request
                    yield env.timeout(1)
            elif finished_status == 2 and (instructionsLeft != 0):
                print("Process {} got the status Ready".format(process))

        #Returning RAM

        yield self.ram_available.put(ram_needed)
        print("Process {} returned {} of RAM".format(process,ram_needed))
        totaltime += env.now - total_time
        time_running.append(totaltime)


# Configuracion de simulacion
env = simpy.Environment()
ram_available = 100
cpu_cores = 1
OperativeSystem = OS(env, ram_available, cpu_cores)
random.seed(10)

# Ejecucion de simulacion
processes = 20
for i in range(processes):
    instructions = random.randint(1, 10)
    ram_needed = random.randint(1, 10)
    env.process(OperativeSystem.Software_usage(i, instructions, ram_needed))
env.run()
Mean_time = statistics.mean(time_running)
Stdev = statistics.stdev(time_running)

print("MEAN TIME: " + str(Mean_time))
print("STANDARD DEVIATION " + str(Stdev))

