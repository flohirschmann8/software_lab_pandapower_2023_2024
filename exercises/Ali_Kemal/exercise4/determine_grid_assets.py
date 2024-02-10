

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
    x = buses_subnet[0]

    for x in range(buses_subnet[0], buses_subnet[-1]):
        nr_loads.append(network.load[network.load.bus == x])
        x += 1

    print("The network includes ", len(nr_loads), "loads.")

    # Print number of gens
    nr_gens = []
    x = buses_subnet[0]
    for x in range(buses_subnet[0], buses_subnet[-1]):
        nr_gens.append(network.sgen[network.sgen.bus == x])
        x += 1

    print("The network includes ", len(nr_gens), "gens.")
