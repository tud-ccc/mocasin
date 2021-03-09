# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard


"""Contains classes that manage simulation of (dataflow) processes.

**Classes:**
    * :class:`ProcessState`: an enumeration of process states
    * :class:`RuntimeProcess`: base process model
    * :class:`RuntimeDataflowProcess`: dataflow process model
"""

import enum
import logging

from mocasin.common.trace import SegmentType
from mocasin.simulate.adapter import SimulateLoggerAdapter


log = logging.getLogger(__name__)


@enum.unique
class ProcessState(enum.Enum):
    """Denotes the state of a runtime process."""

    CREATED = 0
    """The process is instantiated but not started yet."""
    READY = 1
    """The process is ready and waits to be scheduled."""
    RUNNING = 2
    """The process is currently being executed."""
    BLOCKED = 3
    """The process is blocked and waits for a resource to become available."""
    FINISHED = 4
    """The process completed its execution."""


class RuntimeProcess(object):
    """Runtime instance of a process.

    Implements a process state machine and provides an API for triggering valid
    transitions from outside (e.g. by a scheduler). This class is designed to
    be a base class and does not provide any functionality. Subclasses should
    override :func:`workload` to implement the process functionality.

    **State Machine:**

        **States:** See :class:`ProcessState`.

        **Events:**
          * :attr:`~created`: Triggered on entering the
            :const:`~ProcessState.CREATED` state.
          * :attr:`~ready`: Triggered on entering the
            :const:`~ProcessState.READY` state.
          * :attr:`~running`: Triggered on entering the
            :const:`~ProcessState.RUNNING` state.
          * :attr:`~finished`: Triggered on entering the
            :const:`~ProcessState.FINISHED` state.
          * :attr:`~blocked`: Triggered on entering the
            :const:`~ProcessState.BLOCKED` state.

        **Entry Actions:**
          * :func:`_cb_created`:  Callback of :attr:`created`
          * :func:`_cb_ready`:  Callback of :attr:`ready`
          * :func:`_cb_running`:  Callback of :attr:`running`
          * :func:`_cb_finished`: Callback of :attr:`finished`
          * :func:`_cb_blocked`: Callback of :attr:`blocked`

        **Transitions:**
          * :func:`start`: Transition from :const:`~ProcessState.CREATED` to
            :const:`~ProcessState.READY`
          * :func:`activate`: Transition from :const:`~ProcessState.READY` to
            :const:`~ProcessState.RUNNING`
          * :func:`_deactivate`: Transition from :const:`~ProcessState.RUNNING`
            to :const:`~ProcessState.READY`
          * :func:`_finish`: Transition from :const:`~ProcessState.RUNNING` to
            :const:`~ProcessState.FINISHED`
          * :func:`_block`: Transition from :const:`~ProcessState.RUNNING` to
            :const:`~ProcessState.BLOCKED`
          * :func:`unblock`: Transition from :const:`~ProcessState.BLOCKED` to
            :const:`~ProcessState.READY`

    Note:
        This class should never be instantiated directly. Instead a subclass
        that overrides :func:`workload` should be defined.
    Attributes:
        name (str): the process name
        app (RuntimeApplication): the application this process is part of
        _state (ProcessState): The current process state.
        _log (SimulateLoggerAdapter): an logger adapter to print messages with
            simulation context
        processor (Processor): the processor that the processes currently runs
            on. This attribute is only valid in the
            :const:`~ProcessState.RUNNING` state.
        created (~simpy.events.Event): An event that triggers on entering the
            :const:`~ProcessState.CREATED` state.
        ready (~simpy.events.Event): An event that triggers on entering the
            :const:`~ProcessState.READY` state.
        running (~simpy.events.Event): An event that triggers on entering the
            :const:`~ProcessState.RUNNING` state.
        finished (~simpy.events.Event): An event that triggers on entering the
            :const:`~ProcessState.FINISHED` state.
        blocked (~simpy.events.Event): An event that triggers on entering the
            :const:`~ProcessState.BLOCKED` state.
    Args:
        name (str): The process name (should be unique within the system)
        app (RuntimeApplication): the application this process is part of
    """

    def __init__(self, name, app):
        self.name = name
        self.app = app
        self._state = ProcessState.CREATED
        self.processor = None
        self._log = SimulateLoggerAdapter(log, self.full_name, self.env)

        # setup the events
        self.created = self.env.event()
        self.created.callbacks.append(self._cb_created)
        self.ready = self.env.event()
        self.ready.callbacks.append(self._cb_ready)
        self.running = self.env.event()
        self.running.callbacks.append(self._cb_running)
        self.finished = self.env.event()
        self.finished.callbacks.append(self._cb_finished)
        self.blocked = self.env.event()
        self.blocked.callbacks.append(self._cb_blocked)

        # internal event for requesting preemption
        self._preempt = self.env.event()
        # internal event for requesting termination
        self._kill = self.env.event()

        # record the process creation int the simulation trace
        if self.app.system.app_trace_enabled:
            self.trace_writer.begin_duration(
                self.app.name, self.name, "CREATED", category="Process"
            )

    @property
    def env(self):
        """The simpy environment"""
        return self.app.env

    @property
    def full_name(self):
        """Full name including the application name"""
        return f"{self.app.name}.{self.name}"

    @property
    def trace_writer(self):
        """The system's trace writer"""
        return self.app.system.trace_writer

    def _transition(self, state_name):
        """Helper function for convenient state transitions.

        Updates the process state (:attr:`_state`), triggers the corresponding
        event, and reinitializes the event.

        Args:
            state_name(str): name of the state to be transitioned to
        """
        if not hasattr(ProcessState, state_name):
            raise RuntimeError(
                "Tried to transition to an invalid state (%s)" % (state_name)
            )

        event_name = state_name.lower()
        cb_name = "_cb_" + state_name.lower()
        assert hasattr(self, event_name)
        assert hasattr(self, cb_name)

        # record the transition in the simulation trace
        if self.app.system.app_trace_enabled:
            self.trace_writer.end_duration(
                self.app.name, self.name, self._state.name, category="Process"
            )
            self.trace_writer.begin_duration(
                self.app.name, self.name, state_name, category="Process"
            )

        # update the state
        self._state = getattr(ProcessState, state_name)

        old_event = getattr(self, event_name)
        old_event.succeed(self)

        new_event = self.env.event()
        new_event.callbacks.append(getattr(self, "_cb_" + event_name))
        setattr(self, event_name, new_event)

    def check_state(self, state):
        """Compare to internal state

        Args:
            state(ProcessState): the state to compare to
        Return:
            bool: ``True`` if states are equal
        """
        return self._state == state

    def start(self, event=None):
        """Start the process.

        Transition to the :const:`~ProcessState.READY` state. This function may
        be called directly, but can also be registered as a callback to a simpy
        event.

        Args:
            event(~simpy.events.Event): unused (only required for usage as a
                 simpy callback)
        Raises:
            AssertionError: if not in :const:`ProcessState.CREATED` state
        """
        assert self._state == ProcessState.CREATED
        self._log.debug("Process starts.")
        self.processor = None
        self._transition("READY")

    def activate(self, processor):
        """Start the process execution.

        Transition to the :const:`~ProcessState.RUNNING` state and update
        :attr:`processor`.

        Args:
            processor (Processor): The processor that executes the workload
        Raises:
            AssertionError: if not in :const:`ProcessState.READY` state
        """
        assert self._state == ProcessState.READY
        self._log.debug(
            "Start workload execution on processor %s", processor.name
        )
        self.processor = processor
        self._transition("RUNNING")

    def _deactivate(self):
        """Halt the process execution.

        Transition to the :const:`~ProcessState.READY` state and update
        :attr:`processor`.

        Raises:
            AssertionError: if not in :const:`ProcessState.RUNNING` state
        """
        assert self._state == ProcessState.RUNNING
        self._log.debug(
            "Stop workload execution on processor %s", self.processor.name
        )
        self.processor = None
        self._transition("READY")

    def preempt(self):
        """Request deactivation of a running process

        Raises:
            AssertionError: if not in :const:`ProcessState.RUNNING` state
        """
        assert self._state == ProcessState.RUNNING
        self._log.debug(
            "Preempt workload execution on processor %s", self.processor.name
        )
        old_event = self._preempt
        self._preempt = self.env.event()
        old_event.succeed()

    def _finish(self):
        """Terminate the process.

        Transition to the :const:`~ProcessState.FINISHED` state.

        Raises:
            AssertionError: if not in :const:`ProcessState.RUNNING` state
        """
        self._log.debug("Workload execution finished.")
        self.processor = None
        self._transition("FINISHED")

    def kill(self):
        """Request termination of a running process"""
        self._log.debug("Kill request")
        if self._state == ProcessState.RUNNING:
            old_event = self._kill
            self._kill = self.env.event()
            old_event.succeed()
        else:
            self._finish()

    def _block(self):
        """Block the process.

        Interrupt the process execution by transitioning to the
        :const:`~ProcessState.BLOCKED` state.
        """
        assert self._state == ProcessState.RUNNING
        self._log.debug("Process blocks")
        self.processor = None
        self._transition("BLOCKED")

    def unblock(self):
        """Unblock the process.

        Transition to the :const:`~ProcessState.READY` if currently in
        :const:`ProcessState.BLOCKED` state. Does nothing if currently in
        :const:`ProcessState.FINISHED` state.

        Raises:
            AssertionError: if not in :const:`ProcessState.BLOCKED` or
            :const:`ProcessState.FINISHED` state
        """
        if self._state == ProcessState.FINISHED:
            return

        assert self._state == ProcessState.BLOCKED
        self._log.debug("Process unblocks")
        self.processor = None
        self._transition("READY")

    def _cb_ready(self, event):
        """Callback invoked upon entering the :const:`~ProcessState.READY`
        state.

        Args:
            event (~simpy.events.Event): unused (only required to provide the
                callback interface)
        """
        assert self._state == ProcessState.READY
        self._log.debug("Entered READY state")

    def _cb_running(self, event):
        """Callback invoked upon entering the :const:`~ProcessState.RUNNING`
        state.

        Args:
            event (~simpy.events.event): unused (only required to provide the
                callback interface)
        """
        assert self._state == ProcessState.RUNNING
        self._log.debug("Entered RUNNING state")

    def _cb_finished(self, event):
        """Callback invoked upon entering the :const:`~ProcessState.FINISHED`
        state.

        Args:
            event (~simpy.events.event): unused (only required to provide the
                callback interface)
        """
        assert self._state == ProcessState.FINISHED
        self._log.debug("Entered FINISHED state")

    def _cb_blocked(self, event):
        """Callback invoked upon entering the :const:`~ProcessState.BLOCKED`
        state.

        Args:
            event (~simpy.events.event): unused (only required to provide the
                callback interface)
        """
        assert self._state == ProcessState.BLOCKED
        self._log.debug("Entered BLOCKED state")

    def _cb_created(self, event):
        """Callback invoked upon entering the :const:`~ProcessState.CREATED`
        state.

        Args:
            event (~simpy.events.event): unused (only required to provide the
                callback interface)
        """
        assert self._state == ProcessState.CREATED
        self._log.debug("Entered CREATED state")

    def workload(self):
        """Implements the process functionality.

        This is just a stub and may not be called. This has to be overridden by
        a subclass.

        Raises:
            NotImplementedError
        """
        raise NotImplementedError(
            "This function does not provide any functionality and should "
            "never be called. Override it in a subclass!"
        )


