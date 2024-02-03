import exercise




def data_output_subnet(
    #Printing number of lines, buses, loads feed-in plants in subnetwork
    # Print number of buses
    nr_buses = len(buses_area2)
    print("The network includes ", nr_buses, "buses.")

    # Print number of lines
    nr_lines = len(buses_area2)
    print("The network includes ", nr_lines, "lines.")


    # Print number of loads
    nr_loads = []
    x = buses_area2[0]

    for x in range(buses_area2[0], buses_area2[-1]):
        nr_loads.append(net.load[net.load.bus == x])
        x += 1

    print("The network includes ", len(nr_loads), "loads.")

    # Print number of gens
    nr_gens = []
    x = buses_area2[0]
    for x in range(buses_area2[0], buses_area2[-1]):
        nr_gens.append(net.sgen[net.sgen.bus == x])
        x += 1

    print("The network includes ", len(nr_gens), "gens.")
)



