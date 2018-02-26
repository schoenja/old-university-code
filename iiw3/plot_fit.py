from messungen import *
import matplotlib.pyplot as plt
import scipy.optimize
import numpy as np


def create_plt(name):
    plt.figure(figsize=(10, 7.5), dpi=80)
    plt1 = plt.subplot(1, 1, 1)
    plt.grid(True)
    plt.suptitle(name, fontsize=14, fontweight='bold')
    plt.xlabel(r'Magnetische Flussdichte $B$ [mT]')
    plt.ylabel(r'Hallspannung $U_H$ [$\mu$V]')


def plt_data(xdata, ydata, xerr, yerr):
    plt.errorbar(xdata, ydata, yerr, xerr,
                 fmt='.', ecolor='black',
                 label='Messwerte')


def fit_func(x, a, b):
    return a*x+b


def convert_func(x):
    return 780*(1-np.exp(-0.334*x))-84


def create_fit(xdata, ydata):
    p, p_co = scipy.optimize.curve_fit(fit_func, np.array(xdata), np.array(ydata))
    return p, np.sqrt(np.diag(p_co))


def plot_fit(xdata, p, perr, fxloc, fyloc):
    yfit = [0]*12
    for i in range(12):
        yfit[i] = fit_func(xdata[i], p[0], p[1])

    plt.plot(xdata, yfit, color='red', label='Fit')
    plt.text(fxloc, fyloc,
             "a*x+b\n" + "a=" + '{:.3e}'.format(p[0]) + "±" + '{:.3e}'.format(perr[0]) + "\n"
             + "b=" + '{:.3e}'.format(p[1]) + "±" + '{:.3e}'.format(perr[1]),
             horizontalalignment='center', verticalalignment='top',
             bbox={'facecolor': 'white', 'alpha': 1.0, 'pad': 10})


def x_error(xdata):
    xerr = [0]*len(xdata)
    for i in range(len(xdata)):
        xerr[i] = max([abs(convert_func(xdata[i]-0.05)-convert_func(xdata[i])),
                       abs(convert_func(xdata[i]+0.05)-convert_func(xdata[i]))])
    return xerr

# to_plot = messungen["Ag, 10A, #1"]

# create_plt()
# nxdata = list(map(lambda x: convert_func(x), to_plot["A"]))
# nydata = to_plot["V"]

# nxerr = list(map(lambda x: convert_func(x), [0.05]*12))
# nxerr = x_error(nxdata)
# nyerr = [0.3]*12

# plt_data(nxdata, nydata, nxerr, nyerr)

# np, np_err = create_fit(nxdata, nydata)
# plot_fit(nxdata, np)

# plt.show()

fit_data = {}

for name, data in messungen.items():
    create_plt(name)
    plt.xlim(data["xmin"], data["xmax"])
    plt.ylim(data["ymin"], data["ymax"])

    nxdata = list(map(lambda x: convert_func(x), data["A"]))
    nydata = data["V"]
    nxerr = x_error(nxdata)
    nyerr = [0.3]*12

    plt_data(nxdata, nydata, nxerr, nyerr)
    npd, np_err = create_fit(nxdata, nydata)
    fit_data[name] = {"param": npd, "param_err": np_err}
    plot_fit(nxdata, npd, np_err, data["fx"], data["fy"])

    plt.legend(loc=data["leg_loc"])


    # plt.savefig("test__" + data["fn"] + ".png")

# print(fit_data)

same_meas_list = {
    "Ag10": ["Ag, 10A, #1", "Ag, 10A, #2", "Ag, 10A, #3"],
    "Ag15": ["Ag, 15A, #1", "Ag, 15A, #2", "Ag, 15A, #3"],
    "W10": ["W, 10A, #1", "W, 10A, #2", "W, 10A, #3"],
    "W15": ["W, 15A, #1", "W, 15A, #2", "W, 15A, #3"],
}


def std_mean(nums):
    aver = sum(nums)/3
    return aver, (np.sqrt(1/2*sum(list(map(lambda x: (aver - x)**2, nums)))))/np.sqrt(2)


for i, j in same_meas_list.items():
    my_nums = []
    for l in j:
        my_nums.append(fit_data[l]["param"][0])
    av, sdom = std_mean(my_nums)
    print(i, av, sdom)


