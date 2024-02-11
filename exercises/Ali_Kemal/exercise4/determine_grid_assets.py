

def data_output_subnet(buses_subnet, lines_subnet, network):
    # Printing number of lines, buses, loads feed-in plants in subnetwork
    # Print number of buses
    nr_buses = len(buses_subnet)
    print("The subnet includes ", nr_buses, "buses.")

    # Print number of lines
    # nr_lines = len(buses_subnet)
    # print("The complete network includes ", nr_lines, "lines.")

    # Print number of lines
    print("The subnetwork includes ", len(lines_subnet), "lines.")

    # Print number of loads
    nr_loads = []
    #x = buses_subnet[0]

    #for x in range(buses_subnet[0], buses_subnet[-1]):
    #    nr_loads.append(network.load[network.load.bus == x])
    #    x += 1
    loads_a2 = network.load.bus.isin(buses_subnet)
    print("The network includes ", len(loads_a2), "loads.")

    # Print number of sgens
    sgens_a2 = network.sgen.bus.isin(buses_subnet)
    #x = buses_subnet[0]
    #for x in range(buses_subnet[0], buses_subnet[-1]):
    #    nr_gens.append(network.sgen[network.sgen.bus == x])
    #    x += 1

    print("The network includes ", len(sgens_a2), "gens.")
    return loads_a2, sgens_a2