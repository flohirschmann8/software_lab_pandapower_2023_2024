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
from Controller import KLController
from my_classes import W_Controller, MyGrid

matplotlib.use("Qt5Agg")


def create_data_source():
    profiles = pd.read_csv(
        "C:/Users/User/Documents/Uni/Master/1. Semester/Pandapower/Hausarbeit/csv/timeseries_exercise_4.csv", sep=";")

    ds = DFData(profiles)
    n_timesteps = len(profiles.loads)
    return profiles, ds, n_timesteps


def area3_net():
    #Knoten, Lasten und Generatoren von area_1 listen
    net = pp.from_json("C:/Users/User/Documents/Uni/Master/1. Semester/Pandapower/Hausarbeit/Netz/net_exercise_4.json")
    mg = top.create_nxgraph(net)
    buses_area3 = list(top.connected_component(mg, bus=89))
    lines_area3 = list(tool.get_connected_elements(net=net, element_type="line", buses=buses_area3))
    loads_area3 = list(tool.get_connected_elements(net=net, element_type="load", buses=buses_area3))
    sgens_area3 = list(tool.get_connected_elements(net=net, element_type="sgen", buses=buses_area3))
    buses_area1 = list(top.connected_component(mg, bus=0))
    loads_area1 = list(tool.get_connected_elements(net=net, element_type="load", buses=buses_area1))
    sgens_area1 = list(tool.get_connected_elements(net=net, element_type="sgen", buses=buses_area1))
    return net, buses_area3, lines_area3, loads_area3, sgens_area3, buses_area1, loads_area1, sgens_area1


def create_controllers(net, loads_area3, sgens_area3, loads_area1, sgens_area1, ds):
    #constcontroler für für Lasten und Generatoren von Area_1 hinzufügen
    ConstControl(net, element="load", variable="scaling", element_index=loads_area3,
                 data_source=ds, profile_name="loads")
    ConstControl(net, element="sgen", variable="scaling", element_index=sgens_area3,
                 data_source=ds, profile_name="sgens")
    ConstControl(net, element="load", variable="scaling", element_index=loads_area1,
                 data_source=ds, profile_name="loads")
    ConstControl(net, element="sgen", variable="scaling", element_index=sgens_area1,
                 data_source=ds, profile_name="sgens")

    KLController(net, max_limit_pu=1.05, min_limit_pu=0.95)
    dennis_net = MyGrid(net, 0)
    W_Controller(net, element="voltage", my_grid=dennis_net,limits_pu=[0.95, 1.05])
    return net


def create_output_writer(net, buses_area3, time_steps, output_dir):
    #ow für Spannungspegel, welche von WController geregelt werden, hinzufügen
    ow = OutputWriter(net, time_steps, output_path=output_dir, output_file_type=".xlsx", log_variables=list())

    ow.log_variable("res_bus", "vm_pu", index=buses_area3, eval_function=np.max, eval_name="Max. Spannungspegel area_3")
    ow.log_variable("res_bus", "vm_pu", index=buses_area3, eval_function=np.min, eval_name="Min. Spannungspegel area_3")

    dennis_net = MyGrid(net, 0)
    ow.log_variable("res_bus", "vm_pu", index=dennis_net.get_indices("bus"), eval_function=np.max, eval_name="Max. Spannungspegel area_1")
    ow.log_variable("res_bus", "vm_pu", index=dennis_net.get_indices("bus"), eval_function=np.min, eval_name="Min. Spannungspegel area_1")
def timeseries_area3(output_dir):
    net, buses_area3, lines_area3, loads_area3, sgens_area3, buses_area1, loads_area1, sgens_area1 = area3_net()
    profiles, ds, n_timesteps = create_data_source()
    create_controllers(net, loads_area3, sgens_area3, loads_area1, sgens_area1, ds)
    time_steps = range(0, n_timesteps)
    create_output_writer(net, buses_area3, time_steps, output_dir)
    run_timeseries(net, time_steps)


output_dir = r"C:\Users\User\Documents\Uni\Master\1. Semester\Pandapower\Hausarbeit\Zeitreihen_4.5_dennis\Output dir"
print("Results can be found in your Zeitreihen folder: {}".format(output_dir))
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
timeseries_area3(output_dir)

vm_pu_file = os.path.join(output_dir, "res_bus", "vm_pu.xlsx")
vm_pu = pd.read_excel(vm_pu_file, index_col=0)
vm_pu.plot(label="vm_pu")
plt.hlines(y=1.05, xmin=0, xmax=len(vm_pu), linestyles="dashed", label="max. limit", color="red")
plt.hlines(y=0.95, xmin=0, xmax=len(vm_pu), linestyles="dashed", color="red", label="min. limit")
plt.xlabel("Zeitschritt")
plt.ylabel("Spannungspegel [p.u.]")
plt.title("Spannungspegel")
plt.legend()
plt.grid()
plt.show()

