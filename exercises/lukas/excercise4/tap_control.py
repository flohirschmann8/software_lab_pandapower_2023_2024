import os
import numpy as np
import pandas as pd
import tempfile
import pandapower as pp
import pandapower.topology as top
from pandapower.control import Characteristic, ConstControl
from pandapower.control.basic_controller import Controller
from pandapower.timeseries import DFData
from pandapower.timeseries import OutputWriter
from pandapower.timeseries.run_time_series import run_timeseries
import matplotlib.pyplot as plt

data = pd.read_csv("/Users/lukaskramer/Documents/Uni/Mastersemester1/Pandapower/Unterlagen/Exam_Files/timeseries_exercise_4.csv", sep=";")
ds = DFData(data)

def simple_test_net():
    net = pp.from_json(
        "/Users/lukaskramer/Documents/Uni/Mastersemester1/Pandapower/Unterlagen/Exam_Files/net_exercise_4.json")
    mg = top.create_nxgraph(net)
    # Zählt alle Knoten auf, die mit Bus 0, 45, 89 und 134 verbunden sind
    global buses_area2
    buses_area1 = list(top.connected_component(mg, bus=0))
    buses_area2 = list(top.connected_component(mg, bus=45))
    buses_area3 = list(top.connected_component(mg, bus=89))
    buses_area4 = list(top.connected_component(mg, bus=134))
    return net
net = simple_test_net()
pp.runpp(net)

class TapController(Controller):
    def __init__(self, net, tid, data_source=None, in_service=True,
                 recycle=False, order=0, level=0, **kwargs):
        super().__init__(net, in_service=in_service, recycle=recycle, order=order, level=level,
                    initial_powerflow = True, **kwargs)

        self.tid = tid
        self.bus = net.trafo.at[tid, "hv_bus"]
        for i in net.ext_grid.bus.index:
            if net.ext_grid.bus.loc[i] == net.trafo.at[3, "hv_bus"]:
                tmp = i
        self.power = net.res_ext_grid.at[tmp, "p_mw"]
        self.tap_pos = net.trafo.at[tid, "tap_pos"]
        self.applied = False

        # profile attributes
        self.data_source = data_source
        self.last_time_step = None

        def get_tap_pos(self):
            return self.tap_pos

        def is_converged(self, net):
            return self.applied

        def write_to_net(self, net):
            net.tap_pos.at[self.tid, "tap_pos"] = self.tap_pos

        def control_step(self, net):
            self.write_to_net(net)
            self.applied = True

        def time_step(self, net, time):
            if self.last_time_step is not None:
                if self.p_mw >=10:
                    self.tap_pos == 5
                if self.p_mw >=8:
                    self.tap_pos == 4
                if self.p_mw >=6:
                    self.tap_pos == 3
                if self.p_mw >=4:
                    self.tap_pos == 2
                if self.p_mw >=2:
                    self.tap_pos == 1
                if self.p_mw <=-2:
                    self.tap_pos == -1
                if self.p_mw <=-4:
                    self.tap_pos == -2
                if self.p_mw <=-6:
                    self.tap_pos == -3
                if self.p_mw <=-8:
                    self.tap_pos == -4
                if self.p_mw <=-10:
                    self.tap_pos == -5
                self.last_time_step = time
            if self.data_source:
                self.p_mw = self.data_source.get_time_step_value(time_step=time)
            self.applied = False