class RuntimeDataflowProcess(RuntimeProcess):
    """Runtime instance of a dataflow process.

    Attributes:
        _channels(dict[str, RuntimeChannel]): Dictionary of channel names and
            there corresponding runtime object. This only includes channels
            that may be accessed by this process.
        _trace (generator): a generator of trace segments
        _current_segment: The trace segment that is currently
            processed
    Args:
        name (str): The process name. This should be unique across applications
            within the same system.
        process_trace (generator): a generator of process trace segments
        app (RuntimeApplication): the application this process is part of
    """

    def __init__(self, name, process_trace, app):
        super().__init__(name, app)
        log.debug(
            "initialize new dataflow runtime process (%s)", self.full_name
        )

        self._channels = {}
        self._trace = process_trace
        self._current_segment = None
        self._remaining_compute_cycles = None

        # lets the workload method know whether it is run for the first time
        # or whether it is resumed
        self._is_running = False

    def connect_to_incomming_channel(self, channel):
        """Connect the process to an incoming runtime channel

        Also makes the process a sink of the channel.

        Args:
            channel (RuntimeChannel): the channel to connect to
        """
        self._channels[channel.name] = channel
        channel.add_sink(self)

    def connect_to_outgoing_channel(self, channel):
        """Connect the process to an outgoing runtime channel

        Also makes the process the source of the channel.

        Args:
            channel (RuntimeChannel): the channel to connect to
        """
        self._channels[channel.name] = channel
        channel.set_src(self)

    def workload(self):
        """Replay a dataflow execution trace

        Iterates over all segments in the execution trace and performs actions
        as specified by the segments. By returning, the execution
        terminates. However, this does not mean that it is actually complete. A
        process may also return when it blocks or was deactivated. Then the
        execution is resumed on the next call of this method.
        """

        self._init_workload()

        while self._current_segment is not None:
            # The preempt and kill events will be overwritten once
            # triggered. Thus we keep references to the original events here.
            preempt = self._preempt
            kill = self._kill

            s = self._current_segment
            if s.segment_type == SegmentType.COMPUTE:
                for compute_event in self._handle_compute():
                    yield compute_event
            elif s.segment_type == SegmentType.READ_TOKEN:
                consume_finished = self._handle_read_segment()
                if consume_finished is None:
                    # if we get None this means the consume operation blocked
                    # and we need to return from workload
                    return
                # Otherwise we got an event that indicates the end of the
                # consume operation and we simply wait for it
                yield consume_finished
            elif s.segment_type == SegmentType.WRITE_TOKEN:
                produce_finished = self._handle_write_segment()
                if produce_finished is None:
                    # if we get None this means the consume operation blocked
                    # and we need to return from workload
                    return
                # Otherwise we got an event that indicates the end of the
                # produce operation and we simply wait for it
                yield produce_finished
            else:
                raise RuntimeError(
                    f"Encountered an unknown segment type! ({s.segment_type})"
                )

            # Stop processing if we where preempted or killed
            if kill.triggered:
                self._finish()
                self._log.debug("process was killed")
                return
            if preempt.triggered:
                self._deactivate()
                self._log.debug("process was preempted")
                return

            # move on to the next segment
            self._update_current_segment()

        # reached the end of the trace
        self._log.debug("process terminates")
        self._finish()

    def _init_workload(self):
        assert self.check_state(ProcessState.RUNNING)

        if self._is_running:
            # we are resuming from an earlier workload execution, nothing to do
            self._log.debug("resume workload execution")
        else:
            # we start up workload execution for the first time and need
            # to initialize the current trace segment
            self._log.debug("start workload execution")
            self._is_running = True
            self._update_current_segment()
            self._remaining_compute_cycles = None

    def _update_current_segment(self):
        # updated the current segment to the next segment in the trace
        # set to None if we reached the end of the trace
        try:
            self._current_segment = next(self._trace)
        except StopIteration:
            # reached the end of the trace
            self._current_segment = None

    def _handle_read_segment(self):
        # Consume tokens from a channel. Unlike the processing, this operation
        # cannot easily be preempted. There are two problems here.  First,
        # consume and produce are considered atomic operations by our
        # algorithm. If they could be interrupted, both operations would need
        # to implement a synchronization strategy.  Second, it is unclear what
        # preempting a consume or produce operation means. The simulation does
        # not know Which part of the consume/produce costs is actual processing
        # by a CPU and which part is due to asynchronous operations (e.g., a
        # DMA or the memory architecture) that would not be affected by an
        # interrupt.  Therefore, both consume and produce ignore any preemption
        # requests and process it only after the operation completes.
        s = self._current_segment
        c = self._channels[s.channel]
        self._log.debug(f"read {s.num_tokens} tokens from channel {s.channel}")
        if c.can_consume(self, s.num_tokens):
            return self.env.process(c.consume(self, s.num_tokens))
        else:
            self._log.debug("not enough tokens available -> block")
            self._block()
            self.env.process(c.wait_for_tokens(self, s.num_tokens))
            return None

    def _handle_write_segment(self):
        # Produce tokens on a channel. Similar to consume above, this is
        # considered as an atomic operation and an preemption request is only
        # processed after this operation completes.
        s = self._current_segment
        c = self._channels[s.channel]
        self._log.debug(f"write {s.num_tokens} tokens to channel {s.channel}")
        if c.can_produce(self, s.num_tokens):
            return self.env.process(c.produce(self, s.num_tokens))
        else:
            self._log.debug("not enough slots available -> block")
            self._block()
            self.env.process(c.wait_for_slots(self, s.num_tokens))
            return None

    def _handle_compute(self):
        # The preempt and kill events will be overwritten once triggered. Thus
        # we keep references to the original events here.
        preempt = self._preempt
        kill = self._kill

        s = self._current_segment

        if self._remaining_compute_cycles is None:
            cycles = s.processor_cycles[self.processor.type]
        else:
            cycles = self._remaining_compute_cycles

        self._log.debug(f"process for {cycles} cycles")
        ticks = self.processor.ticks(cycles)

        timeout = self.env.timeout(ticks)
        start = self.env.now

        # process until computation completes (timeout) or until the
        # process is preempted
        yield self.env.any_of([timeout, preempt, kill])

        # if the timeout was processed, the computation completed
        if timeout.processed:
            self._remaining_compute_cycles = None
        elif preempt.processed:
            # Calculate how many cycles where executed until the process was
            # preempted. Note that the preemption can occur in between full
            # cycles in our simulation. We lose a bit of precision here, by
            # allowing preemption in between cycles and rounding the number of
            # processed cycles to an integer number. However, the introduced
            # error should be marginal.
            ticks_processed = self.env.now - start
            ratio = float(ticks_processed) / float(ticks)
            cycles_processed = int(round(float(cycles) * ratio))

            self._remaining_compute_cycles = cycles - cycles_processed
            assert self._remaining_compute_cycles >= 0
            self._log.debug(
                f"process was deactivated after {cycles_processed} cycles"
            )
