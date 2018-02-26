import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

volume_list = [1.5, 2.05, 2.5, 2.5, 0.75, 0.725, 0.75]
pressure_list = [33.25, 32.25, 30.25, 32.0, 43.0, 34.5, 33.5]
pressure_err = [0.25]*7
volume_err = [0.0125]*7

plt.figure(figsize=(8, 6), dpi=80)
plt1 = plt.subplot(1, 1, 1)
plt.grid(True)

plt.errorbar(volume_list, pressure_list, pressure_err, volume_err)

plt.text(1.475, 33.0, r'a', verticalalignment='top', horizontalalignment='right')
plt.text(2.075, 32.5, r'b', verticalalignment='bottom', horizontalalignment='left')
plt.text(2.53, 30.25, r'c', verticalalignment='bottom', horizontalalignment='left')
plt.text(2.53, 32.0, r'd', verticalalignment='bottom', horizontalalignment='left')
plt.text(0.72, 43.0, r'e', verticalalignment='center', horizontalalignment='right')
plt.text(0.69, 34.5, r'f', verticalalignment='center', horizontalalignment='right')
plt.text(0.72, 33.5, r'g', verticalalignment='top', horizontalalignment='right')




plt.xlabel(r'Volume [ml]')
plt.ylabel(r'Pressure [bar]')
plt.suptitle(r'p-V-Diagramm', fontsize=15, fontweight='bold')

plt.show()