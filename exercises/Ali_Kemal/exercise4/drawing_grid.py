import pandapower.plotting as plot
import matplotlib.pyplot as plt

lines_subnet = []
lines_all = []


def draw_grid(network, buses_subnet, buses_other, show):
    # Determine lines of subnet

    for idx, line in network.line.iterrows():
        if line.from_bus in buses_subnet or line.to_bus in buses_subnet:
            lines_subnet.append(idx)

    # Drawing lines of subnet in green and lines of other areas in gree

    x = 0
    for x in range(0, len(network.line)):
        lines_all.append(x)
        x += 1

    lines_other_subnets = [element for element in lines_all if element not in lines_subnet]

    lc_other = plot.create_line_collection(network, lines=lines_other_subnets, color="grey", zorder=2)
    lc_subnet = plot.create_line_collection(network, lines=lines_subnet, color="green", zorder=2)

    # Coloring buses of area 1,3 and 4 in grey and buses of area2 in green
    bc_other = plot.create_bus_collection(network, buses=buses_other, color="grey", size=80, zorder=1)
    bc_subnet = plot.create_bus_collection(network, buses=buses_subnet, color="green", size=80, zorder=1)

    plot.draw_collections([bc_subnet, bc_other, lc_subnet, lc_other])
    if show:
        plt.show()