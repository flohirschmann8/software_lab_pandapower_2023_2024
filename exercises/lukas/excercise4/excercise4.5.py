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
from pandapower.control.basic_controller import Controller
import pandapower.toolbox as tool
from exercises.lukas.excercise4.tap_control import TapController

whole_grid = pp.from_json(
        "/Users/lukaskramer/Documents/Uni/Mastersemester1/Pandapower/Unterlagen/Exam_Files/net_exercise_4.json")

my_area = 3 # i choose the area 3 to be mine for this exercise and because the indexing of the ext_grids starts at 0 not 1, my ext_grid index is 2

##########################################
############# Task I.1 ###################
##########################################

# get the connectet busses of my ext_grid from the topology module

net_graph = top.create_nxgraph(net=whole_grid)

# to get a pandas dataframe as a return value the int my_area has to be passed as a list to the .loc function
my_ext_grid = whole_grid.ext_grid.loc[[my_area],:]

# to extract the int value of the bus to start the grid search it is nessesary to extract the values of the pandas dataframe and
# out of the array of vaules the first value is the int index of the bus that the external grid is connected to
grid_search_starting_bus = my_ext_grid["bus"].values[0]
my_busses_indices = list(top.connected_component(mg=net_graph,bus=grid_search_starting_bus))
my_busses = whole_grid.bus.loc[my_busses_indices,:]

my_lines_indices = list(tool.get_connected_elements(net=whole_grid,element_type="line",buses=my_busses_indices))
my_lines = whole_grid.line.loc[my_lines_indices,:]

my_loads_indices = list(tool.get_connected_elements(net=whole_grid,element_type="load",buses=my_busses_indices))
my_loads = whole_grid.load.loc[my_loads_indices,:]

my_sgen_indices = list(tool.get_connected_elements(net=whole_grid,element_type="sgen",buses=my_busses_indices))
my_sgen = whole_grid.sgen.loc[my_sgen_indices,:]

my_trafo_indices = list(tool.get_connected_elements(net=whole_grid,element_type="trafo",buses=my_busses_indices))
my_trafo = whole_grid.trafo.loc[my_trafo_indices,:]
class MyGrid():
    """
    Create a MyGrid object, that holds the indices and elements, that belong to a subgrid of the whole grid.

    This class is used to store the bus, line, load, sgen, trafo and ext_grid indices and elements that are specific to the selectet subgrid.

    Parameters
    ----------
    whole_net : pandapowerNet
        Whole network of which the subgrid is a part of.
    bus_indices : list
        Thie indices of the busses, that are part of the subgrid as a list.
    line_indices : list
        Thie indices of the lines, that are part of the subgrid as a list.
    load_indices : list
        Thie indices of the loads, that are part of the subgrid as a list.
    sgen_indices : list
        Thie indices of the static generators, that are part of the subgrid as a list.
    ext_grid_indices : list
        Thie indices of the external grid, that are part of the subgrid as a list.
    trafo_indices : list
        Thie indices of the transformers, that are part of the subgrid as a list.

    Returns
    -------
    MyGrid
        The MyGrid object that was created.
    """

    def __init__(self, whole_net, bus_indices, line_indices, load_indices, sgen_indices, ext_grid_indices,
                 trafo_indices) -> None:

        self.my_busses = whole_net.bus.loc[bus_indices, :]
        self.my_lines = whole_net.line.loc[line_indices, :]
        self.my_loads = whole_net.load.loc[load_indices, :]
        self.my_sgens = whole_net.sgen.loc[sgen_indices, :]

        # check only one external grid is part of the subgrid.
        if type(ext_grid_indices) == list:
            # if more than one external grid is part of the subgrid the self.my_ext_gris variable is a pandas dataframe
            self.my_ext_grids = whole_net.ext_grid.loc[ext_grid_indices, :]
        else:
            # if only one external grid is part of the subgrid the self.my_ext_gris variable would ba a pandas dataframe
            # and the index of the external grid has to be passed to the .loc function as a list to get also a pandas dataframe back
            self.my_ext_grids = whole_net.ext_grid.loc[[ext_grid_indices], :]
        # see comment above the self.my_ext_grids initialization
        if type(trafo_indices) == list:
            self.my_trafos = whole_net.trafo.loc[trafo_indices, :]
        else:
            self.my_trafos = whole_net.trafo.loc[[trafo_indices], :]

    def get_indices(self, element):
        if element == "bus":
            return self.my_busses.index
        elif element == "line":
            return self.my_lines.index
        elif element == "load":
            return self.my_loads.index
        elif element == "sgen":
            return self.my_sgens.index
        elif element == "ext_grid":
            return self.my_ext_grids.index
        elif element == "trafo":
            return self.my_trafos.index

    def get_elements(self, element):
        if element == "bus":
            return self.my_busses
        elif element == "line":
            return self.my_lines
        elif element == "load":
            return self.my_loads
        elif element == "sgen":
            return self.my_sgens
        elif element == "ext_grid":
            return self.my_ext_grids
        elif element == "trafo":
            return self.my_trafos
