import xml.etree.ElementTree as ET
import logging

from pytrm import KpnApplication
from pytrm import KpnChannel
from pytrm import KpnProcess
from pytrm import Mapping
from pytrm import SchedulerInfo
from pytrm import ChannelInfo
from scheduler import SchedulingPolicy

log = logging.getLogger(__name__)


class SlxApplication(KpnApplication):

    def __init__(self, name, pngraph):
        self.name = name
        tree = ET.parse(pngraph)
        xmlroot = tree.getroot()

        log.info('Start parsing the PnGraph')

        for channel in xmlroot.iter('PNchannel'):
            name = channel.find('Name').text
            token_size = int(channel.find('EntrySizeHint').text)
            log.debug(''.join([
                'Found the channel ', name, ' with a token size of ',
                str(token_size), ' bytes']))
            self.channels.append(KpnChannel(name, token_size))

        for process in xmlroot.iter('PNprocess'):
            name = process.find('Name').text
            outgoing = []
            incoming = []

            for c in process.find('PNin').iter('Expr'):
                incoming.append(c.text)
            for c in process.find('PNout').iter('Expr'):
                outgoing.append(c.text)

            log.debug('Found the process ' + name)
            log.debug('It reads from the channels ' + str(incoming) + ' ...')
            log.debug('and writes to the channels ' + str(outgoing))

            kpn_process = KpnProcess(name)
            self.processes.append(kpn_process)

            for cn in outgoing:
                channel = None
                for c in self.channels:
                    if cn == c.name:
                        channel = c
                        break
                assert channel is not None

                self.connectProcessToOutgoingChannel(kpn_process, channel)

            for cn in incoming:
                channel = None
                for c in self.channels:
                    if cn == c.name:
                        channel = c
                        break
                assert channel is not None

                self.connectProcessToIncomingChannel(kpn_process, channel)
        log.info('Done parsing the PnGraph')


class SlxMapping(Mapping):

    def __init__(self, mapping_file):
        tree = ET.parse(mapping_file)
        self.xmlroot = tree.getroot()

        # parse the scheduler descriptors
        for desc in self.xmlroot.findall('SingleSchedulerDesc'):
            s = SchedulerInfo()
            id = desc.get('ID')
            s.name = desc.get('Name')
            s.policy = SchedulingPolicy[desc.get('SchedulingPolicy')]
            s.processNames = []
            for p in desc.iter('Process'):
                s.processNames.append(p.get('Name'))
            s.processorNames = []
            for s2g in self.xmlroot.iter('Scheduler2Group'):
                if id == s2g.get('SchedulerID'):
                    groupID = s2g.get('GroupID')
                    for group in self.xmlroot.iter('PeGroup'):
                        if groupID == group.get('GroupId'):
                            l = group.get('Processors').split(' ')
                            s.processorNames = l
            self.schedulers.append(s)

        # parse the channel descriptors
        for bound in self.xmlroot.iter('FifoBound'):
            c = ChannelInfo()
            c.name = bound.get('Fifo')
            c.capacity = int(bound.get('Bound'))

            for mapping in self.xmlroot.iter('ChannelMapping'):
                if c.name == mapping.get('PnChannel'):
                    c.primitive = mapping.get('CommPrimitive')
                    c.processorFrom = mapping.get('ProcessorFrom')
                    c.viaMemory = mapping.get('Memory')
                    c.processorTo = mapping.get('ProcessorTo')
            self.channels.append(c)
