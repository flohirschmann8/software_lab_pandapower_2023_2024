import pandapower as pp

class TapController(pp.control.basic_controller.Controller):
    def __init__(self, net, tid, in_service=True, order=0, level=0):
        """
        Funktion übernimmt Trafo-ID (tid) und sucht nach dem Knoten, welcher mit der HV-Seite dieses Trafos verbunden ist.
        self.power, self.tap_pos und self.applied werden initialisiert
        Parameters
        ----------
        net
        tid
        in_service
        order
        level
        """
        super().__init__(net, in_service=in_service, order=order, level=level)
        self.tid = tid #trafo_index
        self.hv_bus = net.trafo.loc[self.tid, "hv_bus"]
        self.power = None
        self.tap_pos = None
        self.applied = False
    def initialize_control(self, net):
        """
        Aus der Lastflussberechnung wird die Wirkleistung, die über den Trafo fließt (Ermittlung über Slack) in self.power gespeichert.
        self.applied wird auf False gesetzt, um in jedem Zeitschritt in control_step zu gehen
        Parameters
        ----------
        net
        """
        self.power = net.res_ext_grid.loc[net.ext_grid.bus == self.hv_bus, "p_mw"].values[0]
        self.applied = False
    def is_converged(self, net):
        """
        Rückgabe von self.applied (wenn True --> Verlassen der Schleife, wenn False --> control_step)
        Parameters
        ----------
        net

        Returns
        -------

        """
        return self.applied
    def write_to_net(self, net):
        """
        Schreibt die Stufenstellung, die in control_step ermittelt wurde, in net.
        Parameters
        ----------
        net
        """
        net.trafo.loc[self.tid, "tap_pos"] = self.tap_pos
    def control_step(self, net):
        """
        Steuert die Stufenschaltung des HS/MS Transformators und ruft write_to_net auf.
        Zudem wird self.applied auf True gesetzt, um die Regelschleife (über is_converged) zu verlassen.
        Parameters
        ----------
        net

        """
        if self.power > 12:
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
        elif self.power < -8:
            self.tap_pos = 3
        self.write_to_net(net)
        self.applied = True