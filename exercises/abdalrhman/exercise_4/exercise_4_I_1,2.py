
import numpy as np
import pandas as pd

import pandapower.topology as top
import pandapower.plotting as plot

import matplotlib.pyplot as plt
# %matplotlib inline

import os

import pandapower as pp
from pandapower.control import ConstControl
from pandapower.timeseries import DFData
from pandapower.timeseries import OutputWriter
from pandapower.timeseries.run_time_series import run_timeseries


### first we import the grid

# net = pp.from_json(r"C:\Users\alfak\OneDrive\Desktop\GitHubProjects\software_lab_pandapower_2023_2024\exercises\abdalrhman\exercise_4\net_exercise_4.json")
# net = pp.from_json(filename= 'net_exercise_4.json')

net = pp.from_json(r".\exercises\abdalrhman\exercise_4\net_exercise_4.json")



plot.simple_plot(net, respect_switches=True)

#### inspect all area
mg = top.create_nxgraph(net)

buses_area1 = list(top.connected_component(mg, bus=0))
buses_area2 = list(top.connected_component(mg, bus=45))
buses_area3 = list(top.connected_component(mg, bus=89))
buses_area4 = list(top.connected_component(mg, bus=134))

####### I am choosing the area 4 to be my case study

### grid analysis TASK I,1 ####

## grid assets description of Area 4

## indeces and number of the bueses
idx_buses = buses_area4
n_of_busus = len(idx_buses)
## indeces and number of the lines

idx_lines = net.line.index[net.line.from_bus.isin(idx_buses) & net.line.to_bus.isin(idx_buses)]
n_of_lines = len(idx_lines)
## indeces and  number of the static generators

idx_sgens = net.sgen.index[net.sgen.bus.isin(idx_buses)]
n_of_sgens = len(idx_sgens)

## indeces and number of the loads

idx_loads = net.load.index[net.load.bus.isin(idx_buses)]
n_of_loads = len(idx_loads)

##  indeces and number of the switches

idx_switches = net.switch.index[net.switch.bus.isin(idx_buses)& net.switch.element.isin(idx_lines)]
n_of_switches = len(idx_switches)
##  indeces and number of the Trafos

idx_trafos = net.trafo.index[net.trafo.hv_bus.isin(idx_buses)]
n_of_trafos = len(idx_trafos)

##  indeces and number of the ext grids

idx_ext_grids = net.ext_grid.index[net.ext_grid.bus.isin(idx_buses)]
n_of_ext_grids = len(idx_ext_grids)

###### grid sketches #######

### assigning the lines and buses groups that distingush between area 4 and the other areas
lc_area4  = plot.create_line_collection(net, idx_lines, zorder=2, linewidths=2 , color = 'green')
lc_others = plot.create_line_collection(net, net.line.index[~net.line.index.isin(idx_lines)],color = 'grey')

bc_area4 = plot.create_bus_collection(net, idx_buses, size=80, zorder=2, color='blue')
bc_others = plot.create_bus_collection(net, net.bus.index[~net.bus.index.isin(idx_buses)], size=80, zorder=2,color = 'grey')

plot.draw_collections(collections=[lc_area4, lc_others,bc_area4,bc_others], figsize=(12, 8))

## draw legends for grid assets
legend_labels = [f'{n_of_busus} Buses at area 4',
                 f'{n_of_lines} Lines at area 4',

                 f'{n_of_switches} Switches at area',
                 f'{n_of_sgens} Sgen at area 4',
                 f'{n_of_loads} Loads at area 4',
                 f'{n_of_trafos} Trafo at area 4',
                 f'{n_of_ext_grids} External grid at area 4',

                 f'{len(net.line.index[~net.line.index.isin(idx_lines)])} Lines at other areas',
                 f'{len(net.bus.index[~net.bus.index.isin(idx_buses)])} Buses at other areas']
legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10),
                  plt.Line2D([0], [0], color='green', linewidth=2),

                  plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='red', markersize=10),
                  plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='red', markersize=10),
                  plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='red', markersize=10),
                  plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='red', markersize=10),
                  plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='red', markersize=10),

                  plt.Line2D([0], [0], color='grey', linewidth=2),
                  plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='grey', markersize=10)]



