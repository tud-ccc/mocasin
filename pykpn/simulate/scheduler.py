# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from ..common import logging

log = logging.getLogger(__name__)


class RuntimeScheduler(object):
    """Represents the simulated runtime instance of a scheduler.

    :ivar str name: the scheduler name
    :ivar _env: the simpy environment
    :ivar _processor: the processor managed by this scheduler
    :type _processor: Processor
    :ivar _processes: list of runtime processes managed by this scheduler
    :type _processes: list[RuntimeProcess]
    """

    def __init__(self, platform_scheduler, env):
        """Initialize a runtime scheduler.

        :param platform_scheduler: scheduler object as defined by the platform
        :type platform_scheduler: Scheduler
        :param env: the simpy environment
        """
        self.name = platform_scheduler.name
        log.debug('Initialize new runtime scheduler (%s)' % self.name)

        self._env = env

        # TODO implement multi-processor scheduling
        if len(platform_scheduler.processors) > 1:
            raise RuntimeError(
                'Multi-processor scheduling is not yet supported!')
        self._processor = platform_scheduler.processors[0]

        self._processes = []
        self._policy = None
        self._policy_param = None

    def add_application(self, application, mapping_info):
        """Parse the mapping info of an application and configure this
        scheduler accordingly.

        :param application: The application to be parsed
        :type application: RuntimeApplication
        :param mapping_info: mapping_info for this scheduler and application
        :type mapping_info: SchedulerMappingInfo
        """
        log.debug('%s: Add the application %s', self.name, application.name)
        logging.inc_indent()
        if self._policy is None:
            self._policy = mapping_info.policy
            self._policy_param = mapping_info.param
            log.debug('%s: configure %s policy', self.name, self._policy.name)
        else:
            if self._policy.name != mapping_info.policy.name:
                log.warning('%s: The scheduling policy was already set to %s '
                            'but the application %s requested a different '
                            'policy (%s) -> force old policy', self.name,
                            self._policy.name, application.name,
                            mapping_info.policy.name)
            elif self._policy_param != mapping_info._policy_param:
                log.warning('%s: The application %s requested a different '
                            'scheduling policy parameter than the application '
                            'before -> use old parameter',
                            self.name, application.name)

        for p in application.processes():
            log.debug('%s: Append process %s', self.name, p.name)
            self._processes.append(p)
        logging.dec_indent()
