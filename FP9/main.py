import oscimport
import fitting
import matplotlib.pyplot as plt
import numpy as np
import cmath


def import_data(name, n_meas):
    measurements = []
    all_data = oscimport.read_directory(name)
    for i in range(n_meas):
        meas = all_data[str(i)]

        g_freq = fitting.freq_estimate(meas["1"]["y"], meas["1"]["interval"])

        fitting_data1, fitting_data1_error = fitting.get_best_fit(meas["1"]["x"], meas["1"]["y"], g_freq)
        fitting_data2, fitting_data2_error = fitting.get_best_fit(meas["2"]["x"], meas["2"]["y"], g_freq)

        measurements.append({
            "ch1": fitting_data1,
            "ch1err": fitting_data1_error,
            "ch2": fitting_data2,
            "ch2err": fitting_data2_error
        })

        # print("CH1: ", '{:6.0f}'.format(fitting_data1[1]), "±", '{:6.0f}'.format(fitting_data1_error[1]),
        #       " Hz, ", '{:2.5f}'.format(fitting_data1[0]), "±", '{:2.5f}'.format(fitting_data1_error[0]), " V, ",
        #       '{:2.5f}'.format(fitting_data1[2]), "±", '{:2.5f}'.format(fitting_data1_error[2]), "  ",
        #       "CH2: ", '{:6.0f}'.format(fitting_data2[1]), "±", '{:6.0f}'.format(fitting_data2_error[1]),
        #       " Hz, ", '{:2.5f}'.format(fitting_data2[0]),  "±", '{:2.5f}'.format(fitting_data2_error[0]), " V, ",
        #       '{:2.5f}'.format(fitting_data2[2]), "±", '{:2.5f}'.format(fitting_data2_error[2]), "  ",
        #       "   diff:", '{:1.4f}'.format((fitting_data2[2] - fitting_data1[2]) / np.pi),
        #       sep='')
        print("$", '{:6.0f}'.format(fitting_data1[1]), "$ & $", '{:2.5f}'.format(fitting_data1[0]),
              "$ & $", '{:2.5f}'.format(fitting_data1[2]), "$ & $", '{:6.0f}'.format(fitting_data2[1]),
              "$ & $", '{:2.5f}'.format(fitting_data2[0]), "$ & $", '{:2.5f}'.format(fitting_data2[2]), "$ \\\\ \\hline")

    return measurements


def phase_d_points(measurements):
    x_vals = []
    x_err_vals = []
    y_vals = []
    y_err_vals = []
    imped = []

    for point in measurements:
        x_vals.append(point["ch1"][1])
        x_err_vals.append(point["ch1err"][1])

        # calc phase
        impe = impedance(point["ch1"][1])
        # imped_out = impe_out(point["ch1"][1])
        # print(impe.real, impe.imag)
        # print((0.5*np.pi) - np.arctan(impe.imag/impe.real))
        # only bandpass:
        if point["ch1"][1]<2005:
            imped.append((0.5 * np.pi) - np.arctan(impe.imag / impe.real))   # -pi für tiefpass
        else:
            imped.append((-0.5 * np.pi) - np.arctan(impe.imag / impe.real))  # -pi für tiefpass

        # the others
        #imped.append((-0.5*np.pi) - np.arctan(impe.imag/impe.real)) # -pi für tiefpass
        #imped.append(np.arctan(imped_out.imag / imped_out.real) - np.arctan(impe.imag / impe.real))  # -pi für tiefpass

        y_val = point["ch2"][2] - point["ch1"][2]
        #if point["ch2"][2]<0:
        #    y_val = (point["ch2"][2] + np.pi - point["ch1"][2])
        #else:
        #    y_val = point["ch2"][2] - point["ch1"][2]
        # print(y_val)
        # y_val = y_val % (2*np.pi)
        # if y_val < -0.01:
        #    y_val = y_val + 1*np.pi

        # NUR FÜR TIEFPASSFILTER!
        # if y_val > 0:
        #     y_val = y_val - np.pi

        # NUR FÜR BANDPASSFILTER
        #if point["ch1"][1] > 3500:
        #    y_val = y_val - np.pi

        y_vals.append(y_val)
        y_err_vals.append(point["ch1err"][2] + point["ch2err"][2])

    return (x_vals, y_vals, x_err_vals, y_err_vals, imped)


