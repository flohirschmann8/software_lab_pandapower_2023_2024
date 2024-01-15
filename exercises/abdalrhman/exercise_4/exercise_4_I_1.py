

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


### TODO: reminder to summurize the grid description in word

###### grid sketches #######

### assigning the lines and buses groups that distingush between area 4 and the other areas
lc_area4  = plot.create_line_collection(net, idx_lines, zorder=2, linewidths=2 , color = 'green')
lc_others = plot.create_line_collection(net, net.line.index[~net.line.index.isin(idx_lines)],color = 'grey')

bc_area4 = plot.create_bus_collection(net, idx_buses, size=80, zorder=2, color='blue')
bc_others = plot.create_bus_collection(net, net.bus.index[~net.bus.index.isin(idx_buses)], size=80, zorder=2,color = 'grey')

plot.draw_collections(collections=[lc_area4, lc_others,bc_area4,bc_others], figsize=(12, 8))

## draw legends for grid assets
legend_labels = [f'{n_of_busus} Buses at area 4',
                 f'{n_of_lines} Lines at area 4',

                 f'{n_of_switches} Switches at area',
                 f'{n_of_sgens} Sgen at area 4',
                 f'{n_of_loads} Loads at area 4',
                 f'{n_of_trafos} Trafo at area 4',
                 f'{n_of_ext_grids} External grid at area 4',

                 f'{len(net.line.index[~net.line.index.isin(idx_lines)])} Lines at other areas',
                 f'{len(net.bus.index[~net.bus.index.isin(idx_buses)])} Buses at other areas']
legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10),
                  plt.Line2D([0], [0], color='green', linewidth=2),

                  plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='red', markersize=10),
                  plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='red', markersize=10),
                  plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='red', markersize=10),
                  plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='red', markersize=10),
                  plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='red', markersize=10),

                  plt.Line2D([0], [0], color='grey', linewidth=2),
                  plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='grey', markersize=10)]



plt.legend(legend_handles, legend_labels, loc='upper right')


plt.show()

# plt.savefig(r".\exercises\abdalrhman\exercise_4\net_exercise_4_I_1.png")

## TODO: put the sketch on word

