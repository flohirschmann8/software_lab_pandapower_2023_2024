

import pandapower as pp

import pandas as pd
import numpy as np
import pandapower.topology as top
import pandapower.plotting as plot
import matplotlib.pyplot as plt
### first we import the grid

# net = pp.from_json(r"C:\Users\alfak\OneDrive\Desktop\GitHubProjects\software_lab_pandapower_2023_2024\exercises\abdalrhman\exercise_4\net_exercise_4.json")
# net = pp.from_json(filename= 'net_exercise_4.json')

net = pp.from_json(r".\exercises\abdalrhman\exercise_4\net_exercise_4.json")



plot.simple_plot(net, respect_switches=True)

#### inspect all area
mg = top.create_nxgraph(net)

buses_area1 = list(top.connected_component(mg, bus=0))
buses_area2 = list(top.connected_component(mg, bus=45))
buses_area3 = list(top.connected_component(mg, bus=89))
buses_area4 = list(top.connected_component(mg, bus=134))

####### I am choosing the area 4 to be my case study


### grid assets description of Area 4

## indeces and number of the bueses
idx_buses = buses_area4
n_of_busus = len(idx_buses)
## indeces and number of the lines

idx_lines = net.line.index[net.line.from_bus.isin(idx_buses) & net.line.to_bus.isin(idx_buses)]
n_of_lines = len(idx_lines)
## indeces and  number of the static generators

idx_sgens = net.sgen.index[net.sgen.bus.isin(idx_buses)]
n_of_sgens = len(idx_sgens)

## indeces and number of the loads

idx_loads = net.load.index[net.load.bus.isin(idx_buses)]
n_of_loads = len(idx_loads)

##  indeces and number of the switches

idx_switches = net.switch.index[net.switch.bus.isin(idx_buses)& net.switch.element.isin(idx_lines)]
n_of_switches = len(idx_switches)
##  indeces and number of the Trafos

idx_trafos = net.trafo.index[net.trafo.hv_bus.isin(idx_buses)]
n_of_trafos = len(idx_trafos)

##  indeces and number of the ext grids

idx_ext_grids = net.ext_grid.index[net.ext_grid.bus.isin(idx_buses)]
n_of_ext_grids = len(idx_ext_grids)







### Grid area 4 consist of 45 buses,









