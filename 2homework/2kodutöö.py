import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

thrust = 0.00
brake = 0.00
a = 0.0 #kiirendus
v = 0.0 #kiirus
distants = 0.0
max_time = 120
kiiruste_list = [0]
error = 0.1
dt = 0.1
kiiruse_piirang = [25]
distantsi_list = [0]


def kiirendus(thrust, brake):
    return (3 * thrust) - (5 * brake) - 0.1

def on_off_kontroller(thrust, brake, piirang, v, distants, dt):
    kiiruste_list.append(v * 3.6)
    a = kiirendus(thrust, brake) * dt
    v += a
    distants += v * dt
    kiiruse_piirang.append(piirang * 3.6)
    distantsi_list.append(distants)
    return v, distants

for i in range(int(max_time/dt)):
    if distants < 200:
        piirang = 25/3.6
        if v < 25/3.6 - error:
            v, distants = on_off_kontroller(1, 0, piirang, v, distants, dt)
        elif v > 25/3.6 + error:
            v, distants = on_off_kontroller(0, 1, piirang, v, distants, dt)
        else:
            v, distants = on_off_kontroller(1/30, 0, piirang, v, distants, dt)
    elif 200 <= distants < 300:
        piirang = 10/3.6
        if v < 10/3.6 - error:
            v, distants = on_off_kontroller(1, 0, piirang, v, distants, dt)
        elif v > 10/3.6 + error:
            v, distants = on_off_kontroller(0, 1, piirang, v, distants, dt)
        else:
            v, distants = on_off_kontroller(1/30, 0, piirang, v, distants, dt)
    elif 300 <= distants < 500:
        piirang = 30/3.6
        if v < 30/3.6 - error:
            v, distants = on_off_kontroller(1, 0, piirang, v, distants, dt)
        elif v > 30/3.6 + error:
            v, distants = on_off_kontroller(0, 1, piirang, v, distants, dt)
        else:
            v, distants = on_off_kontroller(1/30, 0, piirang, v, distants, dt)
    elif distants >= 500:
        piirang = 0
        if v > 0:
            v, distants = on_off_kontroller(0, 1, piirang, v, distants, dt)
        elif v <= 0:
            v, distants = on_off_kontroller(0, 0, piirang, 0, distants, dt)
        else:
            v, distants = on_off_kontroller(1/30, 0, piirang, v, distants, dt)
    else: #on kiiruse hoidmiseks
        v, distants = on_off_kontroller(1/30, 0, piirang, v, distants, dt)

aegade_list = np.round(np.arange(0, max_time + 0.1, 0.1), 2)
distantsi_list = np.round(distantsi_list, 2)
kiiruste_list = np.round(kiiruste_list, 2)
kiiruse_piirang = np.round(kiiruse_piirang, 1)

#kirjutan andmed CSVsse
andmed = pd.DataFrame({'aeg [s]': aegade_list, ' asukoht [m]': distantsi_list, ' kiirus [km/h]': kiiruste_list, ' kiirusepiirang [km/h]': kiiruse_piirang}).to_csv("andmed.csv", sep = "\t", index = False)

plt.plot(kiiruste_list)
plt.show(block=True)