plt.legend(legend_handles, legend_labels, loc='lower right',fontsize=15)


plt.show()

# plt.savefig(r".\exercises\abdalrhman\exercise_4\net_exercise_4_I_1.png")



#### Grid analysis Task I,2 ################################################################
#### conducting timeseries ####


# import the grid model
net = pp.from_json(r".\exercises\abdalrhman\exercise_4\net_exercise_4.json")


## import the profiles

profiles = pd.read_csv(r".\exercises\abdalrhman\exercise_4\timeseries_exercise_4.csv", sep=';', index_col='Unnamed: 0')

## converts the Dataframe to the required format for the controllers

ds = DFData(profiles)

## create the const controllers


ConstControl(net, element='load', variable='scaling', element_index= idx_loads,
             data_source=ds, profile_name="loads")

ConstControl(net, element='sgen', variable='scaling', element_index= idx_sgens,
             data_source=ds, profile_name="sgens")

### define the output writer

output_dir = r".\exercises\abdalrhman\exercise_4"

ow = OutputWriter(net,
                  time_steps= len(profiles),
                  output_path=output_dir,
                  output_file_type=".csv",
                  log_variables=list())

### extract the line loadings of all lines at grid area 4 at all time steps

ow.log_variable('res_line', 'loading_percent', index=idx_lines)

### extract the maximum line loadings of all lines at grid area 4

ow.log_variable('res_line', 'loading_percent', index=idx_lines, eval_function=np.max, eval_name="maximum line loading")

### extract the bus voltages of all buses at grid area 4 at all time steps

ow.log_variable('res_bus', 'vm_pu', index=idx_buses)

### extract the maximum bus voltages of all buses at grid area 4

ow.log_variable('res_bus', 'vm_pu', index=idx_buses, eval_function=np.max, eval_name="maximum bus voltage")

### extract the minimum bus voltages of all buses at grid area 4

ow.log_variable('res_bus', 'vm_pu', index=idx_buses, eval_function=np.min, eval_name="minimum bus voltage")

run_timeseries(net, len(profiles))


### plotting the results

## import the line loadings and bus voltages results

line_loadings = pd.read_csv(r".\exercises\abdalrhman\exercise_4\res_line\loading_percent.csv", sep=';', index_col='Unnamed: 0')
bus_voltages = pd.read_csv(r".\exercises\abdalrhman\exercise_4\res_bus\vm_pu.csv", sep=';', index_col='Unnamed: 0')

# line loading results

### note that this is the maximum line loading at every time step, so it does not have to be the same
### line that has the maximum loading at every time step


## bus voltages results
## maximum bus voltage

def grid_limit_violation_plt():
    # Create a figure with two subplots (1 row, 2 columns)
    fig, axs = plt.subplots(3, 1, figsize=(12, 18))

    # Plot the first subplot (maximum bus voltage)

    line_loadings["maximum line loading"].plot(ax=axs[0])
    axs[0].axhline(y=100, color='r', linestyle='--')
    axs[0].set_xlabel("time step")
    axs[0].set_ylabel("line loading [%]")
    axs[0].set_title("Maximum line loading")
    axs[0].grid()


    bus_voltages["maximum bus voltage"].plot(ax=axs[1])
    axs[1].axhline(y=1.05, color='r', linestyle='--')
    axs[1].set_xlabel("time step")
    axs[1].set_ylabel("bus voltage [p.u]")
    axs[1].set_title("Maximum bus voltage")
    axs[1].grid()

    bus_voltages["minimum bus voltage"].plot(ax=axs[2])
    axs[2].axhline(y=0.95, color='r', linestyle='--')
    axs[2].set_xlabel("time step")
    axs[2].set_ylabel("bus voltage [p.u]")
    axs[2].set_title("Minimum bus voltage")
    axs[2].grid()

    # Adjust layout to prevent clipping of titles and labels
    plt.tight_layout()

    # Show the figure
    plt.show()


grid_limit_violation_plt()





