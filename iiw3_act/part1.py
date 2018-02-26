import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

# volume_list_low = [4.0, 3.5, 3.0, 2.5, 2.0, 1.9, 1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.6]
# volume_list = [4.0, 3.5, 3.0, 2.5, 2.0, 1.9, 1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7]

# 21 degree C
volume_21_list = [4.0, 3.5, 3.0, 2.5, 2.0, 1.9, 1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.6, 0.575]
pressure_21_list = [20.0, 20.5, 20.5, 20.5, 20.75, 20.5, 20.5, 20.5, 20.5, 20.75, 20.75, 20.75, 20.75, 21.0, 21.0,
                    21.25, 21.25, 22, 27, 43.5]
volume_21_err = [0.0125] * len(volume_21_list)
pressure_21_err = [0.25] * len(pressure_21_list)

# 31 degree C
volume_31_list = [4.0, 3.5, 3.0, 2.5, 2.0, 1.9, 1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.625]
pressure_31_list = [21.5, 23.5, 25.5, 26.0, 26.0, 26.0, 26.0, 26.0, 26.0, 26.0, 26.0, 26.0, 26.0, 26.25, 26.5,
                    26.5, 26.75, 27, 36]
volume_31_err = [0.0125] * len(volume_31_list)
pressure_31_err = [0.25] * len(pressure_31_list)

# 41 degree C
volume_41_list = [4.0, 3.5, 3.0, 2.5, 2.0, 1.9, 1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8]
pressure_41_list = [23.0, 25.0, 27.5, 30.0, 32.35, 32.5, 32.5, 32.5, 32.75, 32.75, 32.75, 32.75, 32.75, 32.75, 32.75,
                    33.0, 37.0]
volume_41_err = [0.0125] * len(volume_41_list)
pressure_41_err = [0.25] * len(pressure_41_list)

# 46 degree C
volume_46_list = [4.0, 3.5, 3.0, 2.5, 2.0, 1.9, 1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7]
pressure_46_list = [23.75, 26.0, 28.5, 31.5, 34.25, 34.5, 35.0, 35.5, 36.0, 36.25, 36.25, 36.25, 36.5, 36.5, 36.5,
                    36.5, 37.5, 47]
volume_46_err = [0.0125] * len(volume_46_list)
pressure_46_err = [0.25] * len(pressure_46_list)

# 51 degree C
volume_51_list = [4.0, 3.5, 3.0, 2.5, 2.0, 1.9, 1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8]
pressure_51_list = [24.5, 27.0, 29.75, 32.75, 36.0, 36.75, 37.25, 38.0, 38.5, 39.0, 39.5, 40.0, 40.25, 40.5, 41.0, 41.5,
                    44.25]
volume_51_err = [0.0125] * len(volume_51_list)
pressure_51_err = [0.25] * len(pressure_51_list)

# 47 degree C
volume_47_list = [4.0, 3.5, 3.0, 2.5, 2.0, 1.9, 1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7]
pressure_47_list = [24.0, 26.5, 29.0, 31.75, 34.75, 35.25, 35.75, 36.25, 36.5, 36.75, 37.0, 37.0, 37.25,
                    37.25, 37.25, 37.5, 39.0, 48.0]
volume_47_err = [0.0125] * len(volume_47_list)
pressure_47_err = [0.25] * len(pressure_47_list)

print(len(volume_21_list), len(pressure_21_list))

plt.figure(figsize=(8, 6), dpi=80)
plt1 = plt.subplot(1, 1, 1)
plt.grid(True)

plt.errorbar(volume_21_list, pressure_21_list, pressure_21_err, volume_21_err, label=r'$T_1=21^\circ C$')
plt.errorbar(volume_31_list, pressure_31_list, pressure_31_err, volume_31_err, label=r'$T_2=31^\circ C$')
plt.errorbar(volume_41_list, pressure_41_list, pressure_41_err, volume_41_err, label=r'$T_3=41^\circ C$')
plt.errorbar(volume_46_list, pressure_46_list, pressure_46_err, volume_46_err, label=r'$T_4=46^\circ C$')
plt.errorbar(volume_47_list, pressure_47_list, pressure_47_err, volume_47_err, label=r'$T_5=47^\circ C$')
plt.errorbar(volume_51_list, pressure_51_list, pressure_51_err, volume_51_err, label=r'$T_6=51^\circ C$')

plt.xlabel(r'Volume [ml]')
plt.ylabel(r'Pressure [bar]')
plt.suptitle(r'p-V-Diagramm', fontsize=15, fontweight='bold')

plt.legend(loc='upper right', fontsize=12)
plt.show()

# latex_start_string = r'\begin{table}' + "\n" + r'\centering' + "\n" + r'\caption{Messwerte für XXX\degree C}' + \
#                      "\n" + r'\label{tab:val_werte_XXX}' + "\n\n" + r'\begin{tabular}[|c|c|]' + "\n" + \
#                      r'\hline' + "\n" + r'$p$ & $V$ \\ \hline' + "\n"



latex_end_string = r'\end{tabular}' + "\n" + r'\end{minipage}' + "\n" + r'\hfill' + "\n" + r'~'

latex_start_string = r'\begin{minipage}{0.32\linewidth}' + "\n" + \
                     r'\captionof{table}{XX\degree C}\label{tab:werte_XX}' + "\n" + \
                     r'\begin{tabular}{|c|c|}' + "\n" + \
                     r'\hline' + "\n" + r'$p$ & $V$ \\ \hline' + "\n"

def print_latex(pressure, volume):
    return_str = latex_start_string
    for i in range(len(pressure)):
        return_str += r'$' + str(pressure[i]) + r'$ & $' +str(volume[i]) + r'$ \\ \hline' + "\n"

    return_str += latex_end_string
    return return_str

#print(print_latex(pressure_21_list, volume_21_list))
#print("\n\n\n")
#print(print_latex(pressure_31_list, volume_31_list))
#print("\n\n\n")
#print(print_latex(pressure_41_list, volume_41_list))
#print("\n\n\n")
#print(print_latex(pressure_46_list, volume_46_list))
#print("\n\n\n")
#print(print_latex(pressure_47_list, volume_47_list))
#print("\n\n\n")
#print(print_latex(pressure_51_list, volume_51_list))
#print("\n\n\n")