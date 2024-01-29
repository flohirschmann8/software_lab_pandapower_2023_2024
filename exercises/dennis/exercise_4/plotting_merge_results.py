import os
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
sns.set_theme()

output_folder = "Task_4_results"

# create the output path
output_path = os.path.join(os.getcwd(),output_folder)
if not os.path.exists(output_path):
    os.mkdir(output_path)

# read in the results from the time series calculation

df_res_bus = pd.read_excel(io=os.path.join(output_path,"res_bus\\vm_pu.xlsx"),index_col=0)
df_res_line = pd.read_excel(io=os.path.join(output_path,"res_line\\loading_percent.xlsx"),index_col=0)

fig, axs = plt.subplots(nrows=2,ncols=1,figsize=(15,8))
fig.suptitle("Comparison of the subgrids from Dennis and Lukas",size=18)
axs[0].plot(df_res_bus.index,df_res_bus["subgrid max. voltage"],label="max. v_pu Dennis")
axs[0].plot(df_res_bus.index,df_res_bus["subgrid min. voltage"],label="min. v_pu Dennis")

axs[0].plot(df_res_bus.index,df_res_bus["Lukas subgrid max. voltage"],label="max. v_pu Lukas")
axs[0].plot(df_res_bus.index,df_res_bus["Lukas subgrid min. voltage"],label="min. v_pu Lukas")

axs[0].hlines(y=1.05, xmin=0, xmax=len(df_res_bus.index),linestyles="dashed",label="limits",color="red")
axs[0].hlines(y=0.95, xmin=0, xmax=len(df_res_bus.index),linestyles="dashed",color="red")
axs[0].set(xlabel="Time Step",ylabel="voltage [p.u.]")
axs[0].legend()
# adjusting the position of the legend in the plot
box_0 = axs[0].get_position()
axs[0].set_position([box_0.x0, box_0.y0, box_0.width*0.9, box_0.height])
axs[0].legend(loc='center right', bbox_to_anchor=(box_0.x1*1.33,0.5))

axs[1].plot(df_res_line.index,df_res_line["subgrid max. line loading"],label="max. line loading Dennis")
axs[1].plot(df_res_line.index,df_res_line["Lukas subgrid max. line loading"],label="max. line loading Lukas")
axs[1].hlines(y=100.0, xmin=0, xmax=len(df_res_line.index),linestyles="dashed",label="limit",color="red")
axs[1].set(xlabel="Time Step",ylabel="line loading [%]")
axs[1].legend()
# adjusting the position of the legend in the plot
box_1 = axs[1].get_position()
axs[1].set_position([box_1.x0, box_1.y0, box_1.width*0.9, box_1.height])
axs[1].legend(loc='center right', bbox_to_anchor=(box_1.x1*1.375,0.5))

plt.savefig("comp_res_dennis_lukas.png")