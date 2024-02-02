import pandapower as pp
import pandapower.networks as nw
import pandapower.plotting as plot
import matplotlib.pyplot as plt



#Load MV_ Oberrhein
net = nw.mv_oberrhein(scenario="generation")

#Incrase Feed-in Power
net.sgen["p_mw"] *= 3.4

#Netz plotten
#plot.simple_topology(net)

#powerflow
pp.runpp(net)

#createlinear colourmap for line loading
cmap_list_lines=[(0, "green"), (100, "yellow"), (101, "red")]
cmap_lines, norm_lines = plot.cmap_continuous(cmap_list_lines)

line_collection = plot.create_line_collection(net, lines=net.line.index, zorder=1, cmap=cmap_lines, norm=norm_lines,linewidths=2)

line_collection = plot.create_line_collection(net, net.line.index, zorder=1, cmap=cmap_lines, norm=norm_lines,linewidths=2)
#plot.draw_collections([line_collection], figsize=(8,6))

cmap_list_buses=[(0.95, "blue"), (1.0, "green"), (1.05, "red")]
cmap_buses, norm_buses = plot.cmap_continuous(cmap_list_buses)
bus_collection = plot.create_bus_collection(net, net.bus.index, size=80, zorder=2, cmap=cmap_buses, norm=norm_buses)
#plot.draw_collections([line_collection, bus_collection], figsize=(8,6))

plot.draw_collections([line_collection, bus_collection])
plt.show()

