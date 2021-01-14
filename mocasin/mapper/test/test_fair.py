from mocasin.mapper.fair import StaticCFS, gen_trace_summary
from mocasin.common.mapping import Mapping
from mocasin.common.trace import TraceSegment


class MockTraceGenerator(object):
    def __init__(self, proc_names, core_types, lookup_function, max_length=1):
        self.cores = core_types
        self.procs = proc_names
        self.lookup = lookup_function
        self.max_length = max_length
        self.num_lookups = {}
        self.reset()

    def reset(self):
        for core in self.cores:
            for proc in self.procs:
                self.num_lookups[(proc, core)] = 0

    def next_segment(self, proc_name, core_type):
        self.num_lookups[(proc_name, core_type)] += 1
        if self.num_lookups[(proc_name, core_type)] >= self.max_length:
            return TraceSegment(terminate=True)
        else:
            return TraceSegment(
                process_cycles=self.lookup((proc_name, core_type))
            )


def test_gen_trace_summary(kpn, platform):
    const_value = 3
    num_iter = 10
    proc_names = [proc.name for proc in kpn.processes()]
    core_types = [core.type for core in platform.processors()]
    const_func = lambda _: const_value
    trace = MockTraceGenerator(
        proc_names, core_types, const_func, max_length=num_iter
    )
    trace_summary = gen_trace_summary(kpn, platform, trace)
    for core in core_types:
        for proc in kpn.processes():
            assert trace_summary[(proc, core)] == const_value * (num_iter - 1)

    for core in core_types:
        for proc in kpn.processes():
            single_comb = (
                lambda x: (x[0] == core) * (x[1] == proc.name) * const_value
            )
            trace = MockTraceGenerator(
                proc_names, core_types, single_comb, max_length=num_iter
            )
            trace_summary = gen_trace_summary(kpn, platform, trace)

            for other_core in core_types:
                for other_proc in kpn.processes():
                    val = trace_summary[(other_proc, other_core)]
                    assert (
                        other_core == core
                        and other_proc == proc
                        and val == (num_iter - 1) * const_value
                    ) or (val == 0)


def test_map_to_core(kpn, platform):
    cfs = StaticCFS(platform)
    for core in platform.processors():
        for proc in kpn.processes():
            mapping = Mapping(kpn, platform)
            cfs.map_to_core(mapping, proc, core)
            assert mapping._process_info[proc.name].affinity == core
