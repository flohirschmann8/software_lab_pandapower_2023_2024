import pandapower as pp

class TapController(pp.control.basic_controller.Controller):
    def __init__(self, net, tid, in_service=True, order=0, level=0):
        super().__init__(net, in_service=in_service, order=order, level=level)
        self.tid = tid #trafo_index
        self.hv_bus = net.trafo.loc[tid, "hv_bus"]
        self.power = None
        self.tap_pos = None
        self.applied = False
    def initialize_control(self, net):
        self.power = net.res_ext_grid.loc[net.ext_grid.bus == self.hv_bus, "p_mw"].values[0]
        self.applied = False
    def is_converged(self, net):
        return self.applied
    def write_to_net(self, net):
        net.trafo.loc[self.tid, "tap_pos"] = self.tap_pos
    def control_step(self, net):
        if self.power >= 12:
            self.tap_pos = -3
        elif self.power >= 8:
            self.tap_pos = -2
        elif self.power >= 4:
            self.tap_pos = -1
        elif self.power >= 0:
            self.tap_pos = 0
        elif self.power >= -4:
            self.tap_pos = 1
        elif self.power >= -8:
            self.tap_pos = 2
        elif self.power <= -8:
            self.tap_pos = 3
        self.write_to_net(net)
        self.applied = True
