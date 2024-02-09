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

# Task 1 - Grid analyse
# Split network in 4 subnetworks
mg = top.create_nxgraph(net)
# Area 1
buses_area1 = list(top.connected_component(mg, bus=0))
# Area 2
buses_area2 = list(top.connected_component(mg, bus=45))
# Area 3
buses_area3 = list(top.connected_component(mg, bus=89))
# Area 4
buses_area4 = list(top.connected_component(mg, bus=134))

# Determine lines of subnet
lines_area2 = []

for idx, line in net.line.iterrows():
    # Überprüfe, ob die Linie an einem der interessierenden Indizes liegt
    if line.from_bus in buses_area2 or line.to_bus in buses_area2:
        # Füge die Linie zur Liste der verbundenen Linien hinzu
        lines_area2.append(idx)


# Drawing lines of area 1,3,4 in gree and lines of area 2 in green
lines_all = []
x = 0
for x in range(0, len(net.line)):
    lines_all.append(x)
    x += 1

lines_other_subnets = [element for element in lines_all if element not in lines_area2]

lc_rest = plot.create_line_collection(net, lines=lines_other_subnets, color="grey", zorder=2)
lc_a2 = plot.create_line_collection(net, lines=lines_area2, color="green", zorder=2)

# Coloring buses of area 1,3 and 4 in grey and buses of area2 in green
bc_rest = plot.create_bus_collection(net, buses=buses_area1 + buses_area3 + buses_area4, color="grey", size=80, zorder=1)
bc_a2 = plot.create_bus_collection(net, buses=buses_area2, color="green", size=80, zorder=1)

plot.draw_collections([bc_a2, bc_rest, lc_a2, lc_rest])
plt.show()

# Output number of buses, lines, loads and gens of selected subnet (area2)
data_output_subnet(buses_area2, lines_area2, net)

# Detect and output violated lines and overloaded buses
pp.runpp(net)

overloaded_lines = []
x = 0
for x in range(0, (len(net.res_line-1))):
    if net.res_line.loading_percent[x] > 100:
        overloaded_lines.append(x)
    x += 1

overloaded_buses = []
x = 0
for x in range(0, (len(net.res_bus)-1)):
    if net.res_bus.vm_pu[x] > 1.05 or net.res_bus.vm_pu[x] < 0.95:
        overloaded_buses.append(x)
    x += 1

print("The overloaded lines are: ", overloaded_lines)
print("The overloaded buses are: ", overloaded_buses)






'''


# Time series calculations

from pandapower.control.controller.const_control import ConstControl
from pandapower.timeseries.data_sources.frame_data import DFData
from pandapower. timeseries. run_time_series import run_timeseries
from pandapower.timeseries.output_writer import OutputWriter

net = nw. example _simple()
net.gen.drop(net.gen.index, inplace=True)
pp. create_sgen (net, 5, P_mw=1)
df = pd. read_json ("/home/florian/pandapower/tutorials/ciare timeseries 15min.json")
ds = DFData (df)
ConstControl (net,
"sgen"
', "p_mw", element_index=net sgen. index, profile_name=["wind", "pv"], data_source=ds)
ConstControl (net,
"load", "p_mw", element_index=net. load index, profile_name=["residential"], data_source=ds)
ow = OutputWriter (net, time_steps=(0, 95), output_path="./results/", output_file_type="Xlsx")
ow. log_variable("res_bus", "vm_pu")
pw
_timeseries (net, time_steps=(0,
'''