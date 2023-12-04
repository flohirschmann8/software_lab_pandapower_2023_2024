import pandapower as pp
import pandapower.networks as nw

# load the network
mv_oberrhein = nw.mv_oberrhein(scenario="generation")

# scaling factors before update
scaling_before = mv_oberrhein.sgen["p_mw"]
print(mv_oberrhein.sgen.loc[0:5,["p_mw","q_mvar"]])

# updating the real power to increse the real power by a factor of 3.4

mv_oberrhein.sgen.loc[:,"p_mw"] = mv_oberrhein.sgen.loc[:,"p_mw"] * 3.4
print(mv_oberrhein.sgen.loc[0:5,["p_mw","q_mvar"]])