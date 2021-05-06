# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard

import hydra
import simpy

from dataclasses import dataclass

from mocasin.simulate.application import RuntimeDataflowApplication
from mocasin.simulate.system import RuntimeSystem


@dataclass
class SimulationResult:
    """Class for keeping the simulation results.

    Attributes:
        exec_time (float): total simulated time in ps.
        static_energy (float): static energy consumption in pJ.
        dynamic_energy (float): dynamic energy consumption in pJ.
    """

    exec_time: float
    static_energy: float
    dynamic_energy: float

    @property
    def total_energy(self) -> float:
        """total energy consumption in pJ"""
        if self.static_energy and self.dynamic_energy:
            return self.static_energy + self.dynamic_energy
        else:
            return None


class BaseSimulation:
    """A base class for handling a simulation

    Note that the ``run()`` method can only be called when
    the simulation object is used within a with block.
    Use something like the following example:

    .. code-block:: python

    with simulation:
        simulation.run()

    'with' is required in order to ensure that the simulation is setup properly
    before calling ``run()`` and finalized afterwards. These additional steps
    of setup and finalization are required in order for this class to be
    picklable. This, in turn, is required to allow parrallel execution
    of multiple simulations via multiprocessing. Now the problem is,
    that the simpy Environment is not picklable. Thus it cannot be a permanent
    attribute of this class. Therefore, the environment and also the runtime
    system are created during the setup phase (``__enter__``) and deleted
    again during finalization (``__exit__``).

    Attributes:
        env (~simpy.core.Environment): The simpy environment. This is only
            valid inside a with block and is ``None`` otherwise.
        platform (Platform): the platform that is simulated by this object
        system (RuntimeSystem): The runtime representation of the simulated
            system. This is only valid inside a with block and is ``None``
            otherwise.
        run: A callable object that triggers the actual simulation. If called
            outside of a with block, calling ``run()`` will raise a
            ``RuntimeError`` .
        result (SimulationResult): the result of the simulation run. This is
            initialized to ``None`` and updated after calling ``run()``

    Args:
        platform (Platform): the platform that is simulated by this object
    """

    def __init__(self, platform):
        self.env = None
        self.platform = platform
        self.system = None
        self.result = None
        self.run = self._default_run

    def __enter__(self):
        """Setup the simulation

        Creates the simpy environment ``env`` and the
        RuntimeSystem instance ``system``.
        """
        self.env = simpy.Environment()
        self.system = RuntimeSystem(self.platform, self.env)
        self.run = self._run
        return self

    def __exit__(self, type, value, traceback):
        """Finalize the simulation

        Resets ``env`` and ``system`` to ``None`` and ``run`` to
        ``_default_run``.
        """
        self.env = None
        self.system = None
        self.run = self._default_run

    def _run(self):
        """Run the simulation

        This needs to be overridden by a  subclass

        Raises:
            NotImplementedError
        """
        raise NotImplementedError()

    def _default_run(self):
        """Invalid implementation of run.

        Raises an RuntimeError notifying the caller of ``run()`` that
        ``run()`` may only be triggered within a with statement.

        Raises:
            RuntimeError
        """
        raise RuntimeError(
            "run() may only be called on a simulation object "
            "that is used in a with statement"
        )


class DataflowSimulation(BaseSimulation):
    """Handles the simulation of a single dataflow application

    Attributes:
        app (RuntimeApplication): Runtime instance of the application to be
            simulated. This is only valid inside a with block and is
            ``None`` otherwise.

    Args:
        platform (Platform): the platform that is simulated by this object
        graph (DataflowGraph): the dataflow application to be executed on the
            given ``platform``
        mapping (Mapping): a mapping of the ``graph`` to the ``platform``
        app_trace (DataflowTrace): a trace for the given ``graph``
    """

    def __init__(self, platform, graph, mapping, app_trace):
        super().__init__(platform)
        self.graph = graph
        self.mapping = mapping
        self.app_trace = app_trace
        self.app = None

    def __enter__(self):
        """Setup the simulation

        Calls `~BaseSimulation.__enter__()` and creates the graph application
        ``app``
        """
        super().__enter__()
        self.app = RuntimeDataflowApplication(
            name=self.graph.name,
            graph=self.graph,
            app_trace=self.app_trace,
            system=self.system,
        )
        return self

    def __exit__(self, type, value, traceback):
        """Finalize the simulation

        Calls `~BaseSimulation.__exit__()` and resets ``app`` to to ``None``.
        """
        super().__exit__(type, value, traceback)
        self.app = None

    def _run(self):
        """Run the simulation.

        May only be called once. Updates the :attr:`result` attribute.
        """
        if self.result is not None:
            raise RuntimeError("A DataflowSimulation may only be run once!")

        # start all schedulers
        self.system.start_schedulers()
        # start the application
        finished = self.env.process(self.app.run(self.mapping))
        # run the actual simulation until the application finishes
        self.env.run(finished)
        # check if all graph processes finished execution
        self.system.check_errors()
        # save the execution time
        self.result = SimulationResult(
            exec_time=self.env.now, static_energy=None, dynamic_energy=None
        )

        energy = self.system.calculate_energy()
        # If the power model is enabled, also save the energy consumption
        if energy:
            static_energy, dynamic_energy = energy
            self.result.static_energy = static_energy
            self.result.dynamic_energy = dynamic_energy

    @staticmethod
    def from_hydra(cfg):
        """Factory method.

        Instantiates :class:`DataflowSimulation` from a hydra configuration object.

        Args:
            cfg: a hydra configuration object
        """
        platform = hydra.utils.instantiate(cfg["platform"])
        trace = hydra.utils.instantiate(cfg["trace"])
        graph = hydra.utils.instantiate(cfg["graph"])
        rep = hydra.utils.instantiate(cfg["representation"], graph, platform)
        mapper = hydra.utils.instantiate(
            cfg["mapper"], graph, platform, trace, rep
        )
        mapping = mapper.generate_mapping()
        simulation = DataflowSimulation(platform, graph, mapping, trace)

        return simulation
