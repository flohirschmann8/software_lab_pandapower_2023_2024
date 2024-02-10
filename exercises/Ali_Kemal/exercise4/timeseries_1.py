import pandas as pd
import pandapower as pp
import matplotlib.pyplot as plt


def run_ts(network, csv_path):
    # 2. Laden der CSV-Datei
    csv_file = csv_path
    df = pd.read_csv(csv_file, header=0, delimiter=";")

    # 3. Zeitreihenanalyse durchführen
    for index, row in df.iterrows():
        # Skalierung der Lasten und Generatoren
        load_scaling = row["loads"]
        sgen_scaling = row["sgens"]
    
        # Skalierung der Lasten
        for load in network.load.iterrows():
            network.load.at[load[0], 'p_mw'] *= load_scaling
    
        # Skalierung der Generatoren
        for gen in network.gen.iterrows():
            network.sgen.at[gen[0], 'p_mw'] *= sgen_scaling
    
        # 4. Simulation durchführen
        pp.runpp(network)

        # Ergebnisse sammeln
        load_total = network.res_load['p_mw'].sum()
        generation_total = network.res_sgen['p_mw'].sum()
    return load_total, generation_total
        # print(load_total)
        # print(generation_total)

        # results = results.append({'Time Step': row['Time Step'], 'Load': load_total, 'Generation': generation_total},
        #                         ignore_index=True)

    # Ergebnisse speichern
    #results.to_csv('ergebnisse.csv', index=False)
'''
    # Ergebnisse plotten
    plt.figure(figsize=(10, 6))
    plt.plot(results['Time Step'], results['Load'], label='Total Load')
    plt.plot(results['Time Step'], results['Generation'], label='Total Generation')
    plt.xlabel('Time Step')
    plt.ylabel('Power (kW)')
    plt.title('Total Load and Generation over Time')
    plt.legend()
    plt.grid(True)
    plt.show()
'''
