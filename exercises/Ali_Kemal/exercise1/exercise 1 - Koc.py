import pandapower as pp
import pandapower.plotting as plot

# Creating an empty network named "net"
net = pp.create_empty_network()

# Creating busses 1 to 6
pp.create_bus (net, vn_kv=10.0)
pp.create_bus (net, vn_kv=0.4)
pp.create_bus (net, vn_kv=0.4)
pp.create_bus (net, vn_kv=0.4)
pp.create_bus (net, vn_kv=0.4)
pp.create_bus (net, vn_kv=0.4)
pp.create_bus (net, vn_kv=0.4)

#Extern Grid
pp.create_ext_grid(net, bus=0)

#Trafo between bus 0 and 1
pp. create_transformer(net, hv_bus=0, lv_bus=1, std_type="0.4 MVA 10/0.4 kV")

#WKA generator at bus1
pp.create_sgen(net, bus=1, p_mw=0.035, q_mvar=-0.005)

#PV generator at bus 2,3 and 6
pp.create_sgen(net, bus=2, p_mw=0.002, q_mvar=-0.0002)
pp.create_sgen(net, bus=3, p_mw=0.010, q_mvar=-0.0)
pp.create_sgen(net, bus=6, p_mw=0.007, q_mvar=-0.001)

#Voltage regulated generator at bus 5
pp.create_gen(net, bus=5, p_mw=0.1, vm_pu=1.0)

#Loads at bus 2,3,4 and 6
pp.create_load(net, bus=2, p_mw=0.015, q_mvar=-0.01)
pp.create_load(net, bus=3, p_mw=0.005, q_mvar=0.0001)
pp.create_load(net, bus=4, p_mw=0.025, q_mvar=-0.005)
pp.create_load(net, bus=6, p_mw=0.01378, q_mvar=0.00453)


#Lines between busses
pp.create_line(net, from_bus=1, to_bus=2, length_km=0.72, std_type="NAYY 4x50 SE")
pp.create_line(net, from_bus=2, to_bus=3, length_km=1.5, std_type="NAYY 4x50 SE")
pp.create_line(net, from_bus=3, to_bus=4, length_km=0.30, std_type="NAYY 4x50 SE")
pp.create_line(net, from_bus=1, to_bus=5, length_km=0.14, std_type="NAYY 4x50 SE")
pp.create_line(net, from_bus=5, to_bus=6, length_km=0.17, std_type="NAYY 4x50 SE")
pp.create_line(net, from_bus=6, to_bus=4, length_km=0.50, std_type="NAYY 4x50 SE")

#Switch between line 2 and bus 4
pp.create_switch(net, bus=4, element=2, et="l", closed=False)

#Adding geodata
net.bus_geodata.loc[0, "x"] = 1.5
net.bus_geodata.loc[0, "y"] = 0
net.bus_geodata.loc[0, "x"] = 1.5
net.bus_geodata.loc[0, "y"] = -1
net.bus_geodata.loc[0, "x"] = 0
net.bus_geodata.loc[0, "y"] = 2.0
net.bus_geodata.loc[0, "x"] = 0.0
net.bus_geodata.loc[0, "y"] = -3.0
net.bus_geodata.loc[0, "x"] = 1.5
net.bus_geodata.loc[0, "y"] = -4.0
net.bus_geodata.loc[0, "x"] = 3.0
net.bus_geodata.loc[0, "y"] = -2.0
net.bus_geodata.loc[0, "x"] = 3.0
net.bus_geodata.loc[0, "y"] = -3.0


#Start calculation
pp.runpp(net)

#Output results
print(net.res_line)

#Plot network
plot.simple_plot(net)