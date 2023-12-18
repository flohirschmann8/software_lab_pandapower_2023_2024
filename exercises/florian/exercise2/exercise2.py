import pandapower as pp
import pandapower.networks as nw

from functions_exercise2 import plot_network_state


# ========== TASK 1 ==========

# LOAD MV_OBERRHEIN
net = nw.mv_oberrhein(scenario="generation")

# INCREASE FEED-IN POWER
net.sgen["p_mw"] *= 3.4


# ========== TASK 2 ==========

# RUN A POWER FLOW
pp.runpp(net)

# CALL THE PLOTTING FUNCTIONS
plot_network_state(net, color_map_type="discrete")


# ========== TASK 3 ==========

# RUN A POWER FLOW
pp.runpp(net)

# IDENTIFY OVERLOADED LINES
overloaded_lines = net.res_line.loc[net.res_line["loading_percent"] > 100].index
print("\nOverloaded lines:")
print(net.res_line.loc[overloaded_lines, "loading_percent"])

# CHECK STANDARD TYPES OF OVERLOADED LINES
print("\nStandard types:")
print(net.line.loc[overloaded_lines, "std_type"])

# REPLACE OVERLOADED LINES
pp.change_std_type(net, eid=54, name="149-AL1/24-ST1A 20.0", element="line")
# ALTERNATIVE: net.line.loc[54, "parallel"] = 2
pp.change_std_type(net, eid=179, name="NA2XS2Y 1x240 RM/25 12/20 kV", element="line")
pp.change_std_type(net, eid=192, name="NA2XS2Y 1x240 RM/25 12/20 kV", element="line")


# ========== TASK 4 ==========

# RUN A POWER FLOW
pp.runpp(net)

# CHECK IF BOTTLENECKS PERSIST USING THE PLOTTING FUNCTIONS
plot_network_state(net, color_map_type="discrete")

# CHECK IF BOTTLENECKS PERSIST USING DATAFRAMES
overloaded_lines = net.res_line.loc[net.res_line["loading_percent"] > 100].index
print("\nOverloaded lines:")
print(net.res_line.loc[overloaded_lines, "loading_percent"])
