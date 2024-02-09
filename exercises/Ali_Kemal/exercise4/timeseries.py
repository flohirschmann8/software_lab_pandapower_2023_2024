import csv
import matplotlib.pyplot as plt
import exercise


# Plotting maximum line-loading + maximum and minimum bus voltages
# Determine maximum line-loading
max_ll = 0
max_ll_index = 0
for x in range(0, len(exercise.net.res_line.loading_percent)):
    if exercise.net.res_line.loading_percent[x] > max_ll:
        max_ll = exercise.net.res_line.loading_percent[x]
        max_ll_index = x
        x += 1
    else:
        x += 1

print(max_ll)
print(max_ll_index)

# Determine maximum and minimum bus voltage
max_bv = 0
min_bv = 0
max_bv_index = 0
min_bv_index = 0

for x in range(0, len(exercise.net.res_bus.vm_pu)):
    if exercise.net.res_bus.vm_pu[x] > max_bv:
        max_bv = exercise.net.res_bus.vm_pu[x]
        max_bv_index = x
        x += 1
    else:
        x += 1

for x in range(0, len(exercise.net.res_bus.vm_pu)):
    if exercise.net.res_bus.vm_pu[x] > max_bv:
        max_bv = exercise.net.res_bus.vm_pu[x]
        max_bv_index = x
        x += 1
    else:
        x += 1

print("The maximum line-loading is at line ", max_ll_index, " with ", max_ll, " percent.")
print("The maximum bus-voltage is at bus ", max_bv_index, " with ", max_bv, " percent.")
print("The minimum bus-voltage is at bus ", min_bv_index, " with ", min_bv, " percent.")

# Plotting maximum line-loading + maximum and minimum bus voltage
t = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
a = [max_ll, max_ll, max_ll, max_ll,max_ll , max_ll, max_ll, max_ll, max_ll, max_ll]
b = [max_bv, max_bv, max_bv, max_bv,max_bv , max_bv, max_bv, max_bv, max_bv, max_bv]
c = [min_bv, min_bv, min_bv, min_bv,min_bv , min_bv, min_bv, min_bv, min_bv, min_bv]

plt.plot(t, a, label="Maximum line-loading")
plt.plot(t, b, label="Maximum bus-voltage")
plt.plot(t, c, label="Minimum bus-voltage")

plt.xlabel("Time")
plt.title("Maximum and minimum values")
plt.legend()
plt.grid(True)
plt.show()

'''

#Simulate time series

time = []
loads = []
sgens = []

# Open and read csv file
with open('timeseries_exercise_4.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=";")
    # Write rows time, loads, and sgens into lists
    for row in csv_reader:
        # Die Werte der aktuellen Zeile den entsprechenden Listen hinzufügen
        time.append(row[0])
        loads.append(row[1])
        sgens.append(row[2])


# Convert lists in datatype: float
x = 1
for x in range(1, (len(time)-1)):
    time[x] = float(time[x])
    loads[x] = float(loads[x])
    sgens[x] = float(sgens[x])
    x += 1

plt.plot(time, loads, label="loads")
plt.plot(time, sgens, label="sgens")

plt.legend()
#plt.show()

'''