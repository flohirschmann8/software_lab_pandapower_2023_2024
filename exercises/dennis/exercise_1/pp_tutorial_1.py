import pandapower as pp
import pandapower.plotting as plot
import matplotlib

#matplotlib.use("Qt5Agg")
#%%

def get_comp_index(list_of_components,name_of_component):
    bus_index = list_of_components[list_of_components["name"] == name_of_component].index[0]
    return bus_index

#####################################################################################################################
#####################################################################################################################
# Task a) ###########################################################################################################
#####################################################################################################################
#####################################################################################################################

# create an empty network
net_tut_1 = pp.create_empty_network()
# define voltage levels
hv = 10.0
lv = 0.4
num_dist_busses = 5 # number of distribution busses that are not the transformer busses
dist_bus_names = ["Bus_2", "Bus_3", "Bus_4", "Bus_5", "Bus_6"]
geodata_dist_busses = [(0.0,-2.0),(0.0,-3.0),(1.5,-4.0),(3.0,-2.0),(3.0,-3.0)]

# creating the network components

# busses

hv_bus_ONT_1 = pp.create_bus(net=net_tut_1, vn_kv=hv, name="HV_Bus_Trafo")
lv_bus_ONT_1 = pp.create_bus(net=net_tut_1, vn_kv=lv, name="LV_Bus_Trafo")
[bus_2, bus_3, bus_4, bus_5, bus_6] = pp.create_buses(net=net_tut_1, nr_buses=num_dist_busses, vn_kv=lv, name=dist_bus_names)

#bus_7 = pp.create_bus(net=net_tut_1, vn_kv=lv, name="Geo_Bus", geodata=(1,1))

list_of_busses = net_tut_1.bus

# create external Grid
mv_grid = pp.create_ext_grid(net=net_tut_1, bus=hv_bus_ONT_1, vm_pu=1.0, name="MV_Slack")

# create transformer
ont_1 = pp.create_transformer(net=net_tut_1, hv_bus=hv_bus_ONT_1,lv_bus=lv_bus_ONT_1, std_type="0.63 MVA 10/0.4 kV", name="ONT_101")

# create static generators (PQ)

wea_1 = pp.create_sgen(net=net_tut_1, bus=lv_bus_ONT_1, p_mw=0.035, q_mvar=-0.005, name="WEA_1")
pv_1 = pp.create_sgen(net=net_tut_1, bus=bus_2, p_mw=0.002, q_mvar=-0.0002, name="PV_1")
pv_2 = pp.create_sgen(net=net_tut_1, bus=bus_3, p_mw=0.01, q_mvar=0.0, name="PV_2")
pv_3 = pp.create_sgen(net=net_tut_1, bus=bus_6, p_mw=0.007, q_mvar=0.001, name="PV_3")

list_of_sgen = net_tut_1.sgen


# create generators (PU)
conv_gen_1 = pp.create_gen(net=net_tut_1, bus=bus_5, p_mw=0.1, vm_pu=1.0, name="Conv._Gen_1")

list_of_conv_gens = net_tut_1.gen


# create loads (PQ)
load_1 = pp.create_load(net=net_tut_1, bus=bus_2, p_mw=0.015, q_mvar=-0.01, name="Load_1")
load_2 = pp.create_load(net=net_tut_1, bus=bus_3, p_mw=0.005, q_mvar=0.0001, name="Load_2")
load_3 = pp.create_load(net=net_tut_1, bus=bus_4, p_mw=0.025, q_mvar=-0.005, name="Load_3")
load_4 = pp.create_load(net=net_tut_1, bus=bus_6, p_mw=0.01378, q_mvar=0.00453, name="Load_4")

list_of_loads = net_tut_1.load


# create lines
standard_type = "NAYY 4x50 SE"

line_1 = pp.create_line(net=net_tut_1, from_bus=lv_bus_ONT_1, to_bus=bus_2, std_type=standard_type, name="Line_1", length_km=0.72)
line_2 = pp.create_line(net=net_tut_1, from_bus=bus_2, to_bus=bus_3, std_type=standard_type, name="Line_2", length_km=1.5)
line_3 = pp.create_line(net=net_tut_1, from_bus=bus_3, to_bus=bus_4, std_type=standard_type, name="Line_3", length_km=0.3)
line_4 = pp.create_line(net=net_tut_1, from_bus=lv_bus_ONT_1, to_bus=bus_5, std_type=standard_type, name="Line_4", length_km=0.14)
line_5 = pp.create_line(net=net_tut_1, from_bus=bus_5, to_bus=bus_6, std_type=standard_type, name="Line_5", length_km=0.17)
line_6 = pp.create_line(net=net_tut_1, from_bus=bus_6, to_bus=bus_4, std_type=standard_type, name="Line_6", length_km=0.5)

list_of_lines = net_tut_1.line

# create switches
switch_1 = pp.create_switch(net=net_tut_1, et="l", bus=bus_4, element=line_3, type="LBS", closed=False)

list_of_switches = net_tut_1.switch

#####################################################################################################################
#####################################################################################################################
# Task b) ###########################################################################################################
#####################################################################################################################
#####################################################################################################################

# plot.simple_plot(net=net_tut_1,plot_line_switches=True,show_plot=False, plot_gens=True, plot_sgens=True, plot_loads=True) # done and saved as fitst_plot_task_b.png
# plot.simple_topology(net=net_tut_1)

# assigning coordinates to the busses

bus_geodata_afterwards = [(1.5,0.0),(1.5,-1.0),(0.0,-2.0),(0.0,-3.0),(1.5,-4.0),(3.0,-2.0),(3.0,-3.0)]

for idx_row, geodata_row in net_tut_1.bus.iterrows():
    net_tut_1.bus_geodata.loc[idx_row, 'x'], net_tut_1.bus_geodata.loc[idx_row, 'y'] = bus_geodata_afterwards[idx_row]

#plot.simple_topology(net=net_tut_1)
# plot.simple_plot(net=net_tut_1, plot_line_switches=True,show_plot=False, plot_gens=True, plot_sgens=True, plot_loads=True, sgen_size=3, gen_size=3, load_size=3)
#%%

#####################################################################################################################
#####################################################################################################################
# Task 2) ###########################################################################################################
#####################################################################################################################
#####################################################################################################################

pp.runpp(net=net_tut_1)

# the line is overloaded, because of the conventional generator at bus 5 to stabelise the voltage.
# Load 3 at bus 6 can be increased to p_mw = 0.0575 to reduce the loading of line 3 (4 in diagramm)


# ideal solution set the nominal voltage of the PU-Gen to 1.03 pu
net_tut_1.gen.loc[conv_gen_1,"vm_pu"] = 1.03 # not needed buz good for line loading