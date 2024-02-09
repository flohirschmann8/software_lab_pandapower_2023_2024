import pandapower as pp
import pandas as pd
import pandapower.plotting as plot
import matplotlib.pyplot as plt

#import net "oberrhein"
net = pp.networks.mv_oberrhein(scenario="generation")

df_line = pd.DataFrame(net.line)

#increase p_mw
net.sgen.loc[:, "p_mw"] *= 3.4

#powerflowcalculation
pp.runpp(net)

#identify overloaded lines
df_line["loading_percent"] = net.res_line.loading_percent
overloaded_lines = df_line[df_line["loading_percent"] > 100]

#print(overloaded_lines)
available_df= pp.available_std_types(net, "line")

for _, row in overloaded_lines.iterrows():
    for j in available_df.index:
        df_line["loading_percent_new"] = net.res_line.loading_percent
        if df_line.at[row.name, "loading_percent_new"] < 100:
            break
        if str(j).endswith("12/20 kV") or str(j).endswith("20.0"):
            pp.change_std_type(net, row.name, j, element="line")
            pp.runpp(net)
        else:
            continue

#colouring lines
cmap_list_b=[(0, "green"), (100, "yellow"), (101, "red")]
cmap, norm = plot.cmap_continuous(cmap_list_b)
lc = plot.create_line_collection(net, net.line.index, zorder=1, cmap=cmap, norm=norm, linewidths=2)

#colouring busses
cmap_list_b=[(0.975, "blue"), (1.0, "green"), (1.05, "red")]
cmap, norm = plot.cmap_continuous(cmap_list_b)
bc = plot.create_bus_collection(net, net.bus.index, size=80, zorder=2, cmap=cmap, norm=norm)

#plotting
plot.draw_collections([lc, bc], figsize=(8,6))
plt.show()

pp.runpp(net)
df_line["loading_percent"] = net.res_line.loading_percent
overloaded_lines2 = df_line[df_line["loading_percent"] > 100]
if overloaded_lines2.empty:
    print("Keine überlasteten Leitungen")
else:
    print(f"Bei den überlasteten Leitungen handelt es sich um", overloaded_lines2)
