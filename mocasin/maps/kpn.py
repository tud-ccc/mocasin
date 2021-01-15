# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import xml.etree.ElementTree as ET

from mocasin.util import logging
from mocasin.common.kpn import KpnChannel, KpnGraph, KpnProcess


log = logging.getLogger(__name__)


class MapsKpnGraph(KpnGraph):
    def __init__(self, name, xml_file):
        super().__init__(name)

        log.info("Start parsing the PnGraph")

        log.debug("Reading from file: %s" % xml_file)
        tree = ET.parse(xml_file)
        xmlroot = tree.getroot()

        for channel in xmlroot.iter("PNchannel"):
            name = channel.find("Name").text
            token_size = int(channel.find("EntrySizeHint").text)
            log.debug(
                "".join(
                    [
                        "Found the channel ",
                        name,
                        " with a token size of ",
                        str(token_size),
                        " bytes",
                    ]
                )
            )
            self.add_channel(KpnChannel(name, token_size))

        for process in xmlroot.iter("PNprocess"):
            name = process.find("Name").text
            outgoing = []
            incoming = []

            for c in process.find("PNin").iter("Expr"):
                incoming.append(c.text)
            for c in process.find("PNout").iter("Expr"):
                outgoing.append(c.text)

            log.debug("Found the process " + name)
            log.debug("It reads from the channels " + str(incoming) + " ...")
            log.debug("and writes to the channels " + str(outgoing))

            kpn_process = KpnProcess(name)
            self.add_process(kpn_process)

            for cn in outgoing:
                channel = None
                for c in self.channels():
                    if cn == c.name:
                        channel = c
                        break
                assert channel is not None
                kpn_process.connect_to_outgoing_channel(channel)

            for cn in incoming:
                channel = None
                for c in self.channels():
                    if cn == c.name:
                        channel = c
                        break
                assert channel is not None
                kpn_process.connect_to_incomming_channel(channel)
        log.info("Done parsing the PnGraph")
