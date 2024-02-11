
'''
#Determining lines of subnet - DRAFT

lines_subnet = []
x = 0
y = 1
for x in range(0, len(net.line)):
    if net.line.from_bus[x] == buses_area2[y]:
        lines_subnet.append(x)
        x = 0
        y += 1
        print("met")
    else:
        x += 1
    print(x)
    print(y)


print("The subnet includes ", len(lines_subnet), "lines.")

print (net.line.from_bus[0])
print (buses_area2[0])
'''
'''


import csv
import matplotlib.pyplot as plt
import exercise
import pandapower as pp
from pandapower.control.controller.const_control import ConstControl
from pandapower.timeseries.run_time_series import run_timeseries
import pandapower.timeseries
import pandas as pd
from pandapower.timeseries.data_sources.frame_data import DFData

def timeseries():
    time = []
    loads = []
    sgens = []

    # Open and read csv file
    with open('timeseries_exercise_4.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=";")
        # Write rows time, loads, and sgens into lists
        for row in csv_reader:
            # Die Werte der aktuellen Zeile den entsprechenden Listen hinzufügen
            time.append(row[0])
            loads.append(row[1])
            sgens.append(row[2])

    del time[0]
    del loads[0]
    del sgens[0]

    time_list = list(map(int, time))
    loads_list = list(map(float, loads))
    sgens_list = list(map(float, sgens))


    #______

    # Laden Sie die Zeitreihendaten aus der CSV-Datei
    #time_series_dt = pd.read_csv("timeseries_exercise_4.csv")

    #time_series_data = DFData(time_series_dt)


    # Fügen Sie die Zeitreihendaten in das Netzwerk ein
    #pp.create_time_series(exercise.net, time_series_data)

    # Definieren Sie die Konstanten für den ConstControl-Controller
    load_controller = ConstControl(exercise.net, element="loads", variable="p_kw", element_index=[1],
                                      data_source=loads_list, profile_name=0)

    generation_controller = ConstControl(exercise.net, element="sgens", variable="p_kw", element_index=[2],
                                            data_source=sgens_list, profile_name=0)

    # Führen Sie die Zeitreihensimulation durch
    run_timeseries(exercise.net, time_steps=(0, 673))

    # Zugriff auf die Ergebnisse der Simulation
    result_load = exercise.net.res_load
    result_generation = exercise.net.res_sgen

#--------------------------



# Fügen Sie eine Zeitreihensimulation hinzu
pp.create_time_steps(exercise.net, time_steps)

# Annahme: 'time_series_data' enthält Spalten 'time', 'generator', 'load'

# Erstellen von ConstControl-Controllern für Generator- und Lastwerte über die Zeit
for index, row in time_series_data.iterrows():
    time = row['time']
    generator_value = row['generator']
    load_value = row['load']

    # ConstControl für den Generatorwert
    pp.create_const_control(net, element='sgen', variable='p_kw', element_index=0,
                            value=generator_value, profile_name=time)

    # ConstControl für den Lastwert
    pp.create_const_control(net, element='load', variable='p_kw', element_index=0,
                            value=load_value, profile_name=time)

# Führen Sie die Zeitreihensimulation durch
pp.run_timeseries(net)

'''
'''
#Simulate time series

time = []
loads = []
sgens = []

# Open and read csv file
with open('timeseries_exercise_4.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=";")
    # Write rows time, loads, and sgens into lists
    for row in csv_reader:
        # Die Werte der aktuellen Zeile den entsprechenden Listen hinzufügen
        time.append(row[0])
        loads.append(row[1])
        sgens.append(row[2])

del time[0]
del loads[0]
del sgens[0]

time_list = list(map(int, time))
loads_list = list(map(float, loads))
sgens_list = list(map(float, sgens))


print(time_list[0])
print(loads_list[0])
print(sgens_list[0])

# Time series
x = 0
for x in range(time_list[0], time_list[-1]):




'''