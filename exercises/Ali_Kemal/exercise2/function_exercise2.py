import matplotlib.pyplot as plt
import pandapower as pp
import pandapower.plotting as plot


# ========== TASK 1 ==========

def plot_network_state(net: pp.pandapowerNet, color_map_type: str = "discrete"):
    """
    This function plots the network and shows the network state using a continuous colormap.
    Before this, a power flow calculation must be performed separately.

    Parameters
    ----------
    net : pandapowerNet
        The network element to be displayed.
    color_map_type : str, optional
        The type of the color map. Defaults to 'discrete' for a discrete colormap.
    """
    # create line collection
    if color_map_type == "discrete":
        cmap_list_lines = [((0, 50), "green"), ((50, 100), "yellow"), ((100, 150), "red")]
        cmap_lines, norm_lines = plot.cmap_discrete(cmap_list_lines)
    else:
        cmap_list_lines = [(0, "green"), (100, "yellow"), (101, "red")]
        cmap_lines, norm_lines = plot.cmap_continuous(cmap_list_lines)
    line_collection = plot.create_line_collection(net, lines=net.line.index, cmap=cmap_lines,
                                                  norm=norm_lines, zorder=1, linewidth=2)

    # create bus collection
    if color_map_type == "discrete":
        cmap_list_buses = [((0.95, 0.975), "blue"), ((0.975, 1.025), "green"),
                           ((1.025, 1.05), "red")]
        cmap_buses, norm_buses = plot.cmap_discrete(cmap_list_buses)
    else:
        cmap_list_buses = [(0.95, "blue"), (1.00, "green"), (1.05, "red")]
        cmap_buses, norm_buses = plot.cmap_continuous(cmap_list_buses)
    bus_collection = plot.create_bus_collection(net, buses=net.bus.index, cmap=cmap_buses,
                                                norm=norm_buses, zorder=2, size=80)

    # plot all collections
    plot.draw_collections([line_collection, bus_collection])
    plt.show()