import pandapower as pp
import matplotlib
import pandapower.plotting as plot

matplotlib.use("Qt5Agg")

#create empty net
net = pp.create_empty_network()

#create buses
bus0 = pp.create_bus(net, vn_kv=10, name="bus0")
bus1 = pp.create_bus(net, vn_kv=0.4, name="bus1")
bus2 = pp.create_bus(net, vn_kv=0.4, name="bus2")
bus3 = pp.create_bus(net, vn_kv=0.4, name="bus3")
bus4 = pp.create_bus(net, vn_kv=0.4, name="bus4")
bus5 = pp.create_bus(net, vn_kv=0.4, name="bus5")
bus6 = pp.create_bus(net, vn_kv=0.4, name="bus6")

#create bus elements
pp.create_ext_grid(net, bus=bus0, vm_pu=1.0, va_degree=0.0, name="Grid Connection")

#create load
load1 = pp.create_load(net, bus=bus2, p_mw=0.015, q_mvar=-0.01, name="load1")
load2 = pp.create_load(net, bus=bus3, p_mw=0.005, q_mvar=0.0001, name="load2")
load3 = pp.create_load(net, bus=bus4, p_mw=0.025, q_mvar=-0.005, name="load3")
load4 = pp.create_load(net, bus=bus6, p_mw=0.01378, q_mvar=0.00453, name="load4")

#create Trafo
transformer = pp.create_transformer(net, hv_bus=bus0, lv_bus=bus1, std_type="0.63 MVA 10/0.4 kV", name="transformer")

#create lines
line1 = pp.create_line(net, bus1, bus2, length_km=0.72, std_type="NAYY 4x50 SE", name="Line 1")
line2 = pp.create_line(net, bus2, bus3, length_km=1.50, std_type="NAYY 4x50 SE", name="Line 2")
line3 = pp.create_line(net, bus3, bus4, length_km=0.30, std_type="NAYY 4x50 SE", name="Line 3")
line4 = pp.create_line(net, bus1, bus5, length_km=0.14, std_type="NAYY 4x50 SE", name="Line 4")
line5 = pp.create_line(net, bus5, bus6, length_km=0.17, std_type="NAYY 4x50 SE", name="Line 5")
line6 = pp.create_line(net, bus6, bus4, length_km=0.50, std_type="NAYY 4x50 SE", name="Line 6")

#create voltage controlled generator
pp.create_gen(net, bus5, p_mw=0.1, vm_pu=1.0, name="generator")

#static generator
sgen1 = pp.create_sgen(net, bus1, p_mw=0.035, q_mvar=-0.005, name="sgen1")
sgen2 = pp.create_sgen(net, bus2, p_mw=0.002, q_mvar=-0.0002, name="sgen2")
sgen3 = pp.create_sgen(net, bus3, p_mw=0.01, q_mvar=0.0, name="sgen3")
sgen4 = pp.create_sgen(net, bus6, p_mw=0.007, q_mvar=0.001, name="sgen4")

#Switch
pp.create_switch(net, bus=4, element=2, et="l", closed=False)


#plot net 1

plot.simple_topology(net)

#add geocoordinates
net.bus_geodata.loc[0, "x"] = 1.5
net.bus_geodata.loc[0, "y"] = 0.0
net.bus_geodata.loc[1, "x"] = 1.5
net.bus_geodata.loc[1, "y"] = -1.0
net.bus_geodata.loc[2, "x"] = 0.0
net.bus_geodata.loc[2, "y"] = -2.0
net.bus_geodata.loc[3, "x"] = 0.0
net.bus_geodata.loc[3, "y"] = -3.0
net.bus_geodata.loc[4, "x"] = 1.5
net.bus_geodata.loc[4, "y"] = -4.0
net.bus_geodata.loc[5, "x"] = 3.0
net.bus_geodata.loc[5, "y"] = -2.0
net.bus_geodata.loc[6, "x"] = 3.0
net.bus_geodata.loc[6, "y"] = -3.0

#plot net 2
#plot.simple_topology(net)

#Powerflow
#pp.runpp(net)

#results bus
#net.res_bus

#resuls line
#net.res_line

#increase number of columns
import pandas as pd
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

#Aufgabe 3

net.gen.loc[0, "scaling"] = 0.4

net.load.loc[2, "scaling"] = 0.4

pp.runpp(net)




