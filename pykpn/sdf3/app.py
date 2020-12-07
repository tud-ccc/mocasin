# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import logging

from pykpn.common.kpn import KpnChannel, KpnGraph, KpnProcess
from pykpn.sdf3 import _sdf_parser

log = logging.getLogger(__name__)


class Sdf3Graph(KpnGraph):
    def __init__(self, xml_file, name=None):
        log.info("Start parsing the SDF3 graph")

        # load the xml
        with open(xml_file) as f:
            sdf3 = _sdf_parser.CreateFromDocument(f.read())
            if sdf3.type != "sdf":
                raise RuntimeError(
                    f"Cannot parse {sdf3.type} graphs. "
                    "Only SDF graphs are supported."
                )
            graph = sdf3.applicationGraph

        # set the name and initialize parent class
        if name is None:
            name = graph.sdf.name
        super().__init__(name)

        # add all processes
        for actor in graph.sdf.actor:
            log.debug(f"Add process {name}.{actor.name}")
            self.add_process(KpnProcess(actor.name))

        # add all channels
        for sdf_channel in graph.sdf.channel:
            c_name = sdf_channel.name

            # find channel properties
            c_props = None
            for props in graph.sdfProperties.channelProperties:
                if props.channel == c_name:
                    c_props = props
                    break
            if c_props is None:
                raise RuntimeError(
                    "Did not find sdf3 channel properties for channel "
                    f"{name}.{c_name}"
                )

            # add the new channel
            # FIXME token size unit
            log.debug(
                f"Add channel {name}.{c_name} with a token size of "
                "{c_props.token_size} bytes"
            )
            token_size = next(iter(c_props.tokenSize))
            channel = KpnChannel(sdf_channel.name, int(token_size.sz))
            self.add_channel(channel)

            src_process = self.find_process(sdf_channel.srcActor)
            src_process.connect_to_outgoing_channel(channel)
            log.debug(
                f"Process {name}.{src_process.name} writes to channel "
                f"{name}.{c_name}"
            )

            sink_process = self.find_process(sdf_channel.dstActor)
            sink_process.connect_to_incomming_channel(channel)
            log.debug(
                f"Process {name}.{src_process.name} reads from channel "
                f"{name}.{c_name}"
            )

        log.info("Done parsing the SDF3 graph")
