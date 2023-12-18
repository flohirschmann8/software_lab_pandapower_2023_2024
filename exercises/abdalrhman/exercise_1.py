

import pandapower as pp

net = pp.create_empty_network()


pp.create_bus(net, vn_kv=10)
pp.create_bus(net, 0.4)
pp.create_bus(net, 0.4)
pp.create_bus(net, 0.4)
pp.create_bus(net, 0.4)
pp.create_bus(net, 0.4)
pp.create_bus(net, 0.4)

pp.create_ext_grid(net,bus=0,vm_pu=1, va_degree=0)


pp.create_load(net,2,0.015,-0.010)
pp.create_load(net,3,0.005,0.0001)
pp.create_load(net,6,0.01378,0.00453)
pp.create_load(net,4,0.025,-0.005)


pp.create_sgen(net,2,2,-0.2)
pp.create_sgen(net,3,10,0)
pp.create_sgen(net,6,7,1)
pp.create_sgen(net,1,35,-5)

net.sgen.p_mw /= 1000
net.sgen.q_mvar /= 1000

pp.create_gen(net,5,0.01,1)

pp.create_transformer(net,hv_bus=0,lv_bus=1, name="10kV/400V transformer", std_type="0.63 MVA 10/0.4 kV")

pp.create_line(net, 1, 2, length_km=0.72, std_type="NAYY 4x50 SE",  name="Line 1")
pp.create_line(net, 2, 3, length_km=1.50, std_type="NAYY 4x50 SE",  name="Line 2")
pp.create_line(net, 3, 4, length_km=0.30, std_type="NAYY 4x50 SE",  name="Line 3")
pp.create_line(net, 1, 5, length_km=0.14, std_type="NAYY 4x50 SE",  name="Line 4")
pp.create_line(net, 5, 6, length_km=0.17, std_type="NAYY 4x50 SE",  name="Line 5")
pp.create_line(net, 6, 4, length_km=0.50, std_type="NAYY 4x50 SE",  name="Line 6")

pp.create_switch(net,3,2,et='l',closed=True)
x = [1.5,1.5,0,0,1.5,3,3]

y = [0,-1,-2,-3,-4,-2,-3]

net.bus_geodata.x = x
net.bus_geodata.y = y


#
#
# import pandapower.plotting as plot
# plot.simple_topology(net)
#
#
# pp.plotting.simple_plot(net)
#


net.load.scaling=1
net.sgen.scaling=1

#### run power flow
pp.runpp(net)

#### to present the results

net.res_bus