import pandapower as pp

class TapController(pp.control.basic_controller.Controller):
    def __init__(self, net, tid, data_source=None, p_profile=None, in_service=True,
                 recycle=False, order=0, level=0, **kwargs):
        super().__init__(net, in_service=in_service, recycle=recycle, order=order, level=level,
                    initial_powerflow = True, **kwargs)
        self.tid = tid #trafo_index
        self.bus = net.trafo.at[tid, "hv_bus"]
        self.power = net.res_ext_grid.at[tid, "p_mw"]
        self.tap_pos = net.trafo.at[tid, "tap_pos"]
        self.tap_min = net.trafo.at[tid, "tap_min"]
        self.tap_max = net.trafo.at[tid, "tap_max"]
        self.tap_step_percent = net.trafo.at[tid, "tap_step_percent"]
        self.applied = False

        # profile attributes
        self.data_source = data_source
        self.p_profile = p_profile
        self.last_time_step = None

    def get_tap_pos(self):
        return self.tap_pos

    def is_converged(self, net):
        return self.applied

    def write_to_net(self, net):
        net.trafo.at[self.tid, "tap_pos"] = self.tap_pos
        self.power = net.res_ext_grid.at[self.tid, "p_mw"]


    def control_step(self, net):
        self.write_to_net(net)
        self.applied = True

    def time_step(self, net, time):
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
            self.last_time_step = time

            if self.data_source:
                if self.p_profile is not None:
                    self.power = self.data_source.get_time_step_value(time_step=time, profile_name=self.p_profile)

            self.applied = False