class W_Controller(Controller):
    """
    Create a controller that limits the line loading and voltage levels in a given network.

    This controller is able to control either the voltage levels in a given network, or it can limit the line loading
    in a given network. In the case of voltage level limitation will this controler first try to adjust the tap position of the
    transformer. If the tap position is not enough to limit the voltage levels, then this controller will try to adjust the load
    and generation scaling factor. If the generartion is to high, then the load scaling factor is scaled up in each step by 10%
    with respekt to the previous step until the scaling factor reaches 1.0. After that the generation is scaled down in each step
    by 10% with respekt to the previous step. In the case of to much load and not enough generation the scaling factor for the loads is
    scaled down by 10% with respekt to the previous step and the generation scaling factor is not efected, because i assume that only
    pv and wind generators are connected in this mv-grid and those generators can not scale up thier generation. If the controller is
    used to limit the loading in the given grid are, then the procedure is as in the case of voltage limitation, but without the
    changing of the transformer tap position, because this has little to no effect on the line loading and could lead to a voltage violation.

    Parameters
    ----------
    net : pandapowerNet
        Whole network over which the time series calculation is run.
    element : ["voltage","line_loading"]
        The element of the results table the controller is suposed to control.
        "voltage" if the controller should control the voltage levels
        "line_loading" if the controller should controlle the line loading
    my_grid: MyGrid
        The subgrid with the indices of the busses, lines, loads, sgen, trafos and ext_grid of the whole grid that the controller is
        suposed to controlle the elements of the results table
    limits_pu: list[float]
        The limits that should not be violated in the subgrid. If the controller is used to control the line_loading, then one input is enough.
        The line loading limit is like the voltage limits given in per unit and should be between 0 and 1 to make the code simple.
        If the controller is used to control the voltage limits, then the minimum and maximum voltage should be given as arguments in a list.

    Returns
    -------
    None
    """

    def __init__(self, net, element, my_grid: MyGrid, limits_pu=(0.9, 1.1), in_service=True, order=0, level=0,
                 index=None, recycle=False, drop_same_existing_ctrl=False, initial_run=True, overwrite=False,
                 matching_params=None, **kwargs):
        super().__init__(net, in_service, order, level, index, recycle, drop_same_existing_ctrl, initial_run, overwrite,
                         matching_params, **kwargs)

        if element == "line_loading":
            self.max_limit = max(limits_pu) * 100.0
        else:
            self.max_limit = max(limits_pu)

        self.min_limit = min(limits_pu)
        self.element = element
        self.subgrid = my_grid
        self.pq_case = "p-"
        self.converged = False

    def is_converged(self, net):
        # check what element is to be checkt
        if self.element == "line_loading":
            self.check_line_loading(net)
        elif self.element == "voltage":
            self.check_bus_voltage(net)
        else:
            self.converged = True
        return self.converged

    def control_step(self, net):
        if self.element == "line_loading":
            self.control_line_loading(net)

        elif self.element == "voltage":
            self.control_bus_voltage(net)

    def check_line_loading(self, net):
        current_max_line_loading = net.res_line.loc[self.subgrid.get_indices("line"), "loading_percent"].max()
        if current_max_line_loading <= self.max_limit:
            self.converged = True
        else:
            self.converged = False

    def check_bus_voltage(self, net):
        max_vm_pu = net.res_bus.loc[self.subgrid.get_indices("bus"), "vm_pu"].max()
        min_vm_pu = net.res_bus.loc[self.subgrid.get_indices("bus"), "vm_pu"].min()
        if (self.min_limit <= min_vm_pu) and (max_vm_pu <= self.max_limit):
            self.converged = True
        else:
            self.converged = False

    def control_line_loading(self, net):
        self.determain_pq_case(net)
        if self.pq_case == "p+":
            # probbaly load problem in the grid
            net.load.loc[self.subgrid.get_indices("load"), "scaling"] *= 0.9

        elif self.pq_case == "p-":
            # probbaly generation problem in the grid
            current_scaling_load = net.load.loc[self.subgrid.get_indices("load"), "scaling"].max()

            if current_scaling_load < 1.0:
                net.load.loc[self.subgrid.get_indices("load"), "scaling"] *= 1.1
            else:
                net.load.loc[self.subgrid.get_indices("load"), "scaling"] = 1.0
                net.sgen.loc[self.subgrid.get_indices("sgen"), "scaling"] *= 0.9

        else:
            # probbaly generation/load problem in the grid
            net.sgen.loc[self.subgrid.get_indices("sgen"), "scaling"] *= 0.9
            net.load.loc[self.subgrid.get_indices("load"), "scaling"] *= 0.9

    def control_bus_voltage(self, net):
        max_vm_pu = net.res_bus.loc[self.subgrid.get_indices("bus"), "vm_pu"].max()
        min_vm_pu = net.res_bus.loc[self.subgrid.get_indices("bus"), "vm_pu"].min()
        min_tap_pos_trafo = net.trafo.loc[self.subgrid.get_indices("trafo"), "tap_min"].min()
        max_tap_pos_trafo = net.trafo.loc[self.subgrid.get_indices("trafo"), "tap_max"].max()
        current_tap_pos_trafo = net.trafo.loc[self.subgrid.get_indices("trafo"), "tap_pos"].max()
        if (min_tap_pos_trafo < current_tap_pos_trafo) and (current_tap_pos_trafo < max_tap_pos_trafo):
            if (min_vm_pu < self.min_limit):
                net.trafo.loc[self.subgrid.get_indices("trafo"), "tap_pos"] -= 1
            elif (max_vm_pu > self.max_limit):
                net.trafo.loc[self.subgrid.get_indices("trafo"), "tap_pos"] += 1
        else:
            self.control_line_loading(net)

    def determain_pq_case(self, net):

        sum_p_busses = net.res_ext_grid.loc[self.subgrid.get_indices("ext_grid"), "p_mw"].sum()
        sum_q_busses = net.res_ext_grid.loc[self.subgrid.get_indices("ext_grid"), "q_mvar"].sum()

        # check if the active power is grater than the reactive power
        if abs(sum_p_busses) > abs(sum_q_busses):
            # the active power is grater than the reactive power
            if sum_p_busses >= 0.0:
                # positiv active power points to the load as the problem
                self.pq_case = "p+"
            else:
                # negativ active power points to the generation as the problem
                self.pq_case = "p-"
        else:
            # the reactive power is grater than the active power
            if sum_q_busses >= 0.0:
                # positive reactive power points to inductive problem
                self.pq_case = "q+"
            else:
                # negative reactive power points to capacitiv problem
                self.pq_case = "q-"
data = pd.read_csv("/Users/lukaskramer/Documents/Uni/Mastersemester1/Pandapower/Unterlagen/Exam_Files/timeseries_exercise_4.csv", sep=";")
ds = DFData(data)
def timeseries_area2(output_dir):
    net = net_exam()
    n_timesteps = len(data.sgens)
    ds = create_data_source(n_timesteps)
    net = create_controllers(net, ds)
    time_steps = range(0, n_timesteps)
    TapController(net, tid=tid)
    my_grid = MyGrid(net, bus_indices=my_busses_indices, line_indices=my_lines_indices, load_indices=my_loads_indices,
                     sgen_indices=my_sgen_indices, ext_grid_indices=my_area, trafo_indices=my_trafo_indices)
    W_Controller(net, element="line_loading", my_grid=my_grid, limits_pu=[0, 1])
    create_output_writer(net, time_steps, output_dir)
    run_timeseries(net, time_steps)

def net_exam():
    net = pp.from_json(
        "/Users/lukaskramer/Documents/Uni/Mastersemester1/Pandapower/Unterlagen/Exam_Files/net_exercise_4.json")
    global mg
    mg = top.create_nxgraph(net)
    # Zählt alle Knoten auf, die mit Bus 0, 45, 89 und 134 verbunden sind
    global buses_area2
    global buses_area3
    global tid
    buses_area2 = list(top.connected_component(mg, bus=45))
    buses_area3 = list(top.connected_component(mg, bus=89))
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
    num_loads2 = net.load.bus.isin(buses_area2)
    num_sgen2 = net.sgen.bus.isin(buses_area2)
    loads2 = pd.DataFrame(net.load[num_loads2]).index
    sgens2 = pd.DataFrame(net.sgen[num_sgen2]).index
    ConstControl(net, element="load", variable="scaling", element_index=loads2,
                 data_source=ds, profile_name="loads")
    ConstControl(net, element="sgen", variable="scaling", element_index=sgens2,
                 data_source=ds, profile_name="sgens")
    num_loads3 = net.load.bus.isin(buses_area3)
    num_sgen3 = net.sgen.bus.isin(buses_area3)
    loads3 = pd.DataFrame(net.load[num_loads3]).index
    sgens3 = pd.DataFrame(net.sgen[num_sgen3]).index
    ConstControl(net, element="load", variable="scaling", element_index=loads3,
                 data_source=ds, profile_name="loads")
    ConstControl(net, element="sgen", variable="scaling", element_index=sgens3,
                 data_source=ds, profile_name="sgens")
    return net

