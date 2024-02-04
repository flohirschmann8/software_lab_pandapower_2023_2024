import numpy as np
import pandapower.networks as nw

from function_exercise3 import apply_best_measures, determine_grid_capacity

np.random.seed(0)


# ========== TASK 2 ==========

net = nw.mv_oberrhein(scenario="generation")
results = determine_grid_capacity(net, iterations=15)
print(f"The average grid capacity without grid expansion measures is "
      f"{results['installed_mw'].mean():.2f} MW.")


# ========== TASK 3 ==========
'''
net, costs, measures = apply_best_measures(net, budget=3300000, iterations=10,
                                           grid_capacity_iterations=15)
results = determine_grid_capacity(net, iterations=15)
print(f"The average grid capacity after grid expansion measures is "
      f"{results['installed_mw'].mean():.2f} MW.")

'''

