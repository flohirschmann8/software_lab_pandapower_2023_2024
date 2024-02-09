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
import matplotlib.pyplot as plt
import pandapower.toolbox as tool

data = pd.read_csv("/Users/lukaskramer/Documents/Uni/Mastersemester1/Pandapower/Unterlagen/Exam_Files/timeseries_exercise_4.csv", sep=";")
def timeseries_area2(output_dir):
    net = simple_test_net()
    n_timesteps = len(data.sgens)
    ds = create_data_source(n_timesteps)
    net = create_controllers(net, ds)
    time_steps = range(0, n_timesteps)
    create_output_writer(net, time_steps, output_dir)
    run_timeseries(net, time_steps)

def simple_test_net():
    """
Diese Funktion lädt das Netz MV-Oberrhein und und gibt es als net zurück. Zudem werden die unterschiedlichen Netzbereiche definiert.
Da in diesem Beispiel mit Netzbereich 2 gearbeitet wird, wird dieser global verfügbar gemacht.
    Returns
    -------
    net:
    Das gesamte geladene elektrische Netzwerk.
    """
    net = pp.from_json(
        "/Users/lukaskramer/Documents/Uni/Mastersemester1/Pandapower/Unterlagen/Exam_Files/net_exercise_4.json")
    mg = top.create_nxgraph(net)
    #Listet alle mit den aufgeführten Knoten (0, 45, 89, 134) auf und schreibt diese in eine Liste
    global buses_area2
    buses_area1 = list(top.connected_component(mg, bus=0))
    buses_area2 = list(top.connected_component(mg, bus=45))
    buses_area3 = list(top.connected_component(mg, bus=89))
    buses_area4 = list(top.connected_component(mg, bus=134))
    return net

def create_data_source(n_timesteps):
    """
In dieser Funktion werden die Skalierungsfaktoren für die unterschiedlichen Zeitschritte eingelesen und in einem DataFrame gespeichert.
Parameters
    ----------
    n_timesteps:
        Länge der Zeitschritte, die in der Zeitreihensimulation durchlaufen werden.

    Returns
    -------
    ds:
        DataFrame mit dem Skalierungsfaktoren für jeden Zeitschritt.
    """
    data = pd.read_csv(
        "/Users/lukaskramer/Documents/Uni/Mastersemester1/Pandapower/Unterlagen/Exam_Files/timeseries_exercise_4.csv",
        sep=";")
    ds = DFData(data)
    return ds

def create_controllers(net, ds):
    """
Diese Funktion sorgt an jeder Last und an jedem Generator in Netzbereich 2 für die Anpassung des Skalierungsfaktors in dem jeweiligen Zeitschritt.
Dazu wird werden zunächst die Generatoren und Lasten herausgefunden und im Anschluss für den jeweiligen Zeitschritt die Skalierungsfaktoren angepasst.
    Parameters
    ----------
    net:
        Das gesamte geladene elektrische Netzwerk.
    ds:
        DataFrame mit dem Skalierungsfaktoren für jeden Zeitschritt.
    Returns
    -------
    net:
        Das elektrische Netzwerk mit dem in jedem Zeitschritt angepassten Skalierungsfaktor an den Generatoren und Lasten in Netzbereich 2.
    """

    num_loads = net.load.bus.isin(buses_area2)
    num_sgen = net.sgen.bus.isin(buses_area2)
    loads = pd.DataFrame(net.load[num_loads]).index
    sgens = pd.DataFrame(net.sgen[num_sgen]).index
    ConstControl(net, element="load", variable="scaling", element_index=loads,
                 data_source=ds, profile_name="loads")
    ConstControl(net, element="sgen", variable="scaling", element_index=sgens,
                 data_source=ds, profile_name="sgens")
    return net

