# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import simpy

import pytest
from mocasin.common.platform import Primitive
from mocasin.simulate.process import ProcessState


@pytest.fixture
def running_process(env, kpn_process, processor, mocker):
    kpn_process.workload = mocker.Mock()  # disable the normal workload
    kpn_process.start()
    env.run()
    kpn_process.activate(processor)
    env.run()
    env.process(kpn_process.workload())
    env.run()
    return kpn_process


@pytest.fixture
def blocked_process(env, running_process):
    p = running_process
    p._block()
    env.run()
    assert p.check_state(ProcessState.BLOCKED)
    return p


class TestRuntimeChannel:
    def test_init(self, channel):
        assert channel.name == "test_chan"
        assert channel._src is None
        assert len(channel._sinks) == 0
        assert len(channel._fifo_state) == 0

    def test_set_src(self, channel, mocker):
        process = mocker.Mock()
        channel.set_src(process)
        assert channel._src is process
        with pytest.raises(AssertionError):
            channel.set_src(process)

    def test_add_sink(self, channel, mocker):
        process = mocker.Mock()
        channel.add_sink(process)
        assert process in channel._sinks
        assert channel._fifo_state[process.name] == 0

    def test_can_produce(self, channel, mocker):
        src = mocker.Mock()
        sink1 = mocker.Mock()
        sink2 = mocker.Mock()
        with pytest.raises(ValueError):
            channel.can_produce(src, 1)
        channel.set_src(src)
        with pytest.raises(RuntimeError):
            assert channel.can_produce(src, 1)
        channel.add_sink(sink1)
        channel.add_sink(sink2)
        for i in range(1, 10):
            if i < 5:
                assert channel.can_produce(src, i)
            else:
                assert not channel.can_produce(src, i)
        channel._fifo_state[sink1.name] = 2
        for i in range(1, 10):
            if i < 3:
                assert channel.can_produce(src, i)
            else:
                assert not channel.can_produce(src, i)
        channel._fifo_state[sink2.name] = 3
        for i in range(1, 10):
            if i < 2:
                assert channel.can_produce(src, i)
            else:
                assert not channel.can_produce(src, i)

        with pytest.raises(ValueError):
            list(channel.can_produce(src, -1))
        with pytest.raises(ValueError):
            list(channel.can_produce(src, 0))
        with pytest.raises(ValueError):
            list(channel.can_produce(src, 2.5))

    def test_can_consume(self, channel, mocker):
        src = mocker.Mock()
        sink1 = mocker.Mock()
        sink2 = mocker.Mock()
        with pytest.raises(ValueError):
            channel.can_consume(sink1, 1)
        with pytest.raises(ValueError):
            channel.can_consume(sink2, 1)
        channel.add_sink(sink1)
        channel.add_sink(sink2)
        with pytest.raises(RuntimeError):
            channel.can_consume(sink1, 1)
        with pytest.raises(RuntimeError):
            channel.can_consume(sink2, 1)
        channel.set_src(src)
        for i in range(1, 10):
            assert not channel.can_consume(sink1, i)
            assert not channel.can_consume(sink2, i)
        channel._fifo_state[sink1.name] = 2
        for i in range(1, 10):
            if i < 3:
                assert channel.can_consume(sink1, i)
            else:
                assert not channel.can_consume(sink1, i)
            assert not channel.can_consume(sink2, i)
        channel._fifo_state[sink2.name] = 4
        for i in range(1, 10):
            if i < 3:
                assert channel.can_consume(sink1, i)
            else:
                assert not channel.can_consume(sink1, i)
            if i < 5:
                assert channel.can_consume(sink2, i)
            else:
                assert not channel.can_consume(sink2, i)

        with pytest.raises(ValueError):
            list(channel.can_consume(sink1, -1))
        with pytest.raises(ValueError):
            list(channel.can_consume(sink1, 0))
        with pytest.raises(ValueError):
            list(channel.can_consume(sink1, 2.5))

    def produce_after(self, env, chan, ticks, num):
        # produces num tokens after ticks on chan
        yield env.timeout(ticks)
        for key in chan._fifo_state:
            chan._fifo_state[key] += num
        chan.tokens_produced.succeed()
        chan.tokens_produced = env.event()

    def consume_after(self, env, chan, ticks, num):
        # produces num tokens after ticks on chan
        yield env.timeout(ticks)
        for key in chan._fifo_state:
            chan._fifo_state[key] -= num
        chan.tokens_consumed.succeed()
        chan.tokens_consumed = env.event()

    @pytest.mark.parametrize("num", range(1, 4))
    def test_wait_for_tokens(self, env, blocked_process, channel, num, mocker):
        sink1 = blocked_process
        sink2 = mocker.Mock()
        src = mocker.Mock()

        channel.set_src(src)
        channel.add_sink(sink1)
        channel.add_sink(sink2)

        wait_process = env.process(
            channel.wait_for_tokens(blocked_process, num)
        )

        env.run()
        assert not wait_process.processed

        # produce num - 1 times
        for i in range(1, num):
            env.process(self.produce_after(env, channel, 10, 1))
            env.run()
            assert not wait_process.processed
            assert sink1.check_state(ProcessState.BLOCKED)

        # final produce
        env.process(self.produce_after(env, channel, 10, 1))
        env.run()
        assert wait_process.processed
        assert wait_process.ok
        assert sink1.check_state(ProcessState.READY)

    @pytest.mark.parametrize("num", range(1, 4))
    def test_wait_for_slots(self, env, blocked_process, channel, num, mocker):
        sink1 = mocker.Mock()
        sink2 = mocker.Mock()
        src = blocked_process

        channel.set_src(src)
        channel.add_sink(sink1)
        channel.add_sink(sink2)

        # full in the beginning
        channel._fifo_state[sink1.name] = 4
        channel._fifo_state[sink2.name] = 4

        wait_process = env.process(channel.wait_for_slots(blocked_process, num))

        env.run()
        assert not wait_process.processed

        # consume num - 1 times
        for i in range(1, num):
            env.process(self.consume_after(env, channel, 10, 1))
            env.run()
            assert not wait_process.processed
            assert sink1.check_state(ProcessState.BLOCKED)

        # consume produce
        env.process(self.consume_after(env, channel, 10, 1))
        env.run()
        assert wait_process.processed
        assert wait_process.ok
        assert sink1.check_state(ProcessState.READY)

    def test_consume_invalid(self, channel, mocker):
        sink1 = mocker.Mock()
        sink2 = mocker.Mock()
        src = mocker.Mock()

        channel.set_src(src)
        channel.add_sink(sink1)
        channel.add_sink(sink2)

        with pytest.raises(AssertionError):
            list(channel.consume(sink1, 1))

    def test_produce_invalid(self, channel, mocker):
        sink1 = mocker.Mock()
        sink2 = mocker.Mock()
        src = mocker.Mock()

        channel.set_src(src)
        channel.add_sink(sink1)
        channel.add_sink(sink2)

        # full in the beginning
        channel._fifo_state[sink1.name] = 4
        channel._fifo_state[sink2.name] = 4

        with pytest.raises(AssertionError):
            list(channel.produce(src, 1))

    def test_consume(self, env, channel, running_process, mocker):
        sink1 = running_process
        sink2 = mocker.Mock()
        src = mocker.Mock()

        channel.set_src(src)
        channel.add_sink(sink1)
        channel.add_sink(sink2)

        # fill up
        channel._fifo_state[sink1.name] = 4
        channel._fifo_state[sink2.name] = 4

        # setup the primitive
        prim = Primitive("test_prim")
        channel._primitive = prim

        # sink1 processor not added yet -> should fail
        with pytest.raises(RuntimeError):
            list(channel.consume(sink1, 1))
        # add the processor to the primitive
        prim.add_consumer(sink1.processor, [])

        # first try
        start = env.now
        event = channel.tokens_consumed
        process = env.process(channel.consume(sink1, 1))
        env.run()
        assert event.ok
        assert process.ok
        assert channel._fifo_state[sink1.name] == 3
        # should not consume any time since we did not add any communication
        # phases
        assert env.now - start == 0

        # try again with some communication phases
        phases = []
        for i in range(1, 6):
            p = mocker.Mock()
            p.get_costs.side_effect = lambda x, i=i: i * 10
            p.resources = []
            phases.append(p)
        prim.consume_phases[sink1.processor.name] = phases

        event = channel.tokens_consumed
        process = env.process(channel.consume(sink1, 2))
        env.run()
        assert event.ok
        assert process.ok
        assert channel._fifo_state[sink1.name] == 1
        assert env.now - start == 150
        for p in phases:
            p.get_costs.assert_called_once_with(16)

        # and again with resources
        resources = []
        for p in phases:
            for i in range(3):
                r = mocker.Mock()
                r.simpy_resource = simpy.Resource(env)
                resources.append(r)
                p.resources.append(r)

        start = env.now
        event = channel.tokens_consumed
        process = env.process(channel.consume(sink1, 1))

        # peek into each phase
        env.run(env.now + 1)
        x = 10
        for p in phases:
            for r in p.resources:
                # all resources of the phase should be hold
                assert r.simpy_resource.count == 1
            env.run(env.now + x)
            x += 10
            for r in p.resources:
                # all resources of the phase should be released
                assert r.simpy_resource.count == 0

        assert event.ok
        assert process.ok
        assert channel._fifo_state[sink1.name] == 0
        assert env.now - start == 151

        assert all([r.simpy_resource.count == 0 for r in resources])

    def test_produce(self, env, channel, running_process, mocker):
        sink1 = mocker.Mock()
        sink2 = mocker.Mock()
        src = running_process

        channel.set_src(src)
        channel.add_sink(sink1)
        channel.add_sink(sink2)

        # setup the primitive
        prim = Primitive("test_prim")
        channel._primitive = prim

        # src processor not added yet -> should fail
        with pytest.raises(RuntimeError):
            list(channel.produce(src, 1))

        # add the src processor to the primitive
        prim.add_producer(src.processor, [])

        # first try
        start = env.now
        event = channel.tokens_produced
        process = env.process(channel.produce(src, 1))
        env.run()
        assert event.ok
        assert process.ok
        assert channel._fifo_state[sink1.name] == 1
        assert channel._fifo_state[sink2.name] == 1
        # should not consume any time since we did not add any communication
        # phases
        assert env.now - start == 0

        # try again with some communication phases
        phases = []
        for i in range(1, 6):
            p = mocker.Mock()
            p.get_costs.side_effect = lambda x, i=i: i * 10
            p.resources = []
            phases.append(p)
        prim.produce_phases[src.processor.name] = phases

        event = channel.tokens_produced
        process = env.process(channel.produce(src, 2))
        env.run()
        assert event.ok
        assert process.ok
        assert channel._fifo_state[sink1.name] == 3
        assert channel._fifo_state[sink2.name] == 3
        assert env.now - start == 150
        for p in phases:
            p.get_costs.assert_called_once_with(16)

        # and again with resources
        resources = []
        for p in phases:
            for i in range(3):
                r = mocker.Mock()
                r.simpy_resource = simpy.Resource(env)
                resources.append(r)
                p.resources.append(r)

        start = env.now
        event = channel.tokens_produced
        process = env.process(channel.produce(src, 1))

        # peek into each phase
        env.run(env.now + 1)
        x = 10
        for p in phases:
            for r in p.resources:
                # all resources of the phase should be hold
                assert r.simpy_resource.count == 1
            env.run(env.now + x)
            x += 10
            for r in p.resources:
                # all resources of the phase should be released
                assert r.simpy_resource.count == 0

        assert event.ok
        assert process.ok
        assert channel._fifo_state[sink1.name] == 4
        assert channel._fifo_state[sink2.name] == 4
        assert env.now - start == 151

        assert all([r.simpy_resource.count == 0 for r in resources])
