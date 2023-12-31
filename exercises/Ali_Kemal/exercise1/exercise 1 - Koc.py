import matplotlib.pyplot as plt

import pandapower as pp
import pandapower.plotting as plot

# Creating an empty network named "net"
net = pp.create_empty_network()

# Creating busses 0 to 6
bus0 = pp.create_bus (net, vn_kv=10.0)
bus1 = pp.create_bus (net, vn_kv=0.4)
bus2 = pp.create_bus (net, vn_kv=0.4)
bus3 = pp.create_bus (net, vn_kv=0.4)
bus4 = pp.create_bus (net, vn_kv=0.4)
bus5 = pp.create_bus (net, vn_kv=0.4)
bus6 = pp.create_bus (net, vn_kv=0.4)

#Extern Grid
ext_grid0 = pp.create_ext_grid(net, bus=0, vm_pu=1.0, va_degree=0.0)

#Trafo between bus 0 and 1
trafo0 = pp. create_transformer(net, hv_bus=0, lv_bus=1, std_type="0.63 MVA 10/0.4 kV")

#WKA generator at bus1
sgen0 = pp.create_sgen(net, bus=1, p_mw=0.035, q_mvar=-0.005)

#PV generator at bus 2,3 and 6
sgen1 = pp.create_sgen(net, bus=2, p_mw=0.002, q_mvar=-0.0002)
sgen2 = pp.create_sgen(net, bus=3, p_mw=0.010, q_mvar=0.0)
sgen3 = pp.create_sgen(net, bus=6, p_mw=0.007, q_mvar=0.001)

#Voltage regulated generator at bus 5
gen0 = pp.create_gen(net, bus=5, p_mw=0.1, vm_pu=1.0)

#Loads at bus 2,3,4 and 6
load0 = pp.create_load(net, bus=2, p_mw=0.015, q_mvar=-0.01)
load1 = pp.create_load(net, bus=3, p_mw=0.005, q_mvar=0.0001)
load2 = pp.create_load(net, bus=4, p_mw=0.025, q_mvar=-0.005)
load3 = pp.create_load(net, bus=6, p_mw=0.01378, q_mvar=0.00453)


#Lines 0-5 between busses
line0 = pp.create_line(net, from_bus=1, to_bus=2, length_km=0.72, std_type="NAYY 4x50 SE")
line1 = pp.create_line(net, from_bus=2, to_bus=3, length_km=1.5, std_type="NAYY 4x50 SE")
line2 = pp.create_line(net, from_bus=3, to_bus=4, length_km=0.30, std_type="NAYY 4x50 SE")
line3 = pp.create_line(net, from_bus=1, to_bus=5, length_km=0.14, std_type="NAYY 4x50 SE")
line4 = pp.create_line(net, from_bus=5, to_bus=6, length_km=0.17, std_type="NAYY 4x50 SE")
line5 = pp.create_line(net, from_bus=6, to_bus=4, length_km=0.50, std_type="NAYY 4x50 SE")

#Switch between line 2 and bus 4
pp.create_switch(net, bus=4, element=2, et="l", closed=False)

#Adding geodata
net.bus_geodata.loc[0, "x"] = 1.5
net.bus_geodata.loc[0, "y"] = 0
net.bus_geodata.loc[1, "x"] = 1.5
net.bus_geodata.loc[1, "y"] = -1
net.bus_geodata.loc[2, "x"] = 0
net.bus_geodata.loc[2, "y"] = -2.0
net.bus_geodata.loc[3, "x"] = 0.0
net.bus_geodata.loc[3, "y"] = -3.0
net.bus_geodata.loc[4, "x"] = 1.5
net.bus_geodata.loc[4, "y"] = -4.0
net.bus_geodata.loc[5, "x"] = 3.0
net.bus_geodata.loc[5, "y"] = -2.0
net.bus_geodata.loc[6, "x"] = 3.0
net.bus_geodata.loc[6, "y"] = -3.0

#Start calculation for first time
pp.runpp(net)

#Output results
print("Bus results:\n\n")
print(net.res_bus)


print("Line results:\n\n")
print(net.res_line)


#Line 3 is overloaded (234.06%) --- scale gen0 to reduce load at line 3
net.gen.loc[0, "scaling"] = 0.4


#Bus 4 has a too low voltage (vm_pu = 92.37) --- reduce load2 at bus 4 to raise voltage
net.load.loc[2, "scaling"] = 0.5

#Start calculation
pp.runpp(net)

#Output results
print("New bus results:\n\n")
print(net.res_bus)


print("New line results:\n\n")
print(net.res_line)

#Plot network
plot.simple_topology(net)
plt.show()