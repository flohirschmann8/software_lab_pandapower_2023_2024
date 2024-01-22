import pandapower as pp
import pandapower.plotting as plot
import matplotlib.pyplot as plt

#import net "oberrhein"
net = pp.networks.mv_oberrhein(scenario="generation")

#increase p_mw
net.sgen.loc[:, "p_mw"] *= 3.4
#net.sgen["p_mw"] *= 3.4
#net.sgen.p_mw *= 3.4

#powerflow
pp.runpp(net)

#colouring lines
cmap_list_b=[(0, "green"), (100, "yellow"), (101, "red")]
cmap, norm = plot.cmap_continuous(cmap_list_b)
lc = plot.create_line_collection(net, net.line.index, zorder=1, cmap=cmap, norm=norm, linewidths=2)

#colouring busses
cmap_list_b=[(0.95, "blue"), (1.0, "green"), (1.05, "red")]
cmap, norm = plot.cmap_continuous(cmap_list_b)
bc = plot.create_bus_collection(net, net.bus.index, size=80, zorder=2, cmap=cmap, norm=norm)

#plotting
plot.draw_collections([lc, bc], figsize=(8,6))
plt.show()
