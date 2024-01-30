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
        """
Diese Funktion prüft die Wirkleistung, welche durch das ext.grid bereitgestellt wird bzw. zurückgespeist wird.
Zudem wird self.applied auf False gesetzt, damit der Control_Step ausgeführt wird.
        Parameters
        ----------
        net:
            Das Netz, welches berechnet werden soll.
        """
        self.power = net.res_ext_grid.loc[net.ext_grid.bus == self.hv_bus, "p_mw"].values[0]
        self.applied = False
    def is_converged(self, net):
        """
Bestimmung, ob control_step ausgeführt wird oder nicht anhand von applied.
        Parameters
        ----------
        net:
            Das Netz, welches berechnet werden soll.
        Returns
        -------
        True --> control_step wird durchlaufen
        False --> control_step wird nicht durchlaufen, Control-Loop wird abgeschlossen
        """
        return self.applied
    def write_to_net(self, net):
        """
Diese Funktion schreibt die Stufenstellung des Trafos, welche im Control-Step für die jeweilige Wirkleistung hinterlegt wird, in
den Trafo in net.
        Parameters
        ----------
        net:
            Das Netz, welches berechnet werden soll.
        """
        net.trafo.loc[self.tid, "tap_pos"] = self.tap_pos
    def control_step(self, net):
        """
In dieser Funktion sind die Stufenstellungen des HS/MS Trafos abhängig von der vorherrschenden Wirkleistung hinterlegt.
Darüber hinaus wird in der Funktion write_to_net aufgerufen, um die tap_pos in net zu schreien.
Self.applied wird auf true gesetzt, um den Control Step zu verlassen.
        Parameters
        ----------
        net:
            Das Netz, welches berechnet werden soll.
        """
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
