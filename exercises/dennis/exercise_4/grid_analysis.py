import os
import numpy as np
import pandas as pd
import tempfile
import random
import pandapower as pp
import pandapower.topology as top
import pandapower.toolbox as tool
import pandapower.plotting as plot
from pandapower.timeseries import DFData
from pandapower.timeseries import OutputWriter
from pandapower.timeseries.run_time_series import run_timeseries
from pandapower.control import ConstControl
from matplotlib import pyplot as plt
# to make the plots pretty i use the seaborn module to set a good theme
import seaborn as sns 
sns.set_theme()

##########################################
######## import the grid #################
##########################################

whole_grid = pp.from_json(filename="net_exercise_4.json")

my_area = 2 # i choose the area 3 to be mine for this exercise and because the indexing of the ext_grids starts at 0 not 1, my ext_grid index is 2

##########################################
############# Task I.1 ###################
##########################################

# get the connectet busses of my ext_grid from the topology module

net_graph = top.create_nxgraph(net=whole_grid)

my_ext_grid = whole_grid.ext_grid.loc[[my_area],:]

grid_search_starting_bus = my_ext_grid["bus"].values[0]
my_busses_indices = list(top.connected_component(mg=net_graph,bus=grid_search_starting_bus))
my_busses = whole_grid.bus.loc[my_busses_indices,:]

my_lines_indices = list(tool.get_connected_elements(net=whole_grid,element_type="line",buses=my_busses_indices))
my_lines = whole_grid.line.loc[my_lines_indices,:]

my_loads_indices = list(tool.get_connected_elements(net=whole_grid,element_type="load",buses=my_busses_indices))
my_loads = whole_grid.load.loc[my_loads_indices,:]

my_sgen_indices = list(tool.get_connected_elements(net=whole_grid,element_type="sgen",buses=my_busses_indices))
my_sgen = whole_grid.sgen.loc[my_sgen_indices,:]

my_trafo_indices = list(tool.get_connected_elements(net=whole_grid,element_type="trafo",buses=my_busses_indices))
my_trafo = whole_grid.trafo.loc[my_trafo_indices,:]

# get the general information about my grid area

number_of_nodes_in_my_area = len(my_busses_indices)
number_of_lines_in_my_area = len(my_lines_indices)
number_of_loads_in_my_area = len(my_loads_indices)
number_of_sgen_in_my_area = len(my_sgen_indices)
installed_load_power = my_loads["p_mw"].sum()
installed_sgen_power = my_sgen["p_mw"].sum()
line_length_in_my_area = my_lines["length_km"].sum()

# plot the whole grid with my area higlighted

color_fundamental_grid = "gray"
color_my_grid = "blue"

size_nodes = 10
size_trafo = 20
size_ext_grid = 80

# to plot the whole grid in one color and my area of it in another, i first color all the grid elements that i want to plot in gray as a background
all_bus_collection = plot.create_bus_collection(net=whole_grid, buses=whole_grid.bus.index, color=color_fundamental_grid, size=size_nodes)
all_line_collection = plot.create_line_collection(net=whole_grid, lines=whole_grid.line.index, color=color_fundamental_grid, use_bus_geodata=True)
all_trafo_collection = plot.create_trafo_collection(net=whole_grid, trafos=whole_grid.trafo.index, color=color_fundamental_grid, size=size_trafo)
all_ext_grid_collection = plot.create_ext_grid_collection(net=whole_grid, ext_grids=whole_grid.ext_grid.index, color=color_fundamental_grid, size=size_ext_grid)

collection_whole_grid = [all_bus_collection, all_line_collection,all_trafo_collection, all_ext_grid_collection]

# to color my grid area in another color, i use the indices of the busses, lines, loads, sgens and trafos that are in my area 
# and color them in blue
my_bus_collection = plot.create_bus_collection(net=whole_grid, buses=my_busses_indices, color=color_my_grid, size=size_nodes)
my_line_collection = plot.create_line_collection(net=whole_grid, lines=my_lines_indices, color=color_my_grid, use_bus_geodata=True)
my_trafo_collection = plot.create_trafo_collection(net=whole_grid, trafos=my_trafo_indices, color=color_my_grid, size=size_trafo)
my_ext_grid_collection = plot.create_ext_grid_collection(net=whole_grid, ext_grids=my_ext_grid.index, color=color_my_grid, size=size_ext_grid)

collection_my_grid = [my_bus_collection, my_line_collection, my_trafo_collection, my_ext_grid_collection]

