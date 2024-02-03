import pandapower as pp
import pandapower.networks as nw
import pandas as pd
import copy
import matplotlib.pyplot as plt



iterations = 100
results = pd.DataFrame(columns=["installed", "violation"])

#Funktion get_plant_size_mw gibt einen zufälligen Wert aus einer Normalverteilung zurück (Mittelwert: 0.5, Abweichung 0.05)
from numpy.random import normal
def get_plant_size_mw():
    return normal(loc=0.5, scale=0.05)

#Funktion chose_bus(net) wählt einen zufälligen Knoten des Netzwerks aus
from numpy.random import choice
def chose_bus(net):
    return choice(net.load.bus.values)
#Definition von Grenzwertverletzungen (hier >90% Auslastung bzw. Spannungspegel >106%
def violations(net):
    pp.runpp(net)
    if net.res_line.loading_percent.max() > 50:
        return (True, "Line \n Overloading")
    elif net.res_trafo.loading_percent.max() > 50:
        return (True, "Transformer \n Overloading")
    elif net.res_bus.vm_pu.max() > 1.06:
        return (True, "Voltage \n Violation")
    else:
        return (False, None)

def load_network():
    return nw.mv_oberrhein(scenario="generation")

for i in range(iterations):
    net = load_network()
    installed_mw = 0
    while 1:
        violated, violation_type = violations(net)
        if violated:
            results.loc[i] = [installed_mw, violation_type]
            break
        else:
            plant_size = get_plant_size_mw()
            pp.create_sgen(net, chose_bus(net), p_mw=plant_size, q_mvar=0)
            installed_mw += plant_size
            net_copy = copy.deepcopy(net)

summation = sum(results.installed)
arithmetic_mean = summation / iterations

plt.boxplot(results.installed)
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.ylabel("Installed Capacity [MW]")
plt.show()

