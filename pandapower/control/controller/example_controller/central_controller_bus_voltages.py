from pandapower.control.basic_controller import Controller


class CentralBusVoltageController(Controller):
    
    def __init__(self, net, buses, max_vm_pu, in_service=True, order=0, level=0):
        super().__init__(net, in_service=in_service, order=order, level=level)
        self.buses = buses
        self.max_vm_pu = max_vm_pu
        self.overvoltage_buses = None
    
    def initialize_control(self, net):
        net.sgen.loc[net.sgen.bus.isin(self.buses), "in_service"] = True
    
    def is_converged(self, net):
        self.overvoltage_buses = net.bus.loc[(net.bus.index.isin(self.buses)) 
                                             & (net.res_bus["vm_pu"] > self.max_vm_pu)].index
        if len(self.overvoltage_buses) > 0:
            return False
        else:
            return True
    
    def control_step(self, net):
        net.sgen.loc[net.sgen.bus.isin(self.overvoltage_buses), "in_service"] = False
