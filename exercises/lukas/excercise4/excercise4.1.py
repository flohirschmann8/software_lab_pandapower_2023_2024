import pandapower as pp
import pandapower.topology as top
import pandapower.plotting as plot
import matplotlib.pyplot as plt
import pandapower.toolbox as tool

#Importiert das MV Oberrhein Netzwerk
net = pp.from_json("/Users/lukaskramer/Documents/Uni/Mastersemester1/Pandapower/Unterlagen/Exam_Files/net_exercise_4.json")
mg = top.create_nxgraph(net)

#Listet alle mit den aufgeführten Knoten (0, 45, 89, 134) auf und schreibt diese in eine Liste
buses_area1 = list(top.connected_component(mg, bus=0))
buses_area2 = list(top.connected_component(mg, bus=45))
buses_area3 = list(top.connected_component(mg, bus=89))
buses_area4 = list(top.connected_component(mg, bus=134))

#Definition der Elemente in Area 2 anhand der Knoten
lines_area2 = tool.get_connected_elements(net, "line", buses_area2)
#lines_area2 = net.line[(net.line.from_bus.isin(buses_area2))&net.line.to_bus.isin(buses_area2)]
trafo_area2 = net.trafo[(net.trafo.hv_bus.isin(buses_area2)) & (net.trafo.lv_bus.isin(buses_area2))]
ext_grid_area2 = net.ext_grid[net.ext_grid.bus.isin(buses_area2)]
sgen_area2 = net.sgen[net.sgen.bus.isin(buses_area2)]
load_area2 = net.load[net.load.bus.isin(buses_area2)]
ext_grid_area1 = net.ext_grid[net.ext_grid.bus.isin(buses_area1)]
ext_grid_area3 = net.ext_grid[net.ext_grid.bus.isin(buses_area3)]
ext_grid_area4 = net.ext_grid[net.ext_grid.bus.isin(buses_area4)]

#Erstellen von Collection, die zum Plotten verwendet werden können
lc = plot.create_line_collection(net, net.line.index, color="grey", zorder=1)
bc = plot.create_bus_collection(net, net.bus.index, size=50, color="grey", zorder=1)
tc = plot.create_trafo_collection(net, net.trafo.index, color ="grey", size=50, zorder=1)
gc1 = plot.create_ext_grid_collection(net, size=200, color="grey", orientation=1.570796326794897, ext_grids=ext_grid_area1.index, edgecolor="grey")
gc3 = plot.create_ext_grid_collection(net, size=200, color="grey", orientation=4.71238898038469, ext_grids=ext_grid_area3.index, edgecolor="grey")
gc4 = plot.create_ext_grid_collection(net, size=200, color="grey", orientation=4.71238898038469, ext_grids=ext_grid_area4.index, edgecolor="grey")

#Erstellen von Collections der Elemente in Area 2, welche in grün dargestellt werden
bc2 = plot.create_bus_collection(net, net.bus.loc[buses_area2].index, size=50, color="green", zorder=2)
lc2 = plot.create_line_collection(net, lines_area2, color="green", zorder=2)
tc2 = plot.create_trafo_collection(net, trafo_area2.index, color ="green", size=50, zorder=3)
gc2 = plot.create_ext_grid_collection(net, size=200, color="green", orientation=1.570796326794897, ext_grids=ext_grid_area2.index, edgecolor="green")

#Plotten aller Collections
plot.draw_collections([bc, lc, bc2, lc2, tc, gc1, gc3, gc4, tc2, gc2], figsize=(8,6))
#plt.savefig() für Nutzung in Latex notwenidg --> Export als Vektordatei
#plt.savefig("Netzbild.pdf")
plt.show()


lines_area2_km = net.line.loc[list(lines_area2), :]
#Informationen über das Netzgebiet 2
print(f"Die Anzahl der Knoten beträgt", len(buses_area2))
print(f"Die Anzahl der Leitungen beträgt", len(lines_area2))
print(f"Die Gesamtlänge der Leitungen beträgt", round(lines_area2_km["length_km"].sum(), 2), "km")
print(f"Die Anzahl an Generatoren beträgt", len(sgen_area2))
print(f"Die Anzahl an Lasten beträgt", len(load_area2))