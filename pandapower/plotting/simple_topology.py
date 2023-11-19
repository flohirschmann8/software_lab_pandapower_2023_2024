#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 08:42:28 2021

@author: jhaack
"""

from pandapower.plotting import create_bus_collection, create_line_collection, \
                                create_trafo_collection, create_load_collection, \
                                create_gen_collection, create_sgen_collection, \
                                create_ext_grid_collection, create_line_switch_collection, \
                                create_generic_coordinates, \
                                draw_collections
import numpy as np
try:
    import pplog as logging
except ImportError:
    import logging

logger = logging.getLogger(__name__)



def simple_topology(net):
    if len(net.bus_geodata) == 0:
        logger.warning("No or insufficient geodata available --> Creating artificial coordinates." +
                       " This may take some time")
        create_generic_coordinates(net)

    buses_without_geodata = set(net.bus.index) - set(net.bus_geodata.index)
    if buses_without_geodata:
        raise UserWarning("The buses %s have no geodata specified. Please provide geodata for every bus!" % buses_without_geodata)

    bc = create_bus_collection(net, buses=net.bus.index, size=0.05)
    lc = create_line_collection(net, lines=net.line.index, use_bus_geodata=True)
    tc = create_trafo_collection(net, trafos=net.trafo.index, size=0.1)
    loc = create_load_collection(net, size=0.1)
    gc = create_gen_collection(net, size=0.1)
    sgc = create_sgen_collection(net, size=0.1, orientation=0.5*np.pi)
    ec = create_ext_grid_collection(net, size=.3)
    sc = create_line_switch_collection(net, size=0.1, distance_to_bus=0.2, zorder=10)

    draw_collections([bc, lc, tc[0], tc[1], loc[0], loc[1],
        gc[0], gc[1], sgc[0], sgc[1], ec[0], ec[1], sc])
