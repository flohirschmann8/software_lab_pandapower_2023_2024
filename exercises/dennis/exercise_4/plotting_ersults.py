# %%
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
# %%
res_bus_dennis = pd.read_excel(io="Task_4_subgrid_results\\res_bus\\vm_pu.xlsx", index_col=0)
res_bus_lukas = pd.read_excel(io="Lukas_subgrid_results\\res_bus\\vm_pu.xlsx", index_col=0)

res_line_dennis = pd.read_excel(io="Task_4_subgrid_results\\res_line\\loading_percent.xlsx", index_col=0)
res_line_lukas = pd.read_excel(io="Lukas_subgrid_results\\res_line\\loading_percent.xlsx", index_col=0)

res_bus_grid = pd.read_excel(io="Task_4_grid_results\\res_bus\\vm_pu.xlsx", index_col=0)
res_line_grid = pd.read_excel(io="Task_4_grid_results\\res_line\\loading_percent.xlsx", index_col=0)

# %%

fig, axs = plt.subplots(nrows=2,ncols=1,figsize=(15,8))
fig.suptitle("Comparison of the subgrids from Dennis and Lukas",size=18)
axs[0].plot(res_bus_dennis.index,res_bus_dennis["max. voltage"],label="max. v_pu Dennis")
axs[0].plot(res_bus_dennis.index,res_bus_dennis["min. voltage"],label="min. v_pu Dennis")

axs[0].plot(res_bus_lukas.index,res_bus_lukas["max. voltage"],label="max. v_pu Lukas")
axs[0].plot(res_bus_lukas.index,res_bus_lukas["min. voltage"],label="min. v_pu Lukas")

axs[0].hlines(y=1.05, xmin=0, xmax=len(res_bus_dennis.index),linestyles="dashed",label="limits",color="red")
axs[0].hlines(y=0.95, xmin=0, xmax=len(res_bus_dennis   .index),linestyles="dashed",color="red")
axs[0].set(xlabel="Time Step",ylabel="voltage [p.u.]")
axs[0].legend()

axs[1].plot(res_line_dennis.index,res_line_dennis["max. line loading"],label="max. line loading Dennis")
axs[1].plot(res_line_lukas.index,res_line_lukas["max. line loading"],label="max. line loading Lukas")
axs[1].hlines(y=100.0, xmin=0, xmax=len(res_line_dennis.index),linestyles="dashed",label="limit",color="red")
axs[1].set(xlabel="Time Step",ylabel="line loading [%]")
axs[1].legend()

plt.savefig("comp_res_dennis_lukas.png")