from pandapower.control.basic_controller import Controller
import pandapower.topology as top
import pandapower.toolbox as tool


class KLController(Controller):
    def __init__(self, net, max_limit_pu, min_limit_pu, in_service=True,  order=0, level=0):
        super().__init__(net, in_service=in_service, order=order, level=level)
        self.mg = top.create_nxgraph(net)
        self.id_buses_area3 = list(top.connected_component(self.mg, bus=89))
        self.id_trafo_area3 = list(tool.get_connected_elements(net=net, element_type="trafo", buses=self.id_buses_area3))
        self.min_limit_pu = min_limit_pu
        self.max_limit_pu = max_limit_pu
        self.min_tap_pos = net.trafo.loc[self.id_trafo_area3, "tap_min"].min()
        self.max_tap_pos = net.trafo.loc[self.id_trafo_area3, "tap_max"].max()
        self.current_tap_pos = net.trafo.loc[self.id_trafo_area3, "tap_pos"].max()
        self.converged = False

    def is_converged(self, net):
        #min. und max. Spannungspegel innerhalb der Spannungsgrenzen?
        max_vm_pu = net.res_bus.loc[self.id_buses_area3, "vm_pu"].max()
        min_vm_pu = net.res_bus.loc[self.id_buses_area3, "vm_pu"].min()
        if (self.min_limit_pu <= min_vm_pu) and (max_vm_pu <= self.max_limit_pu):
            self.converged = True
        else:
            self.converged = False

        return self.converged

    def control_step(self, net):
        #tap_pos erhöhen, wenn max. Spannungspegel > maxSpannungsgrenze, tap_pos erniedrigen, wenn min.Spannungspegel < min. Spannungsgrenze
        #tap_pos kann nur bis -9 erniedrigt und bis 9 erhöht werden
        max_vm_pu = net.res_bus.loc[self.id_buses_area3, "vm_pu"].max()
        min_vm_pu = net.res_bus.loc[self.id_buses_area3, "vm_pu"].min()
        self.current_tap_pos = net.trafo.loc[self.id_trafo_area3, "tap_pos"].max()
        if (min_vm_pu < self.min_limit_pu) and (self.current_tap_pos > self.min_tap_pos):
            net.trafo.loc[self.id_trafo_area3, "tap_pos"] -= 1
        elif (max_vm_pu > self.max_limit_pu) and (self.current_tap_pos < self.max_tap_pos):
            net.trafo.loc[self.id_trafo_area3, "tap_pos"] += 1




