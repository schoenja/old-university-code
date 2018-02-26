import matplotlib.pyplot as plt
import scipy.optimize
import numpy as np


# Kalibrierung
kal_ampere = [0.57, 0.99, 1.45, 2.13, 2.54, 3.06, 3.45, 4.00, 4.53, 5.12, 5.60, 6.02, 6.46,
              7.04, 7.53, 8.09, 8.48, 9.01, 9.57]
kal_tesla = [71, 136, 195, 293, 348, 415, 459, 501, 537, 567, 584, 596, 607, 619, 628,
             638, 644, 653, 661]
kal_ampere_err = list(map(lambda x: 0.015*x, kal_ampere))
kal_tesla_err = [0.5]*len(kal_tesla)

plt.figure(figsize=(8, 6), dpi=80)
plt1 = plt.subplot(1, 1, 1)
plt.grid(True)

plt.errorbar(kal_ampere, kal_tesla, kal_ampere_err, kal_tesla_err, ecolor='black', fmt='o', label='Messwerte')


def fit_func(x, a, b, c):
    return a * (1 - np.exp(b*x))+c


p, p_co = scipy.optimize.curve_fit(fit_func, np.array(kal_ampere), np.array(kal_tesla),
                                   bounds=([0, -np.inf, -np.inf], [np.inf, 0, 0]))
p_err = np.sqrt(np.diag(p_co))

kal_fit = np.zeros(len(kal_tesla))
for i in range(len(kal_ampere)):
    kal_fit[i] = fit_func(kal_ampere[i], p[0], p[1], p[2])


plt.plot(kal_ampere, kal_fit, color='orange', label='Fit')

plt.suptitle(r'Kalibrierung', fontsize=14, fontweight='bold')
plt.xlabel(r'Stromstärke [A]')
plt.ylabel(r'Magnetfeldstärke [mT]')

plt.text(7, 500,
         "y=a*(1-exp(b*x))+c\na=780±11\nb=-0.334±0.015\nc=-84±14",
         horizontalalignment='left', verticalalignment='top',
         bbox={'facecolor': 'white', 'alpha': 1.0, 'pad': 10})

plt.legend(loc='lower right')
print(p, p_err)

plt.show()
