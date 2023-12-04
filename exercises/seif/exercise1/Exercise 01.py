import pandapower as pp
import pandapower.plotting as plot

import matplotlib

matplotlib.use("Qt5Agg")
# pp.create_buses(net,nr_buses=6,vn_kv=[0.4]
# create empty net
# pp.create_bus(net, vn_kv=10., geodata=(1.5, 0), name="Bus 1")
net = pp.create_empty_network()
# create buses
pp.create_bus(net, vn_kv=10., geodata=(1.5, 0), name="Bus 1")
pp.create_bus(net, vn_kv=0.4, geodata=(1.5, -1), name="Bus 2")
pp.create_bus(net, vn_kv=0.4, geodata=(0, -2.0), name="Bus 3")
pp.create_bus(net, vn_kv=0.4, geodata=(0, -3.0), name="Bus 4")
pp.create_bus(net, vn_kv=0.4, geodata=(1.5, -4.0), name="Bus 5")
pp.create_bus(net, vn_kv=0.4, geodata=(3.0, -3.0), name="Bus 6")
pp.create_bus(net, vn_kv=0.4, geodata=(3.0, -2.0), name="Bus 7")
# create bus elements
pp.create_switch(net, bus=5, element=, et="l", closed=False)
pp.create_ext_grid(net, bus=bus1, vm_pu=1.0, name="Grid Connection")
pp.create_load(net, bus=bus3, p_mw=0.015, q_mvar=-0.01, name="Load3")
pp.create_load(net, bus=bus4, p_mw=0.005, q_mvar=.0001, name="Load4")
pp.create_load(net, bus=bus5, p_mw=0.025, q_mvar=-0.005, name="Load5")
pp.create_load(net, bus=bus6, p_mw=0.01378, q_mvar=-0.00453, name="Load6")
transformer = pp.create_transformer(net, hv_bus=bus1, lv_bus=bus2, name="10/0.4kV ", std_type="0.63 MVA 10/0.4 kV")
pp.create_line(net, from_bus=bus2, to_bus=bus3, length_km=0.72, std_type="NAYY 4x50 SE",  name="Line 1")
pp.create_line(net, from_bus=bus3, to_bus=bus4, length_km=1.5, std_type="NAYY 4x50 SE",  name="Line 2")
line3 = pp.create_line(net, from_bus=bus4, to_bus=bus5, length_km=0.3, std_type="NAYY 4x50 SE",  name="Line 3")
line4 = pp.create_line(net, from_bus=bus5, to_bus=bus6, length_km=0.5, std_type="NAYY 4x50 SE",  name="Line 6")
line5 = pp.create_line(net, from_bus=bus6, to_bus=bus7, length_km=0.17, std_type="NAYY 4x50 SE",  name="Line 5")
line6 = pp.create_line(net, from_bus=bus7, to_bus=bus2, length_km=0.14, std_type="NAYY 4x50 SE",  name="Line 4")
pp.create_sgen(net, bus3, p_mw=0.002, q_mvar=-0.002, name="static generator1")
pp.create_sgen(net, bus4, p_mw=0.01, q_mvar=-0.0, name="static generator2")
pp.create_sgen(net, bus6, p_mw=0.007, q_mvar=0.001, name="static generator3")
pp.create_gen(net, bus7, p_mw=0.1, vm_pu=1.0, name="generator")
pp.create_sgen(net, bus6, p_mw=0.035, q_mvar=-0.005, name="static generator3")
plot.simple_topology(net)
pp.runpp(net)
print(net)
print(net.res_bus)
print(net.res_line)
print(net.bus)
print(net.line)
