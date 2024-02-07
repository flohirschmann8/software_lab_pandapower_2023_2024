import pandapower as pp
net = pp.create_empty_network()
pp.available_std_types(net, element="line")


