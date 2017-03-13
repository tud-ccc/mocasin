# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import xml.etree.ElementTree as ET
import logging

from pytrm import KpnApplication
from pytrm import KpnChannel
from pytrm import KpnProcess

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
