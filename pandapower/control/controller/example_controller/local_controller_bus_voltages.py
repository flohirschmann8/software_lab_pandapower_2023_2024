from pandapower.control.basic_controller import Controller


class LocalBusVoltageController(Controller):
    
    def __init__(self, net, bus_index, max_vm_pu, in_service=True, order=0, level=0):
        super().__init__(net, in_service=in_service, order=order, level=level)
        self.bus_index = bus_index
        self.max_vm_pu = max_vm_pu
    
    def initialize_control(self, net):
        net.sgen.loc[net.sgen.bus == self.bus_index, "in_service"] = True
    
    def is_converged(self, net):
        if net.res_bus.loc[self.bus_index, "vm_pu"] > self.max_vm_pu:
            return False
        else:
            return True
    
    def control_step(self, net):
        net.sgen.loc[net.sgen.bus == self.bus_index, "in_service"] = False
