import pandapower as pp
import pandapower.topology as top
import determine_grid_assets
import drawing_grid
import analyzing_violations_and_overloads
import timeseries_1

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
buses_area1 = list(top.connected_component(mg, bus=0))
buses_area2 = list(top.connected_component(mg, bus=45))
buses_area3 = list(top.connected_component(mg, bus=89))
buses_area4 = list(top.connected_component(mg, bus=134))

# Select subnet
buses_other = buses_area1 + buses_area3 + buses_area4
lines_area2 = drawing_grid.lines_subnet


# Output number of buses, lines, loads and gens of selected subnet (area2)
determine_grid_assets.data_output_subnet(buses_area2, lines_area2, net)

# Drawing grid (To show set "show"=True)
drawing_grid.draw_grid(net, buses_area2, buses_other, show=False)

# Output maximum line-loading + maximum and minimum bus-voltage (To show set "show"=True)
analyzing_violations_and_overloads.extrem_values(net, lines_area2, buses_area2, show=False)

# Run network + detect and output violated lines and overloaded buses
pp.runpp(net)
analyzing_violations_and_overloads.overload(net, 100, 0.95, 1.05)

# Run timeseries way 1
load, generation = timeseries_1.run_ts(net, "timeseries_exercise_4.csv")

# Run timeseries way 2

