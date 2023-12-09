import pandapower as pp
import pandapower.networks as nw
import pandapower.plotting as plot
from matplotlib import pyplot as plt


# %%
#############################################################################################
#############################################################################################
# preambel

show_task_1 = False
show_task_2 = False
show_task_3 = False
show_task_4 = False

# load the network
mv_oberrhein = nw.mv_oberrhein(scenario="generation")

# scaling factors before update
scaling_before = mv_oberrhein.sgen["p_mw"]
if show_task_1:
    print(mv_oberrhein.sgen.loc[0:5,["p_mw","q_mvar"]])

#############################################################################################
#############################################################################################
# task 1
# updating the real power to increse the real power by a factor of 3.4

mv_oberrhein.sgen.loc[:,"p_mw"] = mv_oberrhein.sgen.loc[:,"p_mw"] * 3.4
if show_task_1:
    print(mv_oberrhein.sgen.loc[0:5,["p_mw","q_mvar"]])

#############################################################################################
#############################################################################################
# task 2
# colorcoding the overloaded lines in the grid

pp.runpp(net=mv_oberrhein)
if show_task_2:
    print(mv_oberrhein.res_line[mv_oberrhein.res_line["loading_percent"] > 100.0])

cmap_list_line = [(0, "green"), (100, "yellow"), (101, "red")]
cmap_line, norm_line =plot.cmap_continuous(cmap_list=cmap_list_line)

cmap_list_bus = [(0.95, "blue"), (1.0, "green"), (1.05, "red")]
cmap_bus, norm_bus = plot.cmap_continuous(cmap_list=cmap_list_bus)

# figure 1 for task 2

plt.figure(0)
# create the collection of lines and busses
line_collection = plot.create_line_collection(net=mv_oberrhein, lines=mv_oberrhein.line.index, cmap=cmap_line, norm=norm_line, linewidth=2, zorder=1)
bus_collection = plot.create_bus_collection(net=mv_oberrhein, buses=mv_oberrhein.bus.index, cmap=cmap_bus, norm=norm_bus, zorder=2, size=60)

# draw the grid
plot.draw_collections([line_collection, bus_collection])

overloaded_lines = mv_oberrhein.line[mv_oberrhein.res_line["loading_percent"] > 100.0]
# creating a function to replace lines with other std-type lines
# %%
def replace_lines(net,lines,new_std_type: str):
    
    for i in range(len(lines)):
        temp_line = lines.iloc[i]        
        temp_index = temp_line.name
        temp_geodata_line = net.line_geodata.loc[temp_index,"coords"]
        [temp_name, temp_from_bus, temp_to_bus,
         temp_length, temp_parallel, temp_in_service] = temp_line[["name", "from_bus", "to_bus", "length_km",
                                                                           "parallel", "in_service"]]        
        new_line = pp.create_line(net=net, from_bus=temp_from_bus, to_bus=temp_to_bus, length_km=temp_length, std_type=new_std_type,
                       parallel=temp_parallel, in_service=temp_in_service, name=temp_name)
        net.line_geodata.loc[new_line,"coords"] = temp_geodata_line
    pp.drop_lines(net=net,lines=lines.index)

replacement_std_type = "NA2XS2Y 1x240 RM/25 12/20 kV"

replace_lines(net=mv_oberrhein, lines=overloaded_lines, new_std_type=replacement_std_type)

pp.runpp(net=mv_oberrhein)    

# figure 2 for task 2

plt.figure(1)

# new line collection

new_line_collection = plot.create_line_collection(net=mv_oberrhein, lines=mv_oberrhein.line.index, cmap=cmap_line, norm=norm_line, linewidth=2, zorder=1)
new_bus_collection = plot.create_bus_collection(net=mv_oberrhein, buses=mv_oberrhein.bus.index, cmap=cmap_bus, norm=norm_bus, zorder=2, size=60)

plot.draw_collections([new_line_collection, new_bus_collection])

# one line is still overloaded and one more parallel line is needet, because there is no std-type with a higher max_i_ka

overloaded_lines = mv_oberrhein.line[mv_oberrhein.res_line["loading_percent"] > 100.0]

mv_oberrhein.line.loc[overloaded_lines.index,"parallel"] = 2

pp.runpp(net=mv_oberrhein)

# new line collection

new_line_collection_2 = plot.create_line_collection(net=mv_oberrhein, lines=mv_oberrhein.line.index, cmap=cmap_line, norm=norm_line, linewidth=2, zorder=1)
new_bus_collection_2 = plot.create_bus_collection(net=mv_oberrhein, buses=mv_oberrhein.bus.index, cmap=cmap_bus, norm=norm_bus, zorder=2, size=60)

plot.draw_collections([new_line_collection_2, new_bus_collection_2])

#%%
plt.show()