import pandapower as pp
import pandapower.plotting as plot
import pandas as pd

# ========== TASK 1 ==========

# CREATE NETWORK
net = pp.create_empty_network()

pp.create_bus(net, vn_kv=10.0)
pp.create_buses(net, nr_buses=6, vn_kv=0.4)

pp.create_ext_grid(net, bus=0)

pp.create_line(net, from_bus=1, to_bus=2, length_km=0.72, std_type="NAYY 4x50 SE")
pp.create_line(net, from_bus=2, to_bus=3, length_km=1.50, std_type="NAYY 4x50 SE")
pp.create_line(net, from_bus=3, to_bus=4, length_km=0.30, std_type="NAYY 4x50 SE")
pp.create_line(net, from_bus=1, to_bus=5, length_km=0.14, std_type="NAYY 4x50 SE")
pp.create_line(net, from_bus=5, to_bus=6, length_km=0.17, std_type="NAYY 4x50 SE")
pp.create_line(net, from_bus=6, to_bus=4, length_km=0.50, std_type="NAYY 4x50 SE")

pp.create_transformer(net, hv_bus=0, lv_bus=1, std_type="0.63 MVA 10/0.4 kV")

pp.create_load(net, bus=2, p_mw=0.015, q_mvar=-0.010)
pp.create_load(net, bus=3, p_mw=0.005, q_mvar=0.0001)
pp.create_load(net, bus=4, p_mw=0.025, q_mvar=-0.005)
pp.create_load(net, bus=6, p_mw=0.01378, q_mvar=0.00453)

pp.create_sgen(net, bus=1, p_mw=0.035, q_mvar=-0.005)
pp.create_sgen(net, bus=2, p_mw=0.002, q_mvar=-0.0002)
pp.create_sgen(net, bus=3, p_mw=0.010, q_mvar=0.000)
pp.create_sgen(net, bus=6, p_mw=0.007, q_mvar=0.001)
pp.create_gen(net, bus=5, p_mw=0.100, vn_kv=1.0)

pp.create_switch(net, bus=4, element=2, et="l", closed=False)


# PLOT NETWORK
# plot.simple_topology(net)

# ADD GEOCOORDINATES
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

# PLOT NETWORK AGAIN
# plot.simple_topology(net)

# ========== TASK 2 ==========

# RUN POWER FLOW
pp.runpp(net)

# COMPARE RESULTS
pd.set_option("display.max_columns", None)
print("\n+++ Results before adaption +++")
print("\nBus results")
print(net.res_bus)
print("\nLine results")
print(net.res_line)
pd.set_option("display.max_columns", 0)

# ========== TASK 3 ==========

# MEASURES
# net.gen.loc[0, "scaling"] = 0.4
# net.load.loc[2, "scaling"] = 0.4
net.gen.loc[0, "vm_pu"] = 1.03

# RUN POWER FLOW
pp.runpp(net)

# COMPARE RESULTS
pd.set_option("display.max_columns", None)
print("\n\n+++ Results after adaption +++")
print("\nBus results")
print(net.res_bus)
print("\nLine results")
print(net.res_line)
pd.set_option("display.max_columns", 0)