def create_output_writer(net, time_steps, output_dir):
    """
Diese Funktion schreibt die berechneten Ergebnisse jedes Zeitschritts in die Excel-Tabelle, welche im hinterlegten Pfad erstellt wird.
Hier werden nur die Spannungspegel (min und max) sowie die maximale Leitungsauslastung erfasst.
Weitere Variablen, die erfasst und in eine Excel geschrieben werden sollen, sind hier nicht vorgesehen.
Da hv_bus einen konstanten Spannungspegel von 1.00 hat, muss dieser ausgeschlossen werden. Dazu wird der Index des HV-Buses gesucht und mit .drop ausgeschossen.
    Parameters
    ----------
    net:
        Das elektrische Netzwerk mit den angepassten Skalierungsfaktoren für Netzbereich 2.
    time_steps:
        Der Zeitschritt, der durchlaufen werden soll.
    output_dir:
        Pfad, wo die Ergebnisse gespeichert werden sollen.
    """
    ow = OutputWriter(net, time_steps, output_path=output_dir, output_file_type=".xlsx", log_variables=list())
    mask_buses_area2_hv = net.bus.loc[buses_area2]
    hv_bus = mask_buses_area2_hv.loc[mask_buses_area2_hv["vn_kv"] == 110.0, "vn_kv"].index
    mask_buses_area2 = mask_buses_area2_hv.drop(hv_bus).index
    mask_lines_area2 = net.line[(net.line.from_bus.isin(buses_area2))&net.line.to_bus.isin(buses_area2)].index

    ow.log_variable("res_line", "loading_percent", index=mask_lines_area2, eval_function=np.max, eval_name="Max. Leitungsauslastung")
    ow.log_variable("res_bus", "vm_pu", index=mask_buses_area2, eval_function=np.max, eval_name="Max. Spannungspegel")
    ow.log_variable("res_bus", "vm_pu", index=mask_buses_area2, eval_function=np.min, eval_name="Min. Spannungspegel")


#Erstellen des Pfades, wo die Excel_Tabelle liegt.
#Falls Pfad nicht vorhanden, wird das Verzeichnis erstellt.
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
plt.axhline(y=0.95, color="r", linestyle="--", label="Grenze Unterspannung (0.95 p.u)")
plt.axhline(y=1.05, color="r", linestyle="--", label="Grenze Überspannung (1.05 p.u)")
plt.grid()
plt.show()
low_voltage = vm_pu.loc[vm_pu["Min. Spannungspegel"]<0.95, "Min. Spannungspegel"]
high_voltage = vm_pu.loc[vm_pu["Max. Spannungspegel"]>1.05, "Max. Spannungspegel"]
print(f"In", len(low_voltage), "Zeitschritten gibt es Verletzungen des unteren Spannungsbandes. Das entspricht" ,round(100*len(low_voltage)/len(vm_pu),2), "% der gesamten Zeit.")
print(f"In", len(high_voltage), "Zeitschritten gibt es Verletzungen des oberen Spannungsbandes. Das entspricht" ,round(100*len(high_voltage)/len(vm_pu),2), "% der gesamten Zeit.")
#Max. Leitungsauslastung plotten, Leitungsauslastungen aufzeigen
line_loading_file = os.path.join(output_dir, "res_line", "loading_percent.xlsx")
line_loading = pd.read_excel(line_loading_file, index_col=0)
line_loading.plot(label="Leitungsauslastung")
plt.xlabel("Zeitschritt")
plt.ylabel("Leitungsauslastung [%]")
plt.title("Leitungsauslastung")
plt.axhline(y=100, color="r", linestyle="--", label="Grenze Leitungsauslastung (100 %)")
plt.grid()
plt.show()
overloading = line_loading.loc[line_loading["Max. Leitungsauslastung"]>100, "Max. Leitungsauslastung"]
print(f"In", len(overloading), "Zeitschritten gibt es Verletzungen des oberen Spannungsbandes. Das entspricht" ,round(100*len(overloading)/len(line_loading),2), "% der gesamten Zeit.")