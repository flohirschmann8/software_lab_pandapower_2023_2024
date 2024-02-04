import numpy as np
import pandas as pd
import pandapower as pp
import pandapower.plotting as plot
import pandapower.topology as top
import matplotlib.pyplot as plt
from fc_dataoutput_subnet import data_output_subnet

""""
Exercise

Programming a time series simulation and developing a controller, which solves earlier detected violations.
The developed controller should be combined with controllers of other students, later.
"""

#Load network "net" from json file

net = pp.from_json("/Users/alikemalkoc/Library/Mobile Documents/com~apple~CloudDocs/Uni - Aktuelles Semester/01_Softwarepraktikum Pandapower/Übungen/exercise 4/Exam Files-20240128/net_exercise_4.json")

#Task 1 - Grid analyse

#Split network in 4 subnetworks
mg = top.create_nxgraph(net)
#Area 1
buses_area1 = list(top.connected_component(mg, bus=0))
#Area 2
buses_area2 = list(top.connected_component(mg, bus=45))
#Area 3
buses_area3 = list(top.connected_component(mg, bus=89))
#Area 4
buses_area4 = list(top.connected_component(mg, bus=134))

#Printing number of buses, lines, loads and gens of selected subnet (area2)
data_output_subnet(buses_area2, net)

#Coloring buses in area2 - green
bc_a2 = plot.create_bus_collection(net, buses=buses_area2, color="green", size=80, zorder=1)

#Coloring buses of area 1,3 and 4 - grey
bc_rest = plot.create_bus_collection(net, buses=buses_area1+buses_area3+buses_area4, color="grey", size=80, zorder=1)

#Drawing lines in gree
lines = []
x = 0
for x in range(0, len(net.line)):
    lines.append(x)
    x += 1

lc = plot.create_line_collection(net, lines=lines, color="grey", zorder=2)

plot.draw_collections([bc_a2, bc_rest, lc])

#plt.show()





