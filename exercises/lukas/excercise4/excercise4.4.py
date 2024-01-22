import os
import numpy as np
import pandas as pd
import tempfile
import pandapower as pp
import pandapower.topology as top
from pandapower.control import ConstControl
from pandapower.timeseries import DFData
from pandapower.timeseries import OutputWriter
from pandapower.timeseries.run_time_series import run_timeseries
from exercises.lukas.excercise4.tap_control import TapController
import matplotlib.pyplot as plt

data = pd.read_csv("/Users/lukaskramer/Documents/Uni/Mastersemester1/Pandapower/Unterlagen/Exam_Files/timeseries_exercise_4.csv", sep=";")
ds = DFData(data)
def timeseries_area2(output_dir):
    net = net_exam()
    n_timesteps = len(data.sgens)
    ds = create_data_source(n_timesteps)
    net = create_controllers(net, ds)
    time_steps = range(0, n_timesteps)
    TapController(net, tid=tid)
    create_output_writer(net, time_steps, output_dir)
    run_timeseries(net, time_steps)

def net_exam():
    net = pp.from_json(
        "/Users/lukaskramer/Documents/Uni/Mastersemester1/Pandapower/Unterlagen/Exam_Files/net_exercise_4.json")
    mg = top.create_nxgraph(net)
    # Zählt alle Knoten auf, die mit Bus 0, 45, 89 und 134 verbunden sind
    global buses_area2
    global tid
    buses_area2 = list(top.connected_component(mg, bus=45))
    for i in net.trafo.hv_bus.isin(buses_area2).index:
        if net.trafo.hv_bus.isin(buses_area2).loc[i]:
            tid = i
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
    for i in net.trafo.hv_bus.isin(buses_area2).index:
        if net.trafo.hv_bus.isin(buses_area2).loc[i]:
            trafo_area2 = i
    for j in net.ext_grid.bus.isin(buses_area2).index:
        if net.ext_grid.bus.isin(buses_area2).loc[j]:
            ext_grid_area2 = j

    #Ergebnisse in Excel schreiben
    ow.log_variable("res_line", "loading_percent", index=mask_lines_area2, eval_function=np.max, eval_name="Max. Leitungsauslastung")
    ow.log_variable("res_bus", "vm_pu", index=mask_buses_area2, eval_function=np.max, eval_name="Max. Spannungspegel")
    ow.log_variable("res_bus", "vm_pu", index=mask_buses_area2, eval_function=np.min, eval_name="Min. Spannungspegel")
    ow.log_variable("trafo", "tap_pos", index=trafo_area2, )
    ow.log_variable("res_ext_grid", "p_mw", index=ext_grid_area2)
    return ow

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
plt.axhline(y=0.95, color="r", linestyle="--", label="Grenze Unterspannung (0.95 p.u)")
plt.axhline(y=1.05, color="r", linestyle="--", label="Grenze Überspannung (1.05 p.u)")
plt.show()
low_voltage = vm_pu.loc[vm_pu["Min. Spannungspegel"] < 0.95, "Min. Spannungspegel"]
high_voltage = vm_pu.loc[vm_pu["Max. Spannungspegel"] > 1.05, "Max. Spannungspegel"]
print(f"In", len(low_voltage), "Zeitschritten gibt es Verletzungen des unteren Spannungsbandes. Das entspricht" ,round(100*len(low_voltage)/len(vm_pu),2), "% der gesamten Zeit.")
print(f"In", len(high_voltage), "Zeitschritten gibt es Verletzungen des oberen Spannungsbandes. Das entspricht" ,round(100*len(high_voltage)/len(vm_pu),2), "% der gesamten Zeit.")

#Stufenstellung und Wirkleistung plotten
# Daten einlesen
tap_pos_file = os.path.join(output_dir, "trafo", "tap_pos.xlsx")
tap_pos = pd.read_excel(tap_pos_file, index_col=0)
p_mw_ext_grid_file = os.path.join(output_dir, "res_ext_grid", "p_mw.xlsx")
p_mw_ext_grid = pd.read_excel(p_mw_ext_grid_file, index_col=0)

# Plot für die erste Datei (tap_pos)
ax1 = tap_pos.plot()
ax1.legend(["Stufenstellung"])
ax1.set_xlabel("Zeitschritt")
ax1.set_ylabel("Stufenstellung")
ax1.grid()

# Zweite Y-Achse für die zweite Datei erstellen
ax2 = ax1.twinx()
ax2.set_ylabel("Wirkleistung")

# Plot für die zweite Datei (p_mw_ext_grid)
p_mw = p_mw_ext_grid.plot(ax=ax2, color="orange", label="Wirkleistung")
p_mw.legend(["Wirkleistung"])
plt.xlabel("Zeitschritt")
plt.grid()
plt.show()