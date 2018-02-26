import oscimport as osc
import matplotlib.pyplot as plt
import numpy as np
import fitting
import scipy.optimize


data = osc.read_osc_file("band/F0025CH1.CSV")
data2 = osc.read_osc_file("band/F0025CH2.CSV")
plt.figure(figsize=(8, 6), dpi=80)
plt1 = plt.subplot(1, 1, 1)
plt.grid(True)

# data["y"][:] = [data["y"][i]*0.2 for i in range(len(data["y"]))]

#plt.plot(data["x"], data["y"])
print(max(data["y"]))
g_amp_upper = max(data["y"])*1.1
g_amp_lower = max(data["y"])*0.9

#p, p_co = scipy.optimize.curve_fit(fitting.sine_fit, np.array(data["x"]), np.array(data["y"]),
#                                   bounds=([g_amp_lower, 2000, -np.pi], [g_amp_upper, 5000, np.pi]))
#p, p_co = scipy.optimize.leastsq(fitting.sine_fit, np.array(data["x"]), np.array(data["y"]))

#y_fit = [0]*len(data["x"])
#for i in range(len(data["x"])):
#    y_fit[i] = fitting.sine_fit(data["x"][i], p[0], p[1], p[2])

#p_err = np.sqrt(np.diag(p_co))
#print(p, p_err)

#plt.plot(data["x"], y_fit, color='orange')

#fitting.get_best_fit(data["x"], data["y"])

plt.plot(data2["x"], data2["y"], 'r')
#plt.yscale('log')

print("bla")

plt.show()