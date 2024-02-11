import matplotlib.pyplot as plt
import pandapower as pp


# Plotting maximum line-loading + maximum and minimum bus voltages
def extrem_values(network, lines_subnet, buses_subnet, show):
    # Determine maximum line-loading
    max_ll = 0
    max_ll_index = 0
    for x in range(0, len(network.res_line.loading_percent)):
        if network.res_line.loading_percent[x] > max_ll and x in lines_subnet:
            max_ll = network.res_line.loading_percent[x]
            max_ll_index = x
            x += 1
        else:
            x += 1

    print(max_ll)
    print(max_ll_index)

    # Determine maximum and minimum bus voltage
    max_bv = 0
    min_bv = 0
    max_bv_index = 0
    min_bv_index = 0

    for x in range(0, len(network.res_bus.vm_pu)):
        if network.res_bus.vm_pu[x] > max_bv and x in buses_subnet:
            max_bv = network.res_bus.vm_pu[x]
            max_bv_index = x
            x += 1
        else:
            x += 1

    for x in range(0, len(network.res_bus.vm_pu)):
        if network.res_bus.vm_pu[x] > max_bv and x in buses_subnet:
            max_bv = network.res_bus.vm_pu[x]
            max_bv_index = x
            x += 1
        else:
            x += 1

    print("The maximum line-loading is at line ", max_ll_index, " with ", max_ll, " percent.")
    print("The maximum bus-voltage is at bus ", max_bv_index, " with ", max_bv, " percent.")
    print("The minimum bus-voltage is at bus ", min_bv_index, " with ", min_bv, " percent.")

    # Plotting maximum line-loading + maximum and minimum bus voltage
    t = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    a = [max_ll, max_ll, max_ll, max_ll,max_ll , max_ll, max_ll, max_ll, max_ll, max_ll]
    b = [max_bv, max_bv, max_bv, max_bv,max_bv , max_bv, max_bv, max_bv, max_bv, max_bv]
    c = [min_bv, min_bv, min_bv, min_bv,min_bv , min_bv, min_bv, min_bv, min_bv, min_bv]

    plt.plot(t, a, label="Maximum line-loading")
    plt.plot(t, b, label="Maximum bus-voltage")
    plt.plot(t, c, label="Minimum bus-voltage")

    plt.xlabel("Time")
    plt.title("Maximum and minimum values before timeseries")
    #plt.legend()
    plt.grid(True)
    if show:
        plt.show()


def overload(network, max_line_loading, min_bus_voltage, max_bus_voltage):
    # Detect and output violated lines and overloaded buses
    pp.runpp(network)

    overloaded_lines = []
    x = 0
    for x in range(0, (len(network.res_line - 1))):
        if network.res_line.loading_percent[x] > max_line_loading:
            overloaded_lines.append(x)
        x += 1

    overloaded_buses = []
    x = 0
    for x in range(0, (len(network.res_bus) - 1)):
        if network.res_bus.vm_pu[x] > max_bus_voltage or network.res_bus.vm_pu[x] < min_bus_voltage:
            overloaded_buses.append(x)
        x += 1

    print("The overloaded lines are: ", overloaded_lines)
    print("The overloaded buses are: ", overloaded_buses)
