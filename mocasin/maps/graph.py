# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard


import xml.etree.ElementTree as ET

from hydra.utils import to_absolute_path

from mocasin.util import logging
from mocasin.common.graph import DataflowChannel, DataflowGraph, DataflowProcess


log = logging.getLogger(__name__)


class MapsDataflowGraph(DataflowGraph):
    def __init__(self, name, xml_file):
        super().__init__(name)

        log.info("Start parsing the PnGraph")

        log.debug("Reading from file: %s" % xml_file)
        tree = ET.parse(to_absolute_path(xml_file))
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
            self.add_channel(DataflowChannel(name, token_size))

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

            process = DataflowProcess(name)
            self.add_process(process)

            for cn in outgoing:
                channel = None
                for c in self.channels():
                    if cn == c.name:
                        channel = c
                        break
                assert channel is not None
                process.connect_to_outgoing_channel(channel)

            for cn in incoming:
                channel = None
                for c in self.channels():
                    if cn == c.name:
                        channel = c
                        break
                assert channel is not None
                process.connect_to_incomming_channel(channel)
        log.info("Done parsing the PnGraph")
