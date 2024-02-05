# %%
import os
import numpy as np
import pandas as pd
import pandapower as pp
from pandapower.timeseries import DFData
from pandapower.timeseries import OutputWriter
from pandapower.timeseries.run_time_series import run_timeseries
from pandapower.control import ConstControl
from my_classes import MyGrid,W_Controller

grid = pp.from_json(filename="net_exercise_4.json")

my_area = 2 # i choose the area 3 to be mine for this exercise and because the indexing of the ext_grids starts at 0 not 1, my ext_grid index is 2

# create an object that hold my selected subgrid
My_subgrid = MyGrid(whole_net=grid,ext_grid_subgrid=my_area)

# load the time series data and create the data source object
ts_profiles = pd.read_csv(filepath_or_buffer="timeseries_exercise_4.csv",sep=';',index_col=0)
number_of_time_steps = len(ts_profiles["loads"])
profile_time_steps = range(0, number_of_time_steps)
ds = DFData(df=ts_profiles)

# create the Constcontroler for the loads and generators
ConstControl(net=grid, element='load', variable='scaling', element_index=grid.load.index,
             data_source=ds, profile_name="loads")
ConstControl(net=grid, element='sgen', variable='scaling', element_index=grid.sgen.index,
             data_source=ds, profile_name="sgens")

W_Controller(net=grid,element="line_loading",my_grid=My_subgrid,limits_pu=[1.0])
W_Controller(net=grid,element="voltage",my_grid=My_subgrid,limits_pu=[0.95,1.05])

output_folder = "Task_4_results"

# create the output path
output_path = os.path.join(os.getcwd(),output_folder)
if not os.path.exists(output_path):
    os.mkdir(output_path)

# create the outputwriter
ow = OutputWriter(net=grid, time_steps=profile_time_steps, output_path=output_path, output_file_type=".xlsx", log_variables=list())
# logging the results of my subgrid
ow.log_variable(table="res_bus", variable="vm_pu", index=My_subgrid.get_indices(element="bus"), eval_function=np.max, eval_name="subgrid max. voltage")
ow.log_variable(table="res_bus", variable="vm_pu", index=My_subgrid.get_indices(element="bus"), eval_function=np.min, eval_name="subgrid min. voltage")
ow.log_variable(table="res_line", variable="loading_percent", index=My_subgrid.get_indices(element="line"), eval_function=np.max, eval_name="subgrid max. line loading")

ow.log_variable(table="res_bus", variable="vm_pu", index=list(grid.bus.index), eval_function=np.max, eval_name="max. voltage")
ow.log_variable(table="res_bus", variable="vm_pu", index=list(grid.bus.index), eval_function=np.min, eval_name="min. voltage")
ow.log_variable(table="res_line", variable="loading_percent", index=list(grid.line.index), eval_function=np.max, eval_name="max. line loading")

run_timeseries(net=grid)