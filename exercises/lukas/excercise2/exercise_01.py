import pandapower as pp
import matplotlib.pyplot as plt
import pandas as pd

#Erstellen eines leeren Netzwerks
net = pp.create_empty_network()

#Erstellen der Knoten
bus0 = pp.create_bus(net, vn_kv=10, name= "Bus 0", geodata=(1.5,0))
bus1 = pp.create_bus(net, vn_kv=0.4, name= "Bus 1", geodata=(1.5,-1))
bus2 = pp.create_bus(net, vn_kv=0.4, name= "Bus 2", geodata=(0, -2))
bus3 = pp.create_bus(net, vn_kv=0.4, name= "Bus 3", geodata=(0, -3))
bus4 = pp.create_bus(net, vn_kv=0.4, name= "Bus 4", geodata=(1.5, -4))
bus5 = pp.create_bus(net, vn_kv=0.4, name= "Bus 5", geodata=(3, -2))
bus6 = pp.create_bus(net, vn_kv=0.4, name= "Bus 6", geodata=(3, -3))

#Erstellen des externen Netzes
pp.create_ext_grid(net, bus = bus0, vm_pu= 1.0, va_degree=0)

#Erstellen der Lasten
load2 = pp.create_load(net, bus=bus2, p_mw=0.015, q_mvar=-0.01, name="Load Bus 2")
load3 = pp.create_load(net, bus=bus3, p_mw=0.005, q_mvar=0.0001, name="Load Bus 3")
load4 = pp.create_load(net, bus=bus4, p_mw=0.025, q_mvar=-0.005, name="Load Bus 4")
load6 = pp.create_load(net, bus=bus6, p_mw=0.01378, q_mvar=0.00453, name="Load Bus 6")

#Erstellen der statischen Generatoren
gen1 = pp.create_sgen(net, bus1, p_mw=0.035, q_mvar=-0.005, name="Generator Bus 1")
gen2 = pp.create_sgen(net, bus2, p_mw=0.002, q_mvar=-0.0002, name="Generator Bus 2")
gen3 = pp.create_sgen(net, bus3, p_mw=0.01, name="Generator Bus 3")
gen5 = pp.create_gen(net, bus5, p_mw=0.1, vm_pu=1.0, name="Generator Bus 5")
gen6 = pp.create_sgen(net, bus6, p_mw=0.007, q_mvar=0.001, name="Generator Bus 6")

#Erstellen des Trafos
pp.create_transformer(net, hv_bus=bus0, lv_bus=bus1, std_type="0.63 MVA 10/0.4 kV")

#Erstellen der Leitungen
line1 = pp.create_line(net, from_bus=bus1, to_bus=bus2, length_km=0.72, std_type="NAYY 4x50 SE")
line2 = pp.create_line(net, from_bus=bus2, to_bus=bus3, length_km=1.5, std_type="NAYY 4x50 SE")
line3 = pp.create_line(net, from_bus=bus3, to_bus=bus4, length_km=0.3, std_type="NAYY 4x50 SE")
line4 = pp.create_line(net, from_bus=bus1, to_bus=bus5, length_km=0.14, std_type="NAYY 4x50 SE")
line5 = pp.create_line(net, from_bus=bus5, to_bus=bus6, length_km=0.17, std_type="NAYY 4x50 SE")
line6 = pp.create_line(net, from_bus=bus6, to_bus=bus4, length_km=0.5, std_type="NAYY 4x50 SE")

#Erstellen des Schalters
sw1 = pp.create_switch(net, bus4, line3, et="l", closed= False, type="LBS")

#Anpassung der Leistung von Load Bus 4 und Generator Bus 5
net.gen.p_mw.loc[0] = 0.057
net.load.p_mw.loc[load4] = 0.015

#PowerFlow und Anzeigen der Ergebnisse
pp.runpp(net)
print(net.res_bus)
print(net.res_line)

#Alle Zeilen und Spalten anzeigen
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

#Plotten des Netzwerks
pp.plotting.simple_topology(net)
plt.show()


