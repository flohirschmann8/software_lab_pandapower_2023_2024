import pandapower as pp
import pandapower.topology as top
import matplotlib
import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
from pandapower.timeseries import DFData
from pandapower.timeseries import OutputWriter
from pandapower.timeseries.run_time_series import run_timeseries
from pandapower.control import ConstControl
from Controller import KLController


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
    return net, buses_area3



def create_controllers(net, buses_area3, ds):
    loads_area3 = net.load.bus.isin(buses_area3)
    sgen_area3 = net.sgen.bus.isin(buses_area3)
    loads = pd.DataFrame(net.load[loads_area3]).index
    sgens = pd.DataFrame(net.sgen[sgen_area3]).index
    ConstControl(net, element="load", variable="scaling", element_index=loads,
                 data_source=ds, profile_name="loads")
    ConstControl(net, element="sgen", variable="scaling", element_index=sgens,
                 data_source=ds, profile_name="sgens")
    KLController(net, max_limit_pu=1.05, min_limit_pu=0.95)
    return net


def create_output_writer(net, buses_area3, time_steps, output_dir):
    ow = OutputWriter(net, time_steps, output_path=output_dir, output_file_type=".xlsx", log_variables=list())
    mask_hv_buses_area3 = net.bus.loc[buses_area3]
    mask_lines_area3 = net.line[(net.line.from_bus.isin(buses_area3)) & net.line.to_bus.isin(buses_area3)].index

    ow.log_variable("res_line", "loading_percent", index=mask_lines_area3, eval_function=np.max, eval_name="Max. Leitungsauslastung")
    ow.log_variable("res_bus", "vm_pu", index=mask_hv_buses_area3, eval_function=np.max, eval_name="Max. Spannungspegel")
    ow.log_variable("res_bus", "vm_pu", index=mask_hv_buses_area3, eval_function=np.min, eval_name="Min. Spannungspegel")

def timeseries_area3(output_dir):
    net, buses_area3 = area3_net()
    # n_timesteps = len(data.loads)
    profiles, ds, n_timesteps = create_data_source()
    create_controllers(net, buses_area3, ds)
    time_steps = range(0, n_timesteps)
    create_output_writer(net, buses_area3, time_steps, output_dir=output_dir)
    run_timeseries(net, time_steps)


output_dir = r"C:\Users\User\Documents\Uni\Master\1. Semester\Pandapower\Hausarbeit\Zeitreihen_4.4\Output dir"
print("Results can be found in your Zeitreihen folder: {}".format(output_dir))
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
timeseries_area3(output_dir)

vm_pu_file = os.path.join(output_dir, "res_bus", "vm_pu.xlsx")
vm_pu = pd.read_excel(vm_pu_file, index_col=0)
vm_pu.plot(label="vm_pu")
plt.hlines(y=1.05, xmin=0, xmax=len(vm_pu))
plt.hlines(y=0.95, xmin=0, xmax=len(vm_pu), color="orange")
plt.xlabel("time step")
plt.ylabel("Spannungspegel [p.u.]")
plt.title("Spannungspegel")
plt.grid()
plt.show()

