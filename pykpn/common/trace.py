# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


class TraceSegment(object):
    """Represents a segment in a process' execution trace

    :ivar processing_cycles:
        Duration (in cycles) of a processing segment. None if the segment does
        not contain any computations.
    :type processing_cycles: int or None
    :ivar read_from_channel:
        Name of the channel to read from at the end of the segment (after
        processing). None if no read access is to be performed. If not None,
        write_to_channel must be None.
    :type read_from_channel: str or None
    :ivar write_to_channel:
        Name of the channel to write to at the end of the segment (after
        processing). None if no write access is to be performed. If not None,
        read_from_channel must be None.
    :type write_to_channel: str or None
    :ivar n_tokens:
        Number of tokens to be read from or written to a channel. None if
        neither a write access nor a read access is to be performed at the end
        of the segment.
    :type n_tokens: int or None
    :ivar bool terminate:
        If True, this is the last segment of the execution trace.
    """

    def __init__(self):
        """Initialize a neutral (does not do anything) tracs segment)"""
        self.processing_cycles = None
        self.read_from_channel = None
        self.write_to_channel = None
        self.n_tokens = None
        self.terminate=False

    def sanity_check(self):
        """Perform a series of sanity checks on the object"""
        if (self.read_from_channel is not None and
            self.write_to_channel is not None):
            raise RuntimeError('A trace segment may not contain both a read '
                               'and a write access')
        if (self.n_tokens is None and (self.read_from_channel is not None or
                                       self.write_to_channel is not None)):
            raise RuntimeError('Trace segments contains a channel access but '
                               'the number of tokens is not specified!')


class TraceGenerator(object):
    """Creates trace segments

    This class is intended as a base class. A superclass could extend the
    functionality by generating random traces or reading traces from a file.
    """

    def get_next_entry(self, process_name, processor_type):
        """Return the next trace segment.

        Returns the next trace segment for a process running on a processor of
        the specified type (the segments could differ for different processor
        types). This should be overridden by a subclass. The default behaviuour
        is to return None

        :param str process_name:
            name of the process that a segment is requested for
        :param str processor_type:
            the processor type that a segment is requested for
        :returns: the next trace segment or None if there is none
        :rtype: TraceSegment or None
        """
        return None
