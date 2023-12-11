import pandas as pd
import pandapower as pp
import copy
import pandapower.networks as nw
from numpy.random import choice # random choice out of an list
from numpy.random import normal # normal distribution function
#%%

########## Task 1
# function to run the powerflow and evaluate the violations

def violations(net):
    # run the power flow and check for vioations
    pp.runpp(net)
    if net.res_line.loading_percent.max() > 95:
        return (True, "Line \n Overloading")
    elif net.res_trafo.loading_percent.max() > 100:
        return (True, "Transformer \n Overloading")
    elif net.res_bus.vm_pu.max() > 1.06:
        return (True, "Voltage \n Violation")
    else:
        return (False, None)
    
def chose_bus(net):
    # chose a random bus from the network to attach a new load to
    return choice(net.load.bus.values)

def get_plant_size_mw():
    # randomly get a powerinjection from a normal dristibuted set of values
    return normal(loc=0.5, scale=0.05)

def load_network():
    # load the referens network 
    return nw.mv_oberrhein(scenario="generation")

def get_net_capacity(net,iterations,results):
    print(f'Starting the iteration process.')
    for i in range(iterations):
        print(f'Iteration {i+1} of {iterations} is in work.')
        net_copy = copy.deepcopy(net)
        installed_mw = 0
        while 1:
            violated, violation_type = violations(net_copy)
            if violated:
                results.loc[i] = [installed_mw, violation_type]
                break
            else:
                plant_size = get_plant_size_mw()
                pp.create_sgen(net_copy, chose_bus(net_copy), p_mw=plant_size, q_mvar=0)
                installed_mw += plant_size

# prepare the results pf the capacity calculation

############# Task 2

def analyze_net_results(results:pd.DataFrame):
    print(f'Analyze the capacity results.')
    mean = results["installed"].mean()
    quantile_25 = results["installed"].quantile(q=0.25)
    quantile_75 = results["installed"].quantile(q=0.75)
    print(f'The 25%-Quartile is {quantile_25:.2f} MW\nthe 50%-Quartile is {mean:.2f} MW\nthe 75%-Quartile is {quantile_75:.2f} MW')
    return [quantile_25, mean, quantile_75]

net = load_network()
iterations = 100
results = pd.DataFrame(columns=["installed", "violation"])

get_net_capacity(net=net, iterations=iterations, results=results)
[q_25, q_50, q_75] = analyze_net_results(results=results)

############# Task 3

#%%

# new fuction to determain the grid capacity with additional planung measures

budget = 3.6e6 # 3,3 Mio. € stehen zur Verfügung
PowerToGas_load = 0.05 # Load for a P2G-Plant in [MW]
cost_P2G = 330_000.00
cost_line_replacement = 55.00 # Cost per meter of line replacement

def get_opt_net_capacity(net,iterations,results):
    print(f'Starting the iteration process.\nAdditiona grid planing is considerd.')
    for i in range(iterations):
        print(f'Iteration {i+1} of {iterations} is in work.')
        net_copy = copy.deepcopy(net)
        installed_mw = 0
        while 1:
            violated, violation_type = violations(net_copy)
            if violated:
                results.loc[i] = [installed_mw, violation_type]
                break
            else:
                plant_size = get_plant_size_mw()
                pp.create_sgen(net_copy, chose_bus(net_copy), p_mw=plant_size, q_mvar=0)
                installed_mw += plant_size

def grid_planing(net:pp.pandapowerNet,budget:float,costs:list[float],measures:list[str],violation_type:str):
    while budget > 0.0:
        overloaded_lines = net.line[net.res_line["loading_percent"]]
    pass
