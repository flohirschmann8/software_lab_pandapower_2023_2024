import pandas as pd
import pandapower.topology as top
from pandapower import control

import matplotlib.pyplot as plt
# %matplotlib inline

import numpy as np
import pandapower as pp
from pandapower.control import ConstControl
from pandapower.timeseries import DFData
from pandapower.timeseries import OutputWriter
from pandapower.timeseries.run_time_series import run_timeseries
from exercises.lukas.excercise4.tap_control import TapController

class APC_controller(control.basic_controller.Controller):
    """
    Active Power Curtailment Controller

    This controller curtails the active power of static generators in a stepwise manner to resolve line loading congestions.
    The user can specify curtailment steps.
    controller working concept:
    When a congestion (line loaded more than 100 percent) occurs, the controller takes the following steps:
    1. Curtail the first static generator to the specified curtailment step.
    2. If congestion persists, curtail two static generators up to the specified step.
    3. Continue this process, incrementally curtailed more static generators, until all are curtailed if necessary.
    4. If congestion still exists, start again with the first static generator and curtail to the next specified step.

    Parameters:
    - net (pandapowerNet): The pandapower network.
    - idx_sgens (list): List of indices of static generators.
    - idx_lines (list): List of indices of lines in the network.
    - curtailment_steps (list): List of curtailment steps.
    - in_service (bool): Indicates if the controller is initially in service.
    - recycle (bool): Indicates if the controller is recycled.
    - order (int): Order of the controller.
    - level (int): Level of the controller.
    - **kwargs: Additional keyword arguments.

    Attributes:
    - idx_sgens (list): List of indices of static generators.
    - idx_lines (list): List of indices of lines in the network.
    - curtailment_steps (list): List of curtailment steps.
    - p_mw_original (numpy.ndarray): Original active power of static generators.
    - p_mw (numpy.ndarray): Current active power of static generators.
    - in_service (pandas.Series): In-service status of static generators.
    - applied (bool): Indicates whether the controller has been applied.

    Methods:
    - is_converged(net): Checks if there is a congestion in the network.
    - write_to_net(net): Writes the current state of the controller to the pandapower network.
    - control_step(net): Takes a control step by incrementally curtailing static generators.
    - time_step(net, time): Resets the active power to the original values and sets the applied flag to False.

    Example:
    ```python
    controller = APCController(net, idx_sgens=[1, 2, 3], idx_lines=[10, 11, 12], curtailment_steps=[0.9, 0.8, 0.7])
    ```
    """

    def __init__(self, net, idx_sgens, idx_lines, curtailment_steps, in_service=True,
                 recycle=False, order=0, level=0, **kwargs):
        super().__init__(net, in_service=in_service, recycle=recycle, order=order, level=level,
                         initial_powerflow=True, **kwargs)

        self.idx_sgens = idx_sgens
        self.idx_lines = idx_lines
        self.curtailment_steps = curtailment_steps
        self.p_mw_original = net.sgen.p_mw[net.sgen.index.isin(self.idx_sgens)].values
        self.scaling_original = net.sgen.scaling[net.sgen.index.isin(self.idx_sgens)].values
        self.p_mw = net.sgen.p_mw[net.sgen.index.isin(self.idx_sgens)].values
        # self.in_service = net.sgen.in_service[self.idx_sgens]
        self.applied = False

    def is_converged(self, net):

        ## check line congestions

        self.idx_congested_lines = self.check_line_congestions(net)

        ## check if there is a congested line exists, take a controll step.
        if len(self.idx_congested_lines):
            self.applied = False
        ## if there is no congestion write the current state of results to the net
        else:
            self.write_to_net(net)
            self.applied = True
        return self.applied

    def write_to_net(self, net):
        # Write p to the bus within the specified net
        net.sgen.p_mw[net.sgen.index.isin(self.idx_sgens)] = self.p_mw

    def check_line_congestions(self,net):
        pp.runpp(net)
        self.sorted_lines = net.res_line.loading_percent[net.line.index.isin(self.idx_lines)].sort_values(ascending=False)
        # Identify the indices of congested lines
        self.idx_congested_lines = self.sorted_lines.index[self.sorted_lines > 100]
        return self.idx_congested_lines

    def control_step(self, net):

        for i in self.curtailment_steps:

            ## check line congestions
            self.idx_congested_lines = self.check_line_congestions(net)

            for j in range(len(self.idx_sgens)):
                ### assign the sgens to be curtailed
                current_idx_sgens = self.idx_sgens[len(self.idx_sgens)-j-1:]
                ### apply curtailment considering the specified curtailment steps

                ### maximum line loaded before appling the curtailment
                before_max = self.sorted_lines.max()

                #### apply the curtailment
                net.sgen.p_mw[net.sgen.index.isin(current_idx_sgens)] *= i

                ## check line congestions
                self.idx_congested_lines = self.check_line_congestions(net)

                ### maximum line loaded after appling the curtailment
                after_max = self.sorted_lines.max()

                #### check if the curtailment increased the congestion
                if (after_max - before_max) > 0:

                    ### incease the generatoin by scaling of 1.1
                    net.sgen.scaling[net.sgen.index.isin(self.idx_sgens)] *= 1.1
                    ### return the static generators to its original status
                    net.sgen.p_mw[net.sgen.index.isin(self.idx_sgens)] = self.p_mw_original
                    ### check line congestoins after updates
                    self.idx_congested_lines = self.check_line_congestions(net)

                if len(self.idx_congested_lines):
                    ### return the original static generators installed capacity before curtailment
                    # self.p_mw = self.p_mw_original
                    net.sgen.p_mw[net.sgen.index.isin(self.idx_sgens)] = self.p_mw_original
                else:
                    break

            if not len(self.idx_congested_lines):
                self.applied = True
                self.p_mw = net.sgen.p_mw[net.sgen.index.isin(self.idx_sgens)].values
                self.write_to_net(net)
                break

    def time_step(self, net, time):
        net.sgen.p_mw[net.sgen.index.isin(self.idx_sgens)] = self.p_mw_original
        # net.sgen.scaling[net.sgen.index.isin(self.idx_sgens)] = self.scaling_original
        self.applied = False

