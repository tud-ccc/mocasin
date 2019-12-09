from tgff.tgffSimulation import *
from pykpn.mapper.random import RandomMapping
import simpy
import timeit

def main():
    kpn = KpnGraphFromTgff("../graphs/auto-indust-cords.tgff", 'TASK_GRAPH_0')
    
    platform = PlatformFromTgff('bus', 0, "../graphs/auto-indust-cords.tgff", 2)
    mapping = RandomMapping(kpn, platform)
    trace = TraceGeneratorWrapper("../graphs/auto-indust-cords.tgff")

    env = simpy.Environment()
    app = RuntimeKpnApplication(name=kpn.name,
                                kpn_graph=kpn,
                                mapping=mapping,
                                trace_generator=trace,
                                env=env,)
    system = RuntimeSystem(platform, [app], env)

    start = timeit.default_timer()
    system.simulate()
    stop = timeit.default_timer()

    exec_time = float(env.now) / 1000000000.0
    print('Total simulated time: ' + str(exec_time) + ' ms')
    print('Total simulation time: ' + str(stop - start) + ' s')

    system.check_errors()
    
if __name__ == '__main__':
    main()