def voltage_d_points(measurements):
    x_vals = []
    x_err_vals = []
    y_vals = []
    y_err_vals = []
    yb_vals = []

    for point in measurements:
        x_vals.append(point["ch1"][1])
        yb_vals.append(point["ch1"][0])
        x_err_vals.append(point["ch1err"][1])

        y_vals.append(abs(point["ch2"][0]/point["ch1"][0]))

    return (x_vals, y_vals, x_err_vals, y_err_vals, yb_vals)


def pegel_d_points(measurements):
    x_vals = []
    x_err_vals = []
    y_vals = []
    y_err_vals = []
    # yb_vals = []

    for point in measurements:
        x_vals.append(point["ch1"][1])
        # yb_vals.append(point["ch2"][1])
        x_err_vals.append(point["ch1err"][1])

        y_vals.append(20*np.log10(point["ch2"][0]/point["ch1"][0]))

    return (x_vals, y_vals, x_err_vals, y_err_vals)


def phase_diagram(xl, yl, xe, ye, imped, name):

    # xl = []
    # yl = []
    # temp_list = []
    # for i in range(len(xli)):
    #     temp_list.append((xli[i], yli[i]))
    # temp_list = sorted(temp_list, key=lambda pair: pair[0])
    # for i in range(len(temp_list)):
    #     xl.append(temp_list[i][0])
    #     yl.append(temp_list[i][1])

    plt.figure(figsize=(10, 7.5), dpi=80)
    plt1 = plt.subplot(1, 1, 1)
    plt.grid(True)
    plt.suptitle(name, fontsize=14, fontweight='bold')
    plt.xlabel(r'Frequency $\omega$ [log Hz]')
    plt.ylabel(r'Phase shift [radian]')

    # plt.errorbar(xl, yl, xerr=xe, yerr=ye, fmt=',')
    plt.plot(xl, yl, 'ro', label='Measurements')

    imp_x = np.logspace(1, 4.5, base=10.0, endpoint=True)
    imp_y = []
    for i in range(len(imp_x)):
        impe = impedance(imp_x[i])
        imp_y.append((0.5*np.pi) - np.arctan(impe.imag/impe.real))

        #if imp_x[i]<2005:
        #    imp_y.append((0.5 * np.pi) - np.arctan(impe.imag / impe.real))  # -pi für tiefpass
        #else:
        #    imp_y.append((-0.5 * np.pi) - np.arctan(impe.imag / impe.real))

    plt.plot(imp_x, imp_y, label='Calculated')
    plt.xscale('log')
    # plt.axis([5,5000,-0.5*np.pi,0.5*np.pi])
    plt.minorticks_on()
    plt.legend()
    plt.show()

def voltage_diagram(xl, yl, xe, ye, yb, name):
    plt.figure(figsize=(10, 7.5), dpi=80)
    plt1 = plt.subplot(1, 1, 1)
    plt.grid(True)
    plt.suptitle(name, fontsize=14, fontweight='bold')
    plt.xlabel(r'Frequency $\omega$ [log Hz]')
    plt.ylabel(r'Voltage ratio $\frac{U_2}{U_1}$')

    plt.plot(xl, yl, 'ro', label='Measurements')

    ylcalc = []
    xlcalc = np.logspace(1, 4.5, base=10.0, endpoint=True)
    for i in range(len(xlcalc)):
        #impe = impedance(xl[i])
        #phi = np.arctan(impe.imag/impe.real)
        #volt = abs(0.0002*impe*np.exp(-1*complex(0,1)*phi))
        #ylcalc.append(abs(volt/yb[i]))
        ylcalc.append(abs((4700 + (complex(0, 1) * (xlcalc[i] * (2 * np.pi)) * (380 * 10 ** -3)))/((complex(0,1)*(xlcalc[i]*(2*np.pi))*(380*10**-3))))**-1)
        # ylcalc.append(abs((4700 + (1/(complex(0, 1) * (xlcalc[i] * (2 * np.pi)) * (17*10**-9))))/ (1/(complex(0, 1) * (xlcalc[i] * (2 * np.pi)) * (17*10**-9))))**-1)
        #ylcalc.append(
        #    abs(
        #        (4700 + 1 / (1 / (complex(0, 1) * (xlcalc[i] * (2 * np.pi)) * (100 * 10 ** -3)) + (
        #        (complex(0, 1) * (xlcalc[i] * (2 * np.pi)) * (63 * 10 ** -9))))) /
        #        (1/(1/(complex(0,1)*(xlcalc[i]*(2*np.pi))*(100*10**-3)) + ((complex(0, 1) * (xlcalc[i] * (2 * np.pi)) * (63 * 10 ** -9)))))
        #    )**-1
        #)


    plt.plot(xlcalc, ylcalc, label='Calculated')
    plt.xscale('log')
    plt.legend()
    plt.show()


