import pandapower as pp
import pandapower.topology as top
import matplotlib
import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
import pandapower.toolbox as tool
from pandapower.timeseries import DFData
from pandapower.timeseries import OutputWriter
from pandapower.timeseries.run_time_series import run_timeseries
from pandapower.control import ConstControl


matplotlib.use("Qt5Agg")


def create_data_source():
    profiles = pd.read_csv(
        "C:/Users/User/Documents/Uni/Master/1. Semester/Pandapower/Hausarbeit/csv/timeseries_exercise_4.csv", sep=";")

    ds = DFData(profiles)
    n_timesteps = len(profiles.loads)
    return profiles, ds, n_timesteps


def area3_net():
    net = pp.from_json("C:/Users/User/Documents/Uni/Master/1. Semester/Pandapower/Hausarbeit/Netz/net_exercise_4.json")
    mg = top.create_nxgraph(net)
    buses_area3 = list(top.connected_component(mg, bus=89))
    lines_area3 = list(tool.get_connected_elements(net=net, element_type="line", buses=buses_area3))
    loads_area3 = list(tool.get_connected_elements(net=net, element_type="load", buses=buses_area3))
    sgens_area3 = list(tool.get_connected_elements(net=net, element_type="sgen", buses=buses_area3))
    return net, buses_area3, lines_area3, loads_area3, sgens_area3


def create_controllers(net, loads_area3, sgens_area3, ds):
    ConstControl(net, element="load", variable="scaling", element_index=loads_area3,
                 data_source=ds, profile_name="loads")
    ConstControl(net, element="sgen", variable="scaling", element_index=sgens_area3,
                 data_source=ds, profile_name="sgens")
    return net


def create_output_writer(net, buses_area3, lines_area3, time_steps, output_dir):
    #
    ow = OutputWriter(net, time_steps, output_path=output_dir, output_file_type=".xlsx", log_variables=list())

    ow.log_variable("res_line", "loading_percent", index=lines_area3, eval_function=np.max, eval_name="max. Leitungsauslastung")
    ow.log_variable("res_bus", "vm_pu", index=buses_area3, eval_function=np.max, eval_name="max. Spannungspegel")
    ow.log_variable("res_bus", "vm_pu", index=buses_area3, eval_function=np.min, eval_name="min. Spannungspegel")

def timeseries_area3(output_dir):
    #
    net, buses_area3, lines_area3, loads_area3, sgens_area3 = area3_net()
    profiles, ds, n_timesteps = create_data_source()
    create_controllers(net, loads_area3, sgens_area3, ds)
    time_steps = range(0, n_timesteps)
    create_output_writer(net, buses_area3, lines_area3, time_steps, output_dir=output_dir)
    run_timeseries(net, time_steps)
    print(net.res_line.loading_percent)


output_dir = r"C:\Users\User\Documents\Uni\Master\1. Semester\Pandapower\Hausarbeit\Zeitreihen_4.2\Output dir"
print("Results can be found in your Zeitreihen folder: {}".format(output_dir))
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
timeseries_area3(output_dir)

vm_pu_file = os.path.join(output_dir, "res_bus", "vm_pu.xlsx")
vm_pu = pd.read_excel(vm_pu_file, index_col=0)
vm_pu.plot(label="vm_pu")
plt.hlines(y=1.05, xmin=0, xmax=len(vm_pu), linestyles="dashed", color="red", label="max. limit")
plt.hlines(y=0.95, xmin=0, xmax=len(vm_pu), linestyles="dashed", color="red", label="min. limit")
plt.xlabel("Zeitschritte")
plt.ylabel("Spannungspegel [pu]")
plt.title("Spannungspegel")
plt.legend()
plt.grid()
plt.show()

line_loading_file = os.path.join(output_dir, "res_line", "loading_percent.xlsx")
line_loading = pd.read_excel(line_loading_file, index_col=0)
line_loading.plot(label="Leitungsauslastung")
plt.hlines(y=100, xmin=0, xmax=len(line_loading), linestyles="dashed", color="red", label="max. limit")
plt.xlabel("Zeitschritte")
plt.ylabel("Leitungsauslastung [%]")
plt.title("Leitungsauslastung")
plt.legend()
plt.grid()
plt.show()