#### import the grid
# net = pp.from_json(r".\exercises\abdalrhman\exercise_4\net_exercise_4.json")
net = pp.from_json(r"C:\Users\alfak\OneDrive\Desktop\GitHubProjects\software_lab_pandapower_2023_2024\exercises\abdalrhman\exercise_4\net_exercise_4.json")

### create function that the return buses and lines of the grid area 4
### Note i might introduce another grid into the function later for task III

def grid_area4(net):

    mg = top.create_nxgraph(net)
    buses_area4 = list(top.connected_component(mg, bus=134))

    ## indeces and number of the bueses
    idx_buses = buses_area4
    n_of_busus = len(idx_buses)
    ## indeces and number of the lines

    idx_lines = net.line.index[net.line.from_bus.isin(idx_buses) & net.line.to_bus.isin(idx_buses)]
    n_of_lines = len(idx_lines)
    ## indeces and  number of the static generators

    idx_sgens = net.sgen.index[net.sgen.bus.isin(idx_buses)]
    n_of_sgens = len(idx_sgens)

    ## indeces and number of the loads

    idx_loads = net.load.index[net.load.bus.isin(idx_buses)]
    n_of_loads = len(idx_loads)

    ##  indeces and number of the switches

    idx_switches = net.switch.index[net.switch.bus.isin(idx_buses) & net.switch.element.isin(idx_lines)]
    n_of_switches = len(idx_switches)
    ##  indeces and number of the Trafos

    idx_trafos = net.trafo.index[net.trafo.hv_bus.isin(idx_buses)]
    n_of_trafos = len(idx_trafos)

    ##  indeces and number of the ext grids

    idx_ext_grids = net.ext_grid.index[net.ext_grid.bus.isin(idx_buses)]
    n_of_ext_grids = len(idx_ext_grids)

    return idx_buses,idx_lines,idx_loads,idx_sgens

def grid_area2(net):
    mg = top.create_nxgraph(net)
    buses_area2 = list(top.connected_component(mg, bus=45))

    ## indeces and number of the bueses
    idx_buses = buses_area2
    n_of_busus = len(idx_buses)
    ## indeces and number of the lines

    idx_lines = net.line.index[net.line.from_bus.isin(idx_buses) & net.line.to_bus.isin(idx_buses)]
    n_of_lines = len(idx_lines)
    ## indeces and  number of the static generators

    idx_sgens = net.sgen.index[net.sgen.bus.isin(idx_buses)]
    n_of_sgens = len(idx_sgens)

    ## indeces and number of the loads

    idx_loads = net.load.index[net.load.bus.isin(idx_buses)]
    n_of_loads = len(idx_loads)

    ##  indeces and number of the switches

    idx_switches = net.switch.index[net.switch.bus.isin(idx_buses) & net.switch.element.isin(idx_lines)]
    n_of_switches = len(idx_switches)
    ##  indeces and number of the Trafos

    idx_trafos = net.trafo.index[net.trafo.hv_bus.isin(idx_buses)]
    n_of_trafos = len(idx_trafos)

    ##  indeces and number of the ext grids

    idx_ext_grids = net.ext_grid.index[net.ext_grid.bus.isin(idx_buses)]
    n_of_ext_grids = len(idx_ext_grids)

    return idx_buses,idx_lines,idx_loads,idx_sgens

