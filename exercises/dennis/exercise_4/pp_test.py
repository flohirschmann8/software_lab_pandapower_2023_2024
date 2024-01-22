import pandapower as pp
#%%

grid = pp.create_empty_network()

bus_0 = pp.create_bus(net=grid, vn_kv=110.0)
bus_1, bus_2 = pp.create_buses(net=grid, nr_buses=2, vn_kv=20.0)

ext_grid = pp.create_ext_grid(net=grid, bus=bus_0 ,vm_pu=1.0)

trafo = pp.create_transformer(net=grid, hv_bus=bus_0, lv_bus=bus_1, std_type="25 MVA 110/20 kV")

sgen = pp.create_sgen(net=grid, bus=bus_2, p_mw=0.5)
load = pp.create_load(net=grid, bus=bus_2, p_mw=0.25, scaling=1.0)

line = pp.create_line(net=grid, from_bus=bus_1, to_bus=bus_2, length_km=0.5, std_type="NA2XS2Y 1x240 RM/25 12/20 kV")

pp.runpp(net=grid)

#%%