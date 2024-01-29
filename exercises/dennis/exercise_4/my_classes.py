import pandapower.topology as top
import pandapower.toolbox as tool
from pandapower.control.basic_controller import Controller

class MyGrid():
    """
    Create a MyGrid object, that holds the indices and elements, that belong to a subgrid of the whole grid.

    This class is used to store the bus, line, load, sgen, trafo and ext_grid indices and elements that are specific to the selectet subgrid.
    
    Parameters
    ----------
    whole_net : pandapowerNet
        Whole network of which the subgrid is a part of.
    ext_grid_subgrid : int
        The index of the external grid that defines the subgrid.

    Returns
    -------
    MyGrid
        The MyGrid object that was created.
    """

    def __init__(self, whole_net, ext_grid_subgrid) -> None:
        
        # create a network graph with the whole network
        net_graph = top.create_nxgraph(net=whole_net)
        # to get a pandas dataframe as a return value the int ext_grid_subgrid has to be passed as a list to the .loc function
        self.my_ext_grids = whole_net.ext_grid.loc[[ext_grid_subgrid],:]
        # to extract the indices of the connectet in a list format components it is nessesary to convert the result of the topology function
        # to extract the int value of the bus to start the grid search it is nessesary to extract the values of the pandas dataframe and 
        # out of the array of vaules the first value is the int index of the bus that the external grid is connected to
        ext_grid_bus = self.my_ext_grids["bus"].values[0]

        indices_busses = list(top.connected_component(mg=net_graph,bus=ext_grid_bus))
        self.my_busses = whole_net.bus.loc[indices_busses,:]

        indecies_lines = list(tool.get_connected_elements(net=whole_net,element_type="line",buses=indices_busses))
        self.my_lines = whole_net.line.loc[indecies_lines,:]

        indices_loads = list(tool.get_connected_elements(net=whole_net,element_type="load",buses=indices_busses))
        self.my_loads = whole_net.load.loc[indices_loads,:]

        indices_sgen = list(tool.get_connected_elements(net=whole_net,element_type="sgen",buses=indices_busses))
        self.my_sgens = whole_net.sgen.loc[indices_sgen,:]

        indices_trafo = list(tool.get_connected_elements(net=whole_net,element_type="trafo",buses=indices_busses))
        self.my_trafos = whole_net.trafo.loc[indices_trafo,:]        

    
    def get_indices(self,element):
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

    def get_elements(self,element):
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
    def __init__(self, net, element, my_grid:MyGrid, limits_pu=[0.9,1.1], in_service=True, order=0, level=0, index=None, recycle=False, drop_same_existing_ctrl=False, initial_run=True, overwrite=False, matching_params=None, **kwargs):
        super().__init__(net, in_service, order, level, index, recycle, drop_same_existing_ctrl, initial_run, overwrite, matching_params, **kwargs)

        if element == "line_loading":
            self.max_limit = max(limits_pu)*100.0
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


    def check_line_loading(self,net):
        current_max_line_loading = net.res_line.loc[self.subgrid.get_indices("line"),"loading_percent"].max()
        if current_max_line_loading <= self.max_limit:
            self.converged = True
        else:
            self.converged = False
        
    def check_bus_voltage(self,net):
        max_vm_pu = net.res_bus.loc[self.subgrid.get_indices("bus"),"vm_pu"].max()
        min_vm_pu = net.res_bus.loc[self.subgrid.get_indices("bus"),"vm_pu"].min()
        if (self.min_limit <= min_vm_pu) and (max_vm_pu <= self.max_limit):
            self.converged = True
        else:
            self.converged = False

    def control_line_loading(self,net):
        self.determain_pq_case(net)
        if self.pq_case == "p+":
            # probbaly load problem in the grid
            # in every control step decrease the load power by 90% of its previous value
            net.load.loc[self.subgrid.get_indices("load"),"scaling"] *= 0.9            
            
        elif self.pq_case == "p-":
            # probbaly generation problem in the grid
            # get the highest load scaling factor to see, if the load can be increased to decrease the infeed of all generators in the subgrid
            current_scaling_load = net.load.loc[self.subgrid.get_indices("load"),"scaling"].max()

            if (current_scaling_load * 1.1) < 1.0:
                # increase the load scaling factor by 10% in each control step with respect to its last value
                net.load.loc[self.subgrid.get_indices("load"),"scaling"] *= 1.1
            else:
                # if the load scaling factor is at its peack, then in every control step decrease the load power by 90% of its previous value
                net.load.loc[self.subgrid.get_indices("load"),"scaling"] = 1.0
                net.sgen.loc[self.subgrid.get_indices("sgen"),"scaling"] *= 0.9            
        
        else:
            # the Problem is one of reactive power and is not easy to solve.
            # the simplest solution is to decrease the load and generation at the same time
            # in every control step decrease the load/generation power by 90% of its previous value
            net.sgen.loc[self.subgrid.get_indices("sgen"),"scaling"] *= 0.9
            net.load.loc[self.subgrid.get_indices("load"),"scaling"] *= 0.9

       
    def control_bus_voltage(self,net):
        # get the max and min value for the bus voltages in the subgrid
        max_vm_pu = net.res_bus.loc[self.subgrid.get_indices("bus"),"vm_pu"].max()
        min_vm_pu = net.res_bus.loc[self.subgrid.get_indices("bus"),"vm_pu"].min()

        # get the max/min and current tap positions of the connected transformer
        min_tap_pos_trafo = net.trafo.loc[self.subgrid.get_indices("trafo"),"tap_min"].min()
        max_tap_pos_trafo = net.trafo.loc[self.subgrid.get_indices("trafo"),"tap_max"].max()
        current_tap_pos_trafo = net.trafo.loc[self.subgrid.get_indices("trafo"),"tap_pos"].max()

        if (min_tap_pos_trafo < current_tap_pos_trafo) and (current_tap_pos_trafo < max_tap_pos_trafo):
            # if the tap position can be changed, then check, if it has to be increased or decreased
            if (min_vm_pu < self.min_limit):
                # the minimum voltage of on bus is to low and so the tapposition has to be decreased in order to increase the secondary voltage
                net.trafo.loc[self.subgrid.get_indices("trafo"),"tap_pos"] -= 1
            elif (max_vm_pu > self.max_limit):
                # the maximum voltage of on bus is to high and so the tapposition has to be increased in order to decrease the secondary voltage
                net.trafo.loc[self.subgrid.get_indices("trafo"),"tap_pos"] += 1
        else:
            # if the tap position is at its maximum or minimum position, then the loadings of loads or generators have to be adjusted
            self.control_line_loading(net)

    def determain_pq_case(self,net):

        sum_p_busses = net.res_ext_grid.loc[self.subgrid.get_indices("ext_grid"),"p_mw"].sum()
        sum_q_busses = net.res_ext_grid.loc[self.subgrid.get_indices("ext_grid"),"q_mvar"].sum()

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