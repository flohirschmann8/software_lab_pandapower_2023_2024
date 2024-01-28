import numpy as np
import pandas as pd
import pandapower as pp
import pandapower.plotting as plot
import pandapower.topology as top

#Load network "net" from json file

net = pp.from_json("/Users/alikemalkoc/Library/Mobile Documents/com~apple~CloudDocs/Uni - Aktuelles Semester/01_Softwarepraktikum Pandapower/Übungen/exercise 4/Exam Files-20240128/net_exercise_4.json")

#Split network in 4 subnetworks


mg = top.create_nxgraph(net)
#Area 1
buses_area1 = list(top.connected_component(mg, bus=0))
#Area 2
buses_area2 = list(top.connected_component(mg, bus=45))
#Area 3
buses_area3 = list(top.connected_component(mg, bus=89))
#Area 4
buses_area4 = list(top.connected_component(mg, bus=134))
