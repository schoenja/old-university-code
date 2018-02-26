import oscimport
import fitting
import matplotlib.pyplot as plt
import numpy as np


all_data = oscimport.read_directory("band")

measurements = []

for i in range(26):
    meas = all_data[str(i)]
    fitting_data1, fitting_data1_error = fitting.get_best_fit(meas["1"]["x"], meas["1"]["y"], meas["1"]["interval"])
    fitting_data2, fitting_data2_error = fitting.get_best_fit(meas["2"]["x"], meas["2"]["y"], meas["2"]["interval"])
    # print(fitting_data2_error, fitting_data1_error)
    print("CH1: ", '{:5.0f}'.format(fitting_data1[1]), " Hz, ", '{:2.2f}'.format(fitting_data1[0]), " V, ",
          '{:1.2f}'.format(fitting_data1[2]), "  ",
          "CH2: ", '{:5.0f}'.format(fitting_data2[1]), " Hz, ", '{:2.2f}'.format(fitting_data2[0]), " V, ",
          '{:1.2f}'.format(fitting_data2[2]), "   diff:", '{:1.2f}'.format((fitting_data2[2]-fitting_data1[2])/np.pi),
          sep='')

    # print(str(i), "has", fitting_data1[1])
    measurements.append({
        "ch1": fitting_data1,
        "ch1err": fitting_data1_error,
        "ch2": fitting_data2,
        "ch2err": fitting_data2_error
    })

# print(measurements)

x_vals = []
x_err_vals=[]
y_vals = []
y_err_vals=[]

for point in measurements:
    x_vals.append(point["ch1"][1])
    x_err_vals.append(point["ch1err"][1])
    y_val = point["ch2"][2] - point["ch1"][2]
    #print(y_val)
    # y_val = y_val % (2*np.pi)
    #if y_val < -0.01:
    #    y_val = y_val + 1*np.pi

    # NUR FÜR TIEFPASSFILTER!
    # if y_val > 0:
    #     y_val = y_val - np.pi

    # NUR FÜR BANDPASSFILTER
    if point["ch1"][1] > 3500:
        y_val = y_val - np.pi

    y_vals.append(y_val)
    y_err_vals.append(point["ch1err"][2]+point["ch2err"][2])

# plt.plot(x_vals, y_vals, 'ro')
plt.errorbar(x_vals, y_vals, xerr=x_err_vals, yerr=y_err_vals, fmt=',')
plt.xscale('log')
plt.show()