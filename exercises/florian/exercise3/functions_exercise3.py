import copy

import numpy as np
import pandas as pd

import pandapower as pp


# ========== TASK 1 ==========

def determine_grid_capacity(net, iterations=10):
    """
    This function determines, for the specified number of iterations, how much additional feed-in
    power can be installed in the grid by distributing random feed-in plants in the grid until an
    overload occurs.

    Parameters
    ----------
    net : pandapowerNet
        The network element to be analyzed.
    iterations : int
        The number of iterations.

    Returns
    -------
    res : DataFrame
        This function returns a DataFrame that indicates for each iteration how much additional
        feed-in power could be installed and which limit violation finally occurred.
    """
    # determine grid capacity
    res = pd.DataFrame(columns=["installed_mw", "violation_type"])

    for it in range(iterations):
        print(f"Grid capacity iteration step {it + 1}")

        # copy the network
        net_copy = copy.deepcopy(net)

        # initialize installed feed-in power
        installed_mw = 0

        while True:

            # check for existing violations
            violated, violation_type = violations(net_copy)

            # if congestions appear, store them in the res dataframe and exit the while loop
            if violated:
                res.loc[it] = [installed_mw, violation_type]
                break

            # if no congestions appear, connect a new feed-in plant with a random plant size to a
            # random load bus and increase the installed feed-in power
            else:
                plant_size = np.random.normal(loc=0.5, scale=0.05)
                plant_bus = np.random.choice(net_copy.load.bus.values)
                pp.create_sgen(net_copy, bus=plant_bus, p_mw=plant_size, q_mvar=0)
                installed_mw += plant_size

    return res


def violations(net):
    """
    This function analyzes the network with regard to equipment overloads. Concretely, it examines
    whether the line or transformer utilization is above 50 % and whether the bus voltage is above
    1.04 p.u.

    Parameters
    ----------
    net : pandapowerNet
        The network element to be analyzed.

    Returns
    -------
    tuple
        This function returns a tuple containing True or False in the first entry and a message in
        the second. True in the first entry means that there is a limit violation in the network.
        The message indicates what the limit violation is. If False is returned in the first entry,
        there is no message, but a None.
    """
    pp.runpp(net)
    if net.res_line["loading_percent"].max() > 50:
        return True, "Line overloading"
    elif net.res_trafo["loading_percent"].max() > 50:
        return True, "Trafo overloading"
    elif net.res_bus["vm_pu"].max() > 1.04:
        return True, "Bus overvoltage"
    else:
        return False, None


# ========== TASK 3 ==========

def apply_random_measures(net, budget):
    # set current costs to zero
    costs = 0

    # initialize DataFrame for storing applied measures
    measures = pd.DataFrame(columns=["measure_type", "element"])
    measure_count = 0

    while True:

        # randomly choose a measure type
        measure_type = np.random.choice(["p2g load", "line replacement"])

        # apply the measure on tha basis of the chosen measure type
        if measure_type == "p2g load":

            # check if the measure is affordable
            new_costs = costs + 330000
            if new_costs <= budget:

                # increase current costs
                costs = new_costs

                # choose a random connection bus
                connection_bus = np.random.choice(net.sgen.bus.values)

                # create the new p2g load
                pp.create_load(net, bus=connection_bus, p_mw=0.05, q_mvar=0.0, name="Power2Gas")

                # store the measure in the measure table
                measures.loc[measure_count] = [measure_type, connection_bus]
                measure_count += 1

            # if the measure is not affordable
            else:
                break

        elif measure_type == "line replacement":

            # choose line to replace and check its current standard type
            line_to_replace = np.random.choice(net.line.index)
            repl_std_type = "243-AL1/39-ST1A 20.0"
            if not net.line.loc[line_to_replace, "std_type"] == repl_std_type:

                # get line length and check if measure is affordable
                line_length_km = net.line.loc[line_to_replace, "length_km"]
                new_costs = costs + line_length_km * 1000 * 55
                if new_costs <= budget:

                    # increase current costs
                    costs = new_costs

                    # replace line
                    pp.change_std_type(net, eid=line_to_replace, name=repl_std_type, element="line")

                    # store the measure in the measure table
                    measures.loc[measure_count] = [measure_type, line_to_replace]
                    measure_count += 1

                # if the measure is not affordable
                else:
                    break

    return costs, measures


def apply_best_measures(net, budget, iterations=10, grid_capacity_iterations=10):
    # initialize best values
    maximum_mean_capacity = -1
    costs_of_best_set = -1
    best_measures_set = None
    best_net = None

    for it in range(iterations):
        print(f"Best measure iteration step {it + 1}")

        # copy the network
        net_copy = copy.deepcopy(net)

        # expand the grid using the apply_random_measures function
        costs, measures = apply_random_measures(net_copy, budget)

        # examine the net grid capacity
        results = determine_grid_capacity(net_copy, grid_capacity_iterations)
        mean_capacity = results["installed_mw"].mean()

        # store the net, costs and measures if it's the new best set
        if mean_capacity > maximum_mean_capacity:
            maximum_mean_capacity = mean_capacity
            best_measures_set = measures
            costs_of_best_set = costs
            best_net = net_copy

    return best_net, costs_of_best_set, best_measures_set
