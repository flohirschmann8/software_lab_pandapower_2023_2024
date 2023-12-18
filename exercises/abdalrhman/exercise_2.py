### new exercise 2
import matplotlib.pyplot as plt

import pandapower as pp
import pandapower.networks as nw
import pandapower.plotting as plot
# import matplotlib
# %matplotlib inline

# load the network
net = nw.mv_oberrhein(scenario="generation")

# plot.simple_plot(net)

##### task2 #########
##### line loading color map
net.sgen.p_mw = net.sgen.p_mw*3.4

pp.runpp(net)

def plotting_lc_bc(net):

    pp.runpp(net)

    cmap_list = [(0, "green"), (100, "yellow"), (101, "red")]
    cmap, norm = plot.cmap_continuous(cmap_list)

    lc = plot.create_line_collection(net, net.line.index, zorder=1, cmap=cmap, norm=norm, linewidths=2)
    # plot.draw_collections(collections= [lc], figsize=(12,8))

    ##### adding bus voltage color map

    cmap_list = [(0.95, "blue"), (1.0, "green"), (1.05, "red")]
    cmap, norm = plot.cmap_continuous(cmap_list)

    bc = plot.create_bus_collection(net, net.bus.index, size=80, zorder=2, cmap=cmap, norm=norm)
    plot.draw_collections(collections=[lc, bc], figsize=(12, 8))
    plt.show()



plotting_lc_bc(net)
#### task3 ######

overloaded_lines = net.line[net.res_line.loading_percent > 100].index

pp.change_std_type(net,eid=overloaded_lines[0],name='NA2XS2Y 1x240 RM/25 12/20 kV',element='line')
pp.change_std_type(net,eid=overloaded_lines[1],name='NA2XS2Y 1x240 RM/25 12/20 kV',element='line')
pp.change_std_type(net,eid=overloaded_lines[2],name='NA2XS2Y 1x240 RM/25 12/20 kV',element='line')

#### task4#######

plotting_lc_bc(net)

#### since line 54 still overloaded i changed it with higher stanarded type

pp.change_std_type(net,eid=overloaded_lines[0],name='N2XS(FL)2Y 1x300 RM/35 64/110 kV',element='line')

plotting_lc_bc(net)