def pegel_diagram(xl, yl, xe, ye, name):
    plt.figure(figsize=(10, 7.5), dpi=80)
    plt1 = plt.subplot(1, 1, 1)
    plt.grid(True)
    plt.suptitle(name, fontsize=14, fontweight='bold')
    plt.xlabel(r'Frequency $\omega$ [log Hz]')
    plt.ylabel(r'Gain $20\cdot\log\frac{U_2}{U_1}$ [dB]')

    plt.plot(xl, yl, 'ro', label='Measurements')

    ylcalc = []
    xlcalc = np.logspace(1, 4.5, base=10.0, endpoint=True)
    for i in range(len(xlcalc)):
        # impe = impedance(xl[i])
        # phi = np.arctan(impe.imag/impe.real)
        # volt = abs(0.0002*impe*np.exp(-1*complex(0,1)*phi))
        # ylcalc.append(abs(volt/yb[i]))
        ylcalc.append(20*np.log10(abs((4700 + (complex(0, 1) * (xlcalc[i] * (2 * np.pi)) * (380 * 10 ** -3))) / (
        (complex(0, 1) * (xlcalc[i] * (2 * np.pi)) * (380 * 10 ** -3)))) ** -1))
        #ylcalc.append(20*np.log10(abs((4700 + (1/(complex(0, 1) * (xlcalc[i] * (2 * np.pi)) * (17*10**-9))))/ (1/(complex(0, 1) * (xlcalc[i] * (2 * np.pi)) * (17*10**-9))))**-1))
        # ylcalc.append(20*np.log10(
        #     abs(
        #         (4700 + 1 / (1 / (complex(0, 1) * (xlcalc[i] * (2 * np.pi)) * (100 * 10 ** -3)) + (
        #             (complex(0, 1) * (xlcalc[i] * (2 * np.pi)) * (63 * 10 ** -9))))) /
        #         (1 / (1 / (complex(0, 1) * (xlcalc[i] * (2 * np.pi)) * (100 * 10 ** -3)) + (
        #         (complex(0, 1) * (xlcalc[i] * (2 * np.pi)) * (63 * 10 ** -9)))))
        #     ) ** -1)
        #  )

    plt.plot(xlcalc, ylcalc, label='Calculated')

    # plt.plot(xl, imped, 'ro')
    plt.xscale('log')
    plt.legend()
    plt.show()


def impedance(freq):
    return 4700 + (complex(0,1)*(freq*(2*np.pi))*(380*10**-3)) # Hochpass
    # return 4700 + (1/(complex(0, 1) * (freq * (2 * np.pi)) * (17*10**-9)))  # Tiefpass
    # return 4700 + 1/(1/(complex(0,1)*(freq*(2*np.pi))*(100*10**-3)) + ((complex(0, 1) * (freq * (2 * np.pi)) * (63 * 10 ** -9))))

def impe_out(freq):
    return 1/(1/(complex(0,1)*(freq*(2*np.pi))*(100*10**-3)) + ((complex(0, 1) * (freq * (2 * np.pi)) * (63 * 10 ** -9))))



measurements = import_data("hoch", 58)
xl, yl, xe, ye, imped = phase_d_points(measurements)
phase_diagram(xl, yl, xe, ye, imped, "Hochpass")



xl, yl, xe, ye, yb = voltage_d_points(measurements)
voltage_diagram(xl, yl, xe, ye, yb, "Hochpass")

xl, yl, xe, ye = pegel_d_points(measurements)
pegel_diagram(xl, yl, xe, ye, "Hochpass")