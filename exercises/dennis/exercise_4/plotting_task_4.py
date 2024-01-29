import os
import pandas as pd
from matplotlib import pyplot as plt
# to make the plots pretty i use the seaborn module to set a good theme
import seaborn as sns 
sns.set_theme()

output_folder = "Task_4_results"

# if this variable is set to True, then results of only my subgrid are plotted 
# if this variable is set to False, then all results of the whole gtid are plotted
plot_subgrid_results = False

# create the output path
output_path = os.path.join(os.getcwd(),output_folder)
if not os.path.exists(output_path):
    os.mkdir(output_path)

# read in the results from the time series calculation

df_res_bus = pd.read_excel(io=os.path.join(output_path,"res_bus\\vm_pu.xlsx"),index_col=0)
df_res_line = pd.read_excel(io=os.path.join(output_path,"res_line\\loading_percent.xlsx"),index_col=0)

# plot the results of the time series calculations

if plot_subgrid_results == True:
    plt_figure_name = "Task_4_subgrid_results.png"
    plt_figure_title = "Results from the time series calculation in task 4\nfor my subgrid with the controller working"
    res_vm_pu_max = df_res_bus["subgrid max. voltage"]
    res_vm_pu_min = df_res_bus["subgrid min. voltage"]
    res_line_loading_max = df_res_line["subgrid max. line loading"]
else:
    plt_figure_name = "Task_4_grid_results.png"
    plt_figure_title = "Results from the time series calculation in task 4\nfor the whole grid with the controller working"
    res_vm_pu_max = df_res_bus["max. voltage"]
    res_vm_pu_min = df_res_bus["min. voltage"]
    res_line_loading_max = df_res_line["max. line loading"]

# plot of the voltage results
# in the next line i create a figure with 2 subplots to show the voltage and line loading in one image
fig, axs = plt.subplots(nrows=1,ncols=2,figsize=(15,8))
fig.suptitle(plt_figure_title,size=18)
axs[0].plot(df_res_bus.index,res_vm_pu_max,label="max. voltage")
axs[0].plot(df_res_bus.index,res_vm_pu_min,label="min. voltage")
axs[0].hlines(y=1.05, xmin=0, xmax=len(df_res_bus.index),linestyles="dashed",label="limits",color="red")
axs[0].hlines(y=0.95, xmin=0, xmax=len(df_res_bus.index),linestyles="dashed",color="red")
axs[0].set(xlabel="Time Step",ylabel="voltage [p.u.]")
axs[0].legend()

axs[1].plot(df_res_line.index,res_line_loading_max,label="max. line loading")
axs[1].hlines(y=100.0, xmin=0, xmax=len(df_res_line.index),linestyles="dashed",label="limit",color="red")
axs[1].set(xlabel="Time Step",ylabel="line loading [%]")
axs[1].legend()
plt.savefig(plt_figure_name)
plt.show()