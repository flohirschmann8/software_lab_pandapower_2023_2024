from pandapower.control.basic_controller import Controller


class CentralLineLoadingController(Controller):
    
    def __init__(self, net, lines, max_line_loading, in_service=True, order=0, level=0):
        super().__init__(net, in_service=in_service, order=order, level=level)
        self.lines = lines
        self.max_line_loading = max_line_loading
        from_buses = list(net.line.from_bus.loc[lines])
        to_buses = list(net.line.to_bus.loc[lines])
        self.buses = list(set(from_buses + to_buses))
        self.overloaded_lines = None
    
    def initialize_control(self, net):
        net.sgen.loc[net.sgen.bus.isin(self.buses), "in_service"] = True
    
    def is_converged(self, net):
        self.overloaded_lines = net.line.loc[(net.line.index.isin(self.lines)) 
                                             & (net.res_line["loading_percent"]
                                                > self.max_line_loading)].index
        if len(self.overloaded_lines) > 0:
            return False
        else:
            return True
    
    def control_step(self, net):
        net.sgen.loc[net.sgen.bus.isin(self.buses), "in_service"] = False