idx_buses4,idx_lines4,idx_loads4,idx_sgens4 = grid_area4(net)
idx_buses2,idx_lines2,idx_loads2,idx_sgens2 = grid_area2(net)

idx_buses = np.r_[idx_buses2,idx_buses4]
idx_lines = np.r_[idx_lines2,idx_lines4]
idx_loads = np.r_[idx_loads2,idx_loads4]
idx_sgens = np.r_[idx_sgens2,idx_sgens4]

# profiles = pd.read_csv(r".\exercises\abdalrhman\exercise_4\timeseries_exercise_4.csv", sep=';', index_col='Unnamed: 0')
profiles = pd.read_csv(r"C:\Users\alfak\OneDrive\Desktop\GitHubProjects\software_lab_pandapower_2023_2024\exercises\abdalrhman\exercise_4\timeseries_exercise_4.csv", sep=';', index_col='Unnamed: 0')
# profiles = profiles[80:82]
# profiles = profiles.reset_index()
ds = DFData(profiles)

## create the const controllers

ConstControl(net, element='load', variable='scaling', element_index= idx_loads4,
             data_source=ds, profile_name="loads")

ConstControl(net, element='sgen', variable='scaling', element_index= idx_sgens4,
             data_source=ds, profile_name="sgens")

# creating an Object of my new build active power curtailment controller, that control static generators

APC_controller(net,idx_sgens=idx_buses4,idx_lines=idx_lines4, curtailment_steps=[0.9,0.8,0.7,0]
               , level=1, order=1)

TapController(net,tid=3, level=2, order=1)


#### define the outputwriter function
def outputwriter():

    output_dir = r".\exercises\abdalrhman\exercise_4\controlled_results_abd_merged_lukas2"

    ow = OutputWriter(net,time_steps= len(profiles),output_path=output_dir, output_file_type=".csv",log_variables=list())
    ow.log_variable('res_line', 'loading_percent', index=idx_lines4)
    ow.log_variable('res_line', 'loading_percent', index=idx_lines4, eval_function=np.max, eval_name="maximum line loading")
    ow.log_variable('res_bus', 'vm_pu', index=idx_buses4)
    ow.log_variable('res_bus', 'vm_pu', index=idx_buses4, eval_function=np.max, eval_name="maximum bus voltage")
    ow.log_variable('res_bus', 'vm_pu', index=idx_buses4, eval_function=np.min, eval_name="minimum bus voltage")


outputwriter()

### run timesieres

run_timeseries(net, time_steps= len(profiles), continue_on_divergence=False)

### importing the results

line_loadings = pd.read_csv(r".\exercises\abdalrhman\exercise_4\controlled_results_abd_merged_lukas\res_line\loading_percent.csv", sep=';', index_col='Unnamed: 0')
bus_voltages = pd.read_csv(r".\exercises\abdalrhman\exercise_4\controlled_results_abd_merged_lukas\res_bus\vm_pu.csv", sep=';', index_col='Unnamed: 0')


#######
#### this function plots grid limits vilations after applying the controller
def grid_limit_violation_plt():
    # Create a figure with two subplots (1 row, 2 columns)
    fig, axs = plt.subplots(3, 1, figsize=(12, 18))

    # Plot the first subplot (maximum bus voltage)

    line_loadings["maximum line loading"].plot(ax=axs[0])
    axs[0].axhline(y=100, color='r', linestyle='--')
    axs[0].set_xlabel("time step")
    axs[0].set_ylabel("line loading [%]")
    axs[0].set_title("Maximum line loading after activating APC and Tap changer controllers")
    axs[0].grid()


    bus_voltages["maximum bus voltage"].plot(ax=axs[1])
    axs[1].axhline(y=1.05, color='r', linestyle='--')
    axs[1].set_xlabel("time step")
    axs[1].set_ylabel("bus voltage [p.u]")
    axs[1].set_title("Maximum bus voltage after activating APC and Tap changer controllers")
    axs[1].grid()

    bus_voltages["minimum bus voltage"].plot(ax=axs[2])
    axs[2].axhline(y=0.95, color='r', linestyle='--')
    axs[2].set_xlabel("time step")
    axs[2].set_ylabel("bus voltage [p.u]")
    axs[2].set_title("Minimum bus voltage after activating APC and Tap changer controllers")
    axs[2].grid()

    # Adjust layout to prevent clipping of titles and labels
    plt.tight_layout()

    # Show the figure
    plt.show()


grid_limit_violation_plt()

