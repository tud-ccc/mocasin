# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import json
from recordclass import recordclass


"""Helper record used to manage thread ids within processes"""
ProcessInfo = recordclass("ProcessInfo", "pid tids tid_counter")


class TraceWriter:
    """A class for writing simulation traces in json format.

    The generated trace uses Google's `trace format <(https://docs.google.com/document/d/1CvAClvFfyA5R-PhYUmn5OOQtYMH4h6I0nSsKchNAySU/preview)>`_.
    The trace can be opend with Chrome's built-in trace viewer. Simply type
    :code:`about://tracing` in the address line.

    The Google trace format uses the notion of processes and threads to group
    events. This class uses the same notation, but does not enforce that the
    given names are actually processes or threads. This allows custom grouping
    as suits the application.

    Attributes:
        _env: the simpy environment
        _trace (list(dict)): the generated json trace
        _processes (dict(str, ProcessInfo)): all known processes
        _pid_counter (int): counter used to generate new process IDs
    Args:
        env: the simpy environment
    """

    def __init__(self, env):
        self._env = env
        self._trace = []
        self._processes = {}
        self._pid_counter = 0

    def _add_new_process(self, name):
        """Register a new process and assign an ID

        Args:
            name (str): name of the process to be added
        """
        assert name not in self._processes
        pid = self._pid_counter
        self._pid_counter += 1
        self._trace.append({
            "name": "process_name",
            "ph": "M",
            "pid": pid,
            "args": {
                "name": name
            }
        })
        self._processes[name] = ProcessInfo(pid, {}, 0)

    def _add_new_thread(self, process_info, name):
        """Register a new thread and assign an ID

        Args:
            process_info (ProcessInfo): process info record of the process
                the new thread belongs to
            name (str): name of the thread to be added
        """
        pid = process_info.pid
        tid = process_info.tid_counter
        process_info.tid_counter += 1
        self._trace.append({
            "name": "thread_name",
            "ph": "M",
            "pid": pid,
            "tid": tid,
            "args": {
                "name": name
            }
        })
        process_info.tids[name] = tid

    def _get_pid(self, process):
        """Retrieve the ID of a given process

        If the process is not yet registered, it is added to :ref:`_processes`
        and a new ID will be assigned.

        Args:
            process (str): name of process the to be looked up

        Returns:
            int: the process ID
        """
        if process not in self._processes:
            self._add_new_process(process)

        return self._processes[process].pid

    def _get_tid(self, process, thread):
        """Retrieve the ID of a given thread

        If the thread is not yet registered, it is added to corresponding
        process info and a new ID will be assigned.

        Args:
            process (str): name of the process the thread is part of
            thread (str): name of the thread to be looked up

        Returns:
            int: the thread ID
        """
        if process not in self._processes:
            self._add_new_process(process)
        process_info = self._processes[process]

        if thread not in process_info.tids:
            self._add_new_thread(process_info, thread)
        return process_info.tids[thread]

    def begin_duration(self, process, thread, name, category=None, args=None):
        """Generate a begin duration event.

        This marks the beginning of a duration. The duration can be ended
        by calling :ref:`end_duration`.

        Args:
            process (str): name of the process this event is generated for
            thread (str): name of the thread this event is generated for
            name (str): name of the event to be generated
            category (str, optional): an optional category
            args (dict(str, str)): an optional dictionary of additional
                arguments that the event should be annotated with
        """
        pid = self._get_pid(process)
        tid = self._get_tid(process, thread)
        event = {
            "name": name,
            "ph": "B",
            "ts": self._env.now / 1000000.0,
            "pid": pid,
            "tid": tid,
        }
        if category is not None:
            event["cat"] = category
        if args is not None:
            args["args"] = args

        self._trace.append(event)

    def end_duration(self, process, thread, name, category=None, args=None):
        """Generate an end duration event.

        This marks the end of a duration. The duration can be started
        by calling :ref:`begin_duration`.

        Args:
            process (str): name of the process this event is generated for
            thread (str): name of the thread this event is generated for
            name (str): name of the event to be generated
            category (str, optional): an optional category
            args (dict(str, str)): an optional dictionary of additional
                arguments that the event should be annotated with
        """
        pid = self._get_pid(process)
        tid = self._get_tid(process, thread)
        event = {
            "name": name,
            "ph": "E",
            "ts": self._env.now / 1000000.0,
            "pid": pid,
            "tid": tid,
        }
        if category is not None:
            event["cat"] = category
        if args is not None:
            args["args"] = args

        self._trace.append(event)

    def update_counter(self, process, counter, data, category=None):
        """Generate a counter event.

        This updates the data of a counter. Each counter may provide data form
        multiple series. Be sure to copy the data passed to this method in case
        your program modifies the data later on.

        Args:
            process (str): name of the process this counter is generated for
            name (str): name of the counter event to be generated
            data (dict(str, int)): a data dictionary, each entry represents one
                data series.
            category (str, optional): an optional category
        """
        pid = self._get_pid(process)
        event = {
            "name": counter,
            "ph": "C",
            "ts": self._env.now / 1000000.0,
            "pid": pid,
            "args": data
        }
        if category is not None:
            event["cat"] = category

        self._trace.append(event)

    def write_trace(self, path):
        """Write the trace to a file

        Args:
            path (str): path to the output file
        """
        with open(path, 'w') as f:
            json.dump(self._trace, f)
