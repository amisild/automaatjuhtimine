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
kiiruse_piirang = []
distantsi_list = []


def kiirendus(thrust, brake):
    return (3 * thrust) - (5 * brake) - 0.1

for i in range(int(max_time/dt)):
    if distants < 200:
        piirang = 25 / 3.6
        if v < 25/3.6 - error:
            kiiruste_list.append(v)
            thrust = 1
            brake = 0
            a = kiirendus(thrust, brake) * dt
            v += a
            distants += v * dt
            kiiruse_piirang.append(piirang)
            distantsi_list.append(distants)
        elif v > 25/3.6 + error:
            kiiruste_list.append(v)
            thrust = 0
            brake = 1
            a = kiirendus(thrust, brake) * dt
            v += a
            distants += v * dt
            kiiruse_piirang.append(piirang)
            distantsi_list.append(distants)
        else:
            kiiruste_list.append(v)
            thrust = 1 / 30
            brake = 0
            a = kiirendus(thrust, brake) * dt
            v += a
            distants += v * dt
            kiiruse_piirang.append(piirang)
            distantsi_list.append(distants)
    elif 200 <= distants < 300:
        piirang = 10/3.6
        if v < 10/3.6 - error:
            kiiruste_list.append(v)
            thrust = 1
            brake = 0
            a = kiirendus(thrust, brake) * dt
            v += a
            distants += v * dt
            kiiruse_piirang.append(piirang)
            distantsi_list.append(distants)
        elif v > 10/3.6 + error:
            kiiruste_list.append(v)
            thrust = 0
            brake = 1
            a = kiirendus(thrust, brake) * dt
            v += a
            distants += v * dt
            kiiruse_piirang.append(piirang)
            distantsi_list.append(distants)
        else:
            kiiruste_list.append(v)
            thrust = 1 / 30
            brake = 0
            a = kiirendus(thrust, brake) * dt
            v += a
            distants += v * dt
            kiiruse_piirang.append(piirang)
            distantsi_list.append(distants)
    elif 300 <= distants < 500:
        piirang = 30/3.6
        if v < 30/3.6 - error:
            kiiruste_list.append(v)
            thrust = 1
            brake = 0
            a = kiirendus(thrust, brake) * dt
            v += a
            distants += v * dt
            kiiruse_piirang.append(piirang)
            distantsi_list.append(distants)
        elif v > 30/3.6 + error:
            kiiruste_list.append(v)
            thrust = 0
            brake = 1
            a = kiirendus(thrust, brake) * dt
            v += a
            distants += v * dt
            kiiruse_piirang.append(piirang)
            distantsi_list.append(distants)
        else:
            kiiruste_list.append(v)
            thrust = 1 / 30
            brake = 0
            a = kiirendus(thrust, brake) * dt
            v += a
            distants += v * dt
            kiiruse_piirang.append(piirang)
            distantsi_list.append(distants)
    elif distants >= 500:
        piirang = 0
        if v > 0:
            kiiruste_list.append(v)
            thrust = 0
            brake = 1
            a = kiirendus(thrust, brake) * dt
            v += a
            distants += v * dt
            kiiruse_piirang.append(piirang)
            distantsi_list.append(distants)
        elif v < 0:
            v = 0
            distants += v * dt
            kiiruse_piirang.append(piirang)
            distantsi_list.append(distants)
        else:
            kiiruste_list.append(v)
            thrust = 1 / 30
            brake = 0
            a = kiirendus(thrust, brake) * dt
            v += a
            distants += v * dt
            kiiruse_piirang.append(piirang)
            distantsi_list.append(distants)
    else: #on kiiruse hoidmiseks
        kiiruste_list.append(v)
        thrust = 1/30
        brake = 0
        a = kiirendus(thrust, brake) * dt
        v += a
        distants += v * dt
        piirang = v
        kiiruse_piirang.append(piirang)
        distantsi_list.append(distants)

aegade_list = np.round(np.arange(0, int(max_time), 0.1), 2)
distantsi_list = np.round(distantsi_list, 2)
kiiruste_list = np.round(kiiruste_list, 2)
kiiruse_piirang = np.round(kiiruse_piirang, 2)

#kirjutan andmed CSVsse
andmed = pd.DataFrame({'aeg [s]': aegade_list, ' asukoht [m]': distantsi_list, ' kiirus [m/s]': kiiruste_list, ' kiiruse piirang [m/s]': kiiruse_piirang}).to_csv("d.csv", index = False)

plt.plot(kiiruste_list)
plt.show(block=True)
