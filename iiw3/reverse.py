from messungen import *
import scipy.optimize
import numpy as np


same_meas_list = {
    "Ag10": {"items": ["Ag, 10A, #1", "Ag, 10A, #2", "Ag, 10A, #3"], "beta": 58824},
    "Ag15": {"items": ["Ag, 15A, #1", "Ag, 15A, #2", "Ag, 15A, #3"], "beta": 39216},
    "W10": {"items": ["W, 10A, #1", "W, 10A, #2", "W, 10A, #3"], "beta": -66667},
    "W15": {"items": ["W, 15A, #1", "W, 15A, #2", "W, 15A, #3"], "beta": -44444},
}


results = {}


def fit_func(x, a, b, c):
    return a*(1-np.exp(b*x))+c


def std_mean(nums):
    aver = sum(nums)/3
    return aver, (np.sqrt(1/2*sum(list(map(lambda x: (aver - x)**2, nums)))))/np.sqrt(2)


for set_name, set_items in same_meas_list.items():
    for element in set_items["items"]:
        bi_list = list(map(lambda x: (10**-6)*x*set_items["beta"], messungen[element]["V"]))
        p, p_co = scipy.optimize.curve_fit(fit_func, np.array(messungen[element]["A"]), np.array(bi_list),
                                           bounds=([0, -np.inf, -np.inf], [np.inf, 0, np.inf]))
        results[element] = p


results2 = {}

for set_name2, set_items2 in same_meas_list.items():
    a_l = []
    b_l = []
    c_l = []
    for i in set_items2["items"]:
        a_l.append(results[i][0])
        b_l.append(results[i][1])
        c_l.append(results[i][2])
    res_dict = {}
    res_dict["av"], res_dict["ave"] = std_mean(a_l)
    res_dict["bv"], res_dict["bve"] = std_mean(b_l)
    res_dict["cv"], res_dict["cve"] = std_mean(c_l)
    results2[set_name2] = res_dict

for q,w in results2.items():
    print(q)
    print("a:", w["av"], "±", w["ave"])
    print("b:", w["bv"], "±", w["bve"])
    print("c:", w["cv"], "±", w["cve"])
    print("")
