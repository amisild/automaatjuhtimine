#Tegin koostöös Margus Reintamiga
#Kõik töötab, v.a. simuleeritud kiiruse lõpp, kus koodi järgi peaks kiirendus minema miinustesse ehk sõiduk peaks hakkama tagurdama, mistõttu tekib ka erinevus originaalse ning simuleeritud kiiruse vahel

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

originaal_andmed = pd.read_csv("mõõtmised.csv")

#panen read nihkesse
kiirused_nihkes = pd.DataFrame(originaal_andmed[" speed [m/s]"].shift(periods=1, fill_value=0))

#leian kiiruse muutuse lahutades teisest väärtusest esimese
kiiruse_muutus = originaal_andmed.sub(kiirused_nihkes[' speed [m/s]'], 0).drop(['time [s]', ' thrust [%]', " brake [%]"], axis=1)

def kiiruse_muutuse_valem(X, c0, c1, c2):
    thrust, brake = X
    return c0 * thrust - c1 * brake - c2

sisendid = [originaal_andmed[" thrust [%]"], originaal_andmed[' brake [%]']]
tulemus = kiiruse_muutus[' speed [m/s]']

parameetrid, korrelatsioonimaatriks = curve_fit(kiiruse_muutuse_valem, sisendid, tulemus)

kiiruse_muutused = np.array(kiiruse_muutuse_valem((originaal_andmed[" thrust [%]"], originaal_andmed[' brake [%]']), parameetrid[0], parameetrid[1], parameetrid[2]))

#liidan kiiruse muutused kumulatiivselt et saada kiirused
kiirused = np.cumsum(kiiruse_muutused)

ajad = np.arange(0, 10.01, 0.01).tolist()

#kirjutan andmed CSVsse
simuleeritud_andmed = pd.DataFrame({'time [s]': ajad, ' speed [m/s]': kiirused}).to_csv("simulatsioon.csv", index = False)

plt.plot(ajad, kiirused) #simuleeritud
plt.plot(originaal_andmed['time [s]'], originaal_andmed[' speed [m/s]'])  #originaal
plt.legend(['simuleeritud speed m/s', 'originaal speed m/s'])
plt.show(block=True)
