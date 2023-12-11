import pandas as pd
import pandapower as pp
import copy
import pandapower.networks as nw
from numpy.random import choice # random choice out of an list
from numpy.random import normal # normal distribution function
#%%
def violations(net:pp.pandapowerNet, limit_line:float, limit_trafo:float, limit_voltage:float):
    # run the power flow and check for vioations
    pp.runpp(net)
    if net.res_line.loading_percent.max() > limit_line:
        #print(["Line overload",net.line[net.res_line.loading_percent > loading_limit_lines].index])
        return (True, "Line \n Overloading", 1)
    elif net.res_trafo.loading_percent.max() > limit_trafo:
        #print("Trafo overload")
        return (True, "Transformer \n Overloading", 2)
    elif net.res_bus.vm_pu.max() > limit_voltage:
        #print(["Voltage violation",net.bus[net.res_bus.vm_pu > voltage_limit].index])
        return (True, "Voltage \n Violation", 3)
    else:
        return (False, None, 0)
    
def chose_bus(net:pp.pandapowerNet):
    # chose a random bus from the network to attach a new load to
    return choice(net.load.bus.values)

def get_plant_size_mw():
    # randomly get a powerinjection from a normal dristibuted set of values
    return normal(loc=0.5, scale=0.05)

def load_network():
    # load the referens network 
    return nw.mv_oberrhein(scenario="generation")

def analyze_net_results(results:pd.DataFrame):
    print(f'Analyze the capacity results.')
    mean = results["installed"].mean()
    quantile_25 = results["installed"].quantile(q=0.25)
    quantile_75 = results["installed"].quantile(q=0.75)
    print(f'The 25%-Quartile is {quantile_25:.2f} MW\nthe 50%-Quartile is {mean:.2f} MW\nthe 75%-Quartile is {quantile_75:.2f} MW')
    return [quantile_25, mean, quantile_75]

def get_net_capacity(net:pp.pandapowerNet, iterations:int, results:pd.DataFrame, budget:float, cost_dict:dict):
    print(f'Starting the iteration process.\nAdditiona grid planing is considerd.')
    
    for i in range(iterations):
        print(f'Iteration {i+1} of {iterations} is in work.')
        net_copy = copy.deepcopy(net)
        installed_mw = 0
        while 1:
            violated, violation_type, violation_code = violations(net = net_copy,
                                                                  limit_line = loading_limit_lines,
                                                                  limit_trafo = loading_limit_trafo,
                                                                  limit_voltage = voltage_limit)
            if violated:
                results.loc[i] = [installed_mw, violation_type]
                break
            else:
                plant_size = get_plant_size_mw()
                pp.create_sgen(net_copy, chose_bus(net_copy), p_mw=plant_size, q_mvar=0)
                installed_mw += plant_size

def grid_planing(net:pp.pandapowerNet,budget:float,violation_code:int, limit_line:float, limit_trafo:float, limit_voltage:float):
    remaining_budget = budget
    if violation_code == 1:
        overloaded_lines = net.line[net.res_line["loading_percent"] > limit_line]
        for i in range(len(overloaded_lines)):
            line = overloaded_lines.iloc[i]
            line_type = line["std_type"]
            line_length = line["length_km"]
            line_parallel = line["parallel"]
            if ( line_length*line_parallel*cost_dict["Replace_Line"] - remaining_budget ) > 0.0:
                pp.change_std_type()
        pass
    elif violation_code == 2:
        pass
    elif violation_code == 3:
        pass
    

budget = 3.6e6 # 3,3 Mio. € stehen zur Verfügung
cost_dict = {"Load_P2G": 0.05,
             "Cost_P2G": 330_000.00,
             "Replace_Line": 55.00
             }

availible_overhead_line_types = {"48-AL1/8-ST1A 20.0": 2.10,
                                 "94-AL1/15-ST1A 20.0": 0.350,
                                 "149-AL1/24-ST1A 20.0": 0.47,
                                 "184-AL1/30-ST1A 20.0": 0.535,
                                 "243-AL1/39-ST1A 20.0": 0.645,
                                 }
availible_ground_line_types = {"NA2XS2Y 1x95 RM/25 12/20 kV": 0.252,
                               "NA2XS2Y 1x185 RM/25 12/20 kV": 0.362,
                               "NA2XS2Y 1x240 RM/25 12/20 kV": 0.421
                               }

loading_limit_lines = 95.0
loading_limit_trafo = 100.0
voltage_limit = 1.05

net = load_network()
iterations = 10
results = pd.DataFrame(columns=["installed", "violation"])

get_net_capacity(net=net, iterations=iterations, results=results, budget=budget, cost_dict=cost_dict)
[q_25, q_50, q_75] = analyze_net_results(results=results)
#%%