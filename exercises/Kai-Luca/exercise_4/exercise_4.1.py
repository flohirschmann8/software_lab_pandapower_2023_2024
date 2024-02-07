import pandapower as pp
import pandapower.topology as top
import pandapower.networks as nw
import pandapower.plotting as plot
import matplotlib.pyplot as plt
import pandapower.toolbox as tool


net = pp.from_json("C:/Users/User/Documents/Uni/Master/1. Semester/Pandapower/Hausarbeit/Netz/net_exercise_4.json")
mg = top.create_nxgraph(net)

#Netze unterscheiden anhand der Knoten

buses_area1 = list(top.connected_component(mg, bus=0))
buses_area2 = list(top.connected_component(mg, bus=45))
buses_area3 = list(top.connected_component(mg, bus=89))
buses_area4 = list(top.connected_component(mg, bus=134))

#Leitungen mit den gelisteten Knoten "verbinden"
lines_area3 = tool.get_connected_elements(net, "line", buses_area3)

#Trafo, sgen, load und ext_grid den Areas zuordnen
trafo_area3 = net.trafo[(net.trafo.hv_bus.isin(buses_area3)) & (net.trafo.lv_bus.isin(buses_area3))]
sgen_area3 = net.sgen[net.sgen.bus.isin(buses_area3)]
load_area3 = net.load[net.load.bus.isin(buses_area3)]
ext_grid_area1 = net.ext_grid[net.ext_grid.bus.isin(buses_area1)]
ext_grid_area2 = net.ext_grid[net.ext_grid.bus.isin(buses_area2)]
ext_grid_area3 = net.ext_grid[net.ext_grid.bus.isin(buses_area3)]
ext_grid_area4 = net.ext_grid[net.ext_grid.bus.isin(buses_area4)]

#Collection für line,bus,trafo, ext_grid, alles grau
lc = plot.create_line_collection(net, net.line.index, color="grey", zorder=1)
bc = plot.create_bus_collection(net, net.bus.index, size=60, color="grey", zorder=1)
gc1 = plot.create_ext_grid_collection(net, size=250, color="grey", ext_grids=ext_grid_area1.index, edgecolor="grey")
gc2 = plot.create_ext_grid_collection(net, size=250, color="grey", ext_grids=ext_grid_area2.index, edgecolor="grey")
gc4 = plot.create_ext_grid_collection(net, size=250, color="grey", ext_grids=ext_grid_area4.index, edgecolor="grey")

#Collection für bus, line, trafo, ext grid area 3
bc3 = plot.create_bus_collection(net, net.bus.loc[buses_area3].index, size=60, color="blue", zorder=2)
lc3 = plot.create_line_collection(net, lines_area3, color="blue", zorder=2)
gc3 = plot.create_ext_grid_collection(net, size=250, color="blue", ext_grids=ext_grid_area3.index, edgecolor="blue")

#Plotten aller Collections
plot.draw_collections([lc, bc, gc1, gc2, gc4, bc3, lc3, gc3], figsize=(8,6))
plt.show()

print(f"Anzahl der Knoten: ", len(buses_area3))
print(f"Anzahl der Leitungen: ", len(lines_area3))
print(f"Anzahl der Lasten: ", len(load_area3))
print(f"Anzahl der Einspeiser: ", len(sgen_area3))


