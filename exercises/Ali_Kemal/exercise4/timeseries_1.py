import pandas as pd
from pandapower.control.controller.const_control import ConstControl
from pandapower.timeseries.data_sources.frame_data import DFData
from pandapower.timeseries.run_time_series import run_timeseries
from pandapower.timeseries.output_writer import OutputWriter
import os
import matplotlib.pyplot as plt

data = pd.read_csv("timeseries_exercise_4.csv", sep=";", header=0)
ds = DFData(data)


def run_ts(network, buses_area2, loads_subnet, sgens_subnet, dir):
    # Loading loads and sgens of area2 in pd.DataFrame
    ld_a2 = pd.DataFrame(network.load[loads_subnet]).index
    sg_a2 = pd.DataFrame(network.sgen[sgens_subnet]).index

    # Determine time_steps through lenght of loads
    time_steps = range(0, len(data.loads))

    # ow set
    ow = OutputWriter(network, time_steps)

    # CC set to scale loads and sgens through values in csv
    ConstControl(network, element="load", variable="scaling", element_index=ld_a2, data_source=ds, profile_name="loads")
    ConstControl(network, element="sgen", variable="scaling", element_index=sg_a2, data_source=ds, profile_name="sgens")
    # Run timeseries
    run_timeseries(network, time_steps)
    # Plot results of time_series
    vm_pu_file = os.path.join(dir, "res_bus", "vm_pu.xlsx")
    vm_pu = pd.read_excel(vm_pu_file, index_col=0)
    vm_pu.plot()
    plt.xlabel("Time")
    plt.ylabel("Voltage")
    plt.legend()
    plt.grid(visible=True)
    plt.show()