# after creating the two collection of elements, i add them together into a single list of collection, that then are plotted
collection_to_draw = collection_whole_grid + collection_my_grid

# the text box with the grid information about my seleced area is offset from a specific node in the grid. As the refrence node i chose the infead node of the 
# external grid number 2. The coordinates of the text box is then offset to the white area in the bottom right of the figure.
referenc_coords = whole_grid.bus_geodata.iloc[89]
coords_information_text = {'x':referenc_coords.x+5_000,
                           'y':referenc_coords.y-11_000}

# i want to add the important information about my area of the grid to the plot of it.
# in the next lines i create a multiple row f-String to contain all information i want to relate about my grid area
info_text_my_area = f'''Grid information:\n
Number of nodes = {number_of_nodes_in_my_area}\n
Number of lines = {number_of_lines_in_my_area}, total length = {line_length_in_my_area:.2f} km\n
Number of loads = {number_of_loads_in_my_area}, installed power = {installed_load_power:.2f} MW\n
Number of sgen =  {number_of_sgen_in_my_area}, installed power = {installed_sgen_power:.2f} MW
'''

ax_pp = plot.draw_collections(collections=collection_to_draw)
ax_pp.text(x=coords_information_text["x"],y=coords_information_text["y"],s=info_text_my_area)
plt.savefig(fname="Task_1_colored_grid.png")

##########################################
############# Task I.2 ###################
##########################################

# load the time series data and create the data source object
ts_profiles = pd.read_csv(filepath_or_buffer="timeseries_exercise_4.csv",sep=';',index_col=0)
number_of_time_steps = len(ts_profiles["loads"])
profile_time_steps = range(0, number_of_time_steps)
ds = DFData(df=ts_profiles)

# create the Constcontroler for the loads and generators
ConstControl(net=whole_grid, element='load', variable='scaling', element_index=my_loads_indices,
             data_source=ds, profile_name="loads")
ConstControl(net=whole_grid, element='sgen', variable='scaling', element_index=my_sgen_indices,
             data_source=ds, profile_name="sgens")


# create the output path
output_folder = "time_series_results"
output_path = os.path.join(os.getcwd(),output_folder)
if not os.path.exists(output_path):
    os.mkdir(output_path)

# create the outputwriter
ow = OutputWriter(net=whole_grid, time_steps=profile_time_steps, output_path=output_path, output_file_type=".xlsx", log_variables=list())
ow.log_variable(table="res_bus", variable="vm_pu", index=my_busses_indices, eval_function=np.max, eval_name="max. voltage")
ow.log_variable(table="res_bus", variable="vm_pu", index=my_busses_indices, eval_function=np.min, eval_name="min. voltage")
ow.log_variable(table="res_line", variable="loading_percent", index=my_lines_indices, eval_function=np.max, eval_name="max. line loading")

# %% run the time series
run_timeseries(net=whole_grid, time_steps=profile_time_steps)


# %% read in the results from the time series calculation

df_res_bus = pd.read_excel(io=os.path.join(output_path,"res_bus\\vm_pu.xlsx"),index_col=0)
df_res_line = pd.read_excel(io=os.path.join(output_path,"res_line\\loading_percent.xlsx"),index_col=0)

# plot the results of the time series calculations

# plot of the voltage results
# in the next line i create a figure with 2 subplots to show the voltage and line loading in one image
fig, axs = plt.subplots(nrows=1,ncols=2,figsize=(15,8))
fig.suptitle("Resutls from the time series calculation in task 2",size=18)
axs[0].plot(df_res_bus.index,df_res_bus["max. voltage"],label="max. voltage")
axs[0].plot(df_res_bus.index,df_res_bus["min. voltage"],label="min. voltage")
axs[0].hlines(y=1.05, xmin=0, xmax=len(df_res_bus.index),linestyles="dashed",label="bounds",color="red")
axs[0].hlines(y=0.95, xmin=0, xmax=len(df_res_bus.index),linestyles="dashed",color="red")
axs[0].set(xlabel="Time Step",ylabel="voltage [p.u.]")
axs[0].legend()

axs[1].plot(df_res_line.index,df_res_line["max. line loading"],label="max. line loading")
axs[1].hlines(y=100.0, xmin=0, xmax=len(df_res_line.index),linestyles="dashed",label="bounds",color="red")
axs[1].set(xlabel="Time Step",ylabel="voltage [p.u.]")
axs[1].legend()
plt.savefig("Tast_2_reslts.png")