def create_output_writer(net, time_steps, output_dir):
    ow = OutputWriter(net, time_steps, output_path=output_dir, output_file_type=".xlsx", log_variables=list())
    #Da hv_bus einen konstanten Spannungspegel von 1.00 hat, muss dieser ausgeschlossen werden. Dazu wird der Index des HV-Buses gesucht und mit .drop ausgeschossen
    mask_buses_area2_hv = net.bus.loc[buses_area2]
    mask_buses_area3_hv = net.bus.loc[buses_area3]
    hv_bus2 = mask_buses_area2_hv.loc[mask_buses_area2_hv["vn_kv"] == 110.0, "vn_kv"].index
    hv_bus3 = mask_buses_area3_hv.loc[mask_buses_area3_hv["vn_kv"]==110.0, "vn_kv"].index
    mask_buses_area2 = mask_buses_area2_hv.drop(hv_bus2).index
    mask_buses_area3 = mask_buses_area3_hv.drop(hv_bus3).index
    mask_lines_area2 = net.line[(net.line.from_bus.isin(buses_area2))&net.line.to_bus.isin(buses_area2)].index
    mask_lines_area3 = net.line[(net.line.from_bus.isin(buses_area3)) & net.line.to_bus.isin(buses_area3)].index

    #Ergebnisse in Excel schreiben
    ow.log_variable("res_line", "loading_percent", index=mask_lines_area2, eval_function=np.max, eval_name="Max. Leitungsauslastung Area 2")
    ow.log_variable("res_bus", "vm_pu", index=mask_buses_area2, eval_function=np.max, eval_name="Max. Spannungspegel Area 2")
    ow.log_variable("res_bus", "vm_pu", index=mask_buses_area2, eval_function=np.min, eval_name="Min. Spannungspegel Area 2")
    ow.log_variable("res_line", "loading_percent", index=mask_lines_area3, eval_function=np.max, eval_name="Max. Leitungsauslastung Area 3")
    ow.log_variable("res_bus", "vm_pu", index=mask_buses_area3, eval_function=np.max, eval_name="Max. Spannungspegel Area 3")
    ow.log_variable("res_bus", "vm_pu", index=mask_buses_area3, eval_function=np.min, eval_name="Min. Spannungspegel Area 3")


    return ow

output_dir = os.path.join(tempfile.gettempdir(), "time_series_area2")
print("Results can be found in your local temp folder: {}".format(output_dir))
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
timeseries_area2(output_dir)