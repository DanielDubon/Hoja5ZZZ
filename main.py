import random
import simpy
import statistics


class OS(object):

    def __init__(self, env, ram_available, cpu_cores, instructions):
        self.env = env
        self.ram_available = simpy.Container(env, init=ram_available, capacity=ram_available)
        self.cpu_cores = simpy.Resource(cpu_cores)
        self.instructions = instructions

    def new(self, process):
        print("Asignacion de RAM a proceso" + str(process) + " en t= " + str(env.now))

        if self.ram_available.level == 0:
            yield self.ram_available.get(random.randint(1, 11))
            print("Se asigno la RAM")
            yield self.ready(process)

        else:
            while self.ram_available.capacity == 0:
                print("Esperando a que la ram se libere...")

    def ready(self, process):
        print("El proceso " + str(process) + " esta listo para ser ejecutado en t= " + str(env.now))
        yield self.running(process)

    def running(self, process):
        print("El proceso " + str(process) + " se esta ejecutando en t= " + str(env.now))
        remaining_instructions = self.instructions
        while remaining_instructions > 0:
            with self.cpu_cores.request() as request:
                yield request
                if remaining_instructions < 3:
                    yield self.env.timeout(1)
                    remaining_instructions -= remaining_instructions
                else:
                    yield self.env.timeout(1)
                    remaining_instructions -= 3

            # Determine whether the process terminates, waits, or returns to ready
            if remaining_instructions == 0:
                print("Proceso " + str(process) + " terminado en t=" + str(env.now))
            else:
                io_or_ready = random.randint(1, 21)
                if io_or_ready == 1:
                    print("Proceso " + str(process) + " en espera de I/O en t=" + str(env.now))
                    yield self.env.timeout(1)
                    yield self.ready(process)
                elif io_or_ready == 2:
                    print("Proceso " + str(process) + " regresa a estado listo en t=" + str(env.now))
                    yield self.ready(process)

    def Software_usage(self, process):
        ram_needed = random.randint(1, 11)
        print("Process {} needs {} units of RAM".format(process, ram_needed))
        yield self.ram_available.get(ram_needed)
        print("Process {} got {} units of RAM at time {}".format(process, ram_needed, self.env.now))
        yield self.env.process(self.new(process))


env = simpy.Environment()
OperativeSystem = OS(env, 100, 1, 10)
processes = 100
for i in range(processes):
    env.process(OperativeSystem.Software_usage(i))


env.process(OperativeSystem.Software_usage(2))
env.run(until=20)

