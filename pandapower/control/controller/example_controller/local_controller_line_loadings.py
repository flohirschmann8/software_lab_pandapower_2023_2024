from pandapower.control.basic_controller import Controller


class LocalBusVoltageController(Controller):
    
    def __init__(self, net, line_index, max_line_loading, in_service=True, order=0, level=0):
        super().__init__(net, in_service=in_service, order=order, level=level)
        self.line_index = line_index
        self.max_line_loading = max_line_loading
        self.buses = [net.line.loc[line_index, "from_bus"], net.line.loc[line_index, "to_bus"]]
    
    def initialize_control(self, net):
        net.sgen.loc[net.sgen["bus"].isin(self.buses), "in_service"] = True
    
    def is_converged(self, net):
        if net.res_line.loc[self.line_index, "loading_percent"] > self.max_line_loading:
            return False
        else:
            return True
    
    def control_step(self, net):
        net.sgen.loc[net.sgen["bus"].isin(self.buses), "in_service"] = False
