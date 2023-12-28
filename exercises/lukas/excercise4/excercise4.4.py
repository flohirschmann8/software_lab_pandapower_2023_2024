import os
import numpy as np
import pandas as pd
import tempfile
import pandapower as pp
import pandapower.topology as top
from pandapower.control import Characteristic, ConstControl
from pandapower.timeseries import DFData
from pandapower.timeseries import OutputWriter
from pandapower.timeseries.run_time_series import run_timeseries
import matplotlib.pyplot as plt

data = pd.read_csv("/Users/lukaskramer/Documents/Uni/Mastersemester1/Pandapower/Unterlagen/Exam_Files/timeseries_exercise_4.csv", sep=";")
ds = DFData(data)

def timeseries_area2(output_dir):
    net = simple_test_net()
    tap_control(net)
    n_timesteps = len(data.sgens)
    ds = create_data_source(n_timesteps)
    net = create_controllers(net, ds)
    time_steps = range(0, n_timesteps)
    create_output_writer(net, time_steps, output_dir)
    run_timeseries(net, time_steps)

def simple_test_net():
    net = pp.from_json(
        "/Users/lukaskramer/Documents/Uni/Mastersemester1/Pandapower/Unterlagen/Exam_Files/net_exercise_4.json")
    mg = top.create_nxgraph(net)
    # Zählt alle Knoten auf, die mit Bus 0, 45, 89 und 134 verbunden sind
    global buses_area2
    buses_area1 = list(top.connected_component(mg, bus=0))
    buses_area2 = list(top.connected_component(mg, bus=45))
    buses_area3 = list(top.connected_component(mg, bus=89))
    buses_area4 = list(top.connected_component(mg, bus=134))
    return net

def create_data_source(n_timesteps):
    data = pd.read_csv(
        "/Users/lukaskramer/Documents/Uni/Mastersemester1/Pandapower/Unterlagen/Exam_Files/timeseries_exercise_4.csv",
        sep=";")
    ds = DFData(data)
    return ds

def create_controllers(net, ds):
    num_loads = net.load.bus.isin(buses_area2)
    num_sgen = net.sgen.bus.isin(buses_area2)
    for i, value in enumerate(num_loads):
        if value:
            ConstControl(net, element="load", variable="scaling", element_index=[i],
                         data_source=ds, profile_name=["loads"])
    for j, value in enumerate(num_sgen):
        if value:
            ConstControl(net, element="sgen", variable="scaling", element_index=[j],
                         data_source=ds, profile_name=["sgens"])
    return net

def create_output_writer(net, time_steps, output_dir):
    ow = OutputWriter(net, time_steps, output_path=output_dir, output_file_type=".xlsx", log_variables=list())
    #Da hv_bus einen konstanten Spannungspegel von 1.00 hat, muss dieser ausgeschlossen werden. Dazu wird der Index des HV-Buses gesucht und mit .drop ausgeschossen
    mask_buses_area2_hv = net.bus.loc[buses_area2]
    hv_bus = mask_buses_area2_hv.loc[mask_buses_area2_hv["vn_kv"] == 110.0, "vn_kv"].index
    mask_buses_area2 = mask_buses_area2_hv.drop(hv_bus).index
    mask_lines_area2 = net.line[(net.line.from_bus.isin(buses_area2))&net.line.to_bus.isin(buses_area2)].index
    #Ergebnisse in Excel schreiben
    ow.log_variable("res_line", "loading_percent", index=mask_lines_area2, eval_function=np.max, eval_name="Max. Leitungsauslastung")
    ow.log_variable("res_bus", "vm_pu", index=mask_buses_area2, eval_function=np.max, eval_name="Max. Spannungspegel")
    ow.log_variable("res_bus", "vm_pu", index=mask_buses_area2, eval_function=np.min, eval_name="Min. Spannungspegel")
    return ow
def tap_control(net):
    trafo_area2 = net.trafo[(net.trafo.hv_bus.isin(buses_area2)) & (net.trafo.lv_bus.isin(buses_area2))]
    ext_grid_area2 = net.ext_grid.bus.isin(buses_area2)
    #Index des ext. Grid herausfinden, um damit weiterzuarbeiten
    tmp=0
    for i in range(len(ext_grid_area2)):
        if ext_grid_area2[i]:
            tmp=i
    #Tabelle Wirkleistung - Stufenstellung --> Trafostufen -9 bis -6 sowie 6 bis 9 werden nicht genutzt
    c = Characteristic(net, x_values=[-20, -15, 0, 15, 20], y_values=[-5, -5, 0, 5, 5])
    pp.control.CharacteristicControl(net,
                                     output_element=net.trafo.isin(trafo_area2).astype(str),
                                     output_variable=net.trafo.isin(trafo_area2).tap_pos.astype(str),
                                     output_element_index=net.trafo.lv_bus.isin(trafo_area2).index,
                                     input_element=net.res_ext_grid.loc[tmp].astype(str),
                                     input_variable=net.res_ext_grid.loc[tmp].p_mw.astype(str),
                                     input_element_index=net.res_ext_grid.loc[tmp].index,
                                     characteristic_index=c.index)
    return net

output_dir = os.path.join(tempfile.gettempdir(), "time_series_area2")
print("Results can be found in your local temp folder: {}".format(output_dir))
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
timeseries_area2(output_dir)

#Min. und Max. Spannungspegel plotten, Verletzungen Spannungsband aufzeigen
vm_pu_file = os.path.join(output_dir, "res_bus", "vm_pu.xlsx")
vm_pu = pd.read_excel(vm_pu_file, index_col=0)
vm_pu.plot()
plt.xlabel("Zeitschritt")
plt.ylabel("Spannungspegel [p.u]")
plt.title("Spannungspegel")
plt.grid()
plt.show()
low_voltage = vm_pu.loc[vm_pu["Min. Spannungspegel"]<0.95, "Min. Spannungspegel"]
high_voltage = vm_pu.loc[vm_pu["Max. Spannungspegel"]>1.05, "Max. Spannungspegel"]
print(f"In", len(low_voltage), "Zeitschritten gibt es Verletzungen des unteren Spannungsbandes. Das entspricht" ,round(100*len(low_voltage)/len(vm_pu),2), "% der gesamten Zeit.")
print(f"In", len(high_voltage), "Zeitschritten gibt es Verletzungen des oberen Spannungsbandes. Das entspricht" ,round(100*len(high_voltage)/len(vm_pu),2), "% der gesamten Zeit.")
#Max. Leitungsauslastung plotten, Leitungsauslastungen aufzeigen
line_loading_file = os.path.join(output_dir, "res_line", "loading_percent.xlsx")
line_loading = pd.read_excel(line_loading_file, index_col=0)
"""line_loading.plot(label="Leitungsauslastung")
plt.xlabel("Zeitschritt")
plt.ylabel("Leitungsauslastung [%]")
plt.title("Leitungsauslastung")
plt.grid()
plt.show()"""
overloading = line_loading.loc[line_loading["Max. Leitungsauslastung"]>100, "Max. Leitungsauslastung"]
#print(f"In", len(overloading), "Zeitschritten gibt es Verletzungen des oberen Spannungsbandes. Das entspricht" ,round(100*len(overloading)/len(line_loading),2), "% der gesamten Zeit.")




