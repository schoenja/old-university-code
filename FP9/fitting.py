import numpy as np
import scipy.optimize


def sine_fit(x, a, b, c):
    return a*np.cos(2*np.pi*b*x+c)

def cosine_fit(x, a, b, c):
    return a*np.cos(2*np.pi*b*x+c)

def freq_estimate(y_list, y_scale):
    zero_points = []
    zero_point_distance = []
    y_max = max(y_list)

    for i in range(len(y_list)):
        if abs(y_list[i]) < 0.05*y_max:
            zero_points.append(i)

    for j in range(1,len(zero_points)):
        if (zero_points[j] - zero_points[j-1]) > 10:
            zero_point_distance.append(zero_points[j] - zero_points[j-1])

    average_distance = sum(zero_point_distance)/float(len(zero_point_distance))

    return 1/(average_distance*2*y_scale)
    # return zero_point_distance, zero_points, average_distance

def get_best_fit(x_data, y_data, g_freq):
    g_max = max(y_data)
    g_min = min(y_data)

    #g_freq = freq_estimate(y_data, x_interval)
    #print(g_freq)

    # Try positive sine fit
    p_sine_pos, p_co_sine_pos = scipy.optimize.curve_fit(sine_fit, x_data, y_data,
                                                         bounds=([g_max*0.8, g_freq*0.85, -1*np.pi], [g_max*1.2, g_freq*1.15, 1*np.pi]))

    p_err_sine_pos = np.sqrt(np.diag(p_co_sine_pos))

    return p_sine_pos, p_err_sine_pos


def old(x_data, y_data):
    g_max = max(y_data)
    g_min = min(y_data)

    g_freq = 0
    p_sine_neg, p_co_sine_neg = scipy.optimize.curve_fit(sine_fit, x_data, y_data,
                                                         bounds=([g_min * 1.15, g_freq*0.85, -np.pi], [g_min*0.85, g_freq*1.15, np.pi]))
    p_err_sine_neg = np.sqrt(np.diag(p_co_sine_neg))

    p_cosine_pos, p_co_cosine_pos = scipy.optimize.curve_fit(cosine_fit, x_data, y_data,
                                                         bounds=(
                                                         [g_max * 0.85, g_freq*0.85, -np.pi], [g_max * 1.15, g_freq*1.15, np.pi]))
    p_err_cosine_pos = np.sqrt(np.diag(p_co_cosine_pos))

    p_cosine_neg, p_co_cosine_neg = scipy.optimize.curve_fit(cosine_fit, x_data, y_data,
                                                         bounds=(
                                                         [g_min * 1.15, g_freq*0.85, -np.pi], [g_min * 0.85, g_freq*1.15, np.pi]))
    p_err_cosine_neg = np.sqrt(np.diag(p_co_cosine_neg))

    # print( "\n",
    #     p_sine_pos, p_err_sine_pos, "\n",
    #     p_sine_neg, p_err_sine_neg, "\n",
    #     p_cosine_pos, p_err_cosine_pos, "\n",
    #     p_cosine_neg, p_err_cosine_neg, "\n"
    # )

    result_list = [
        (p_sine_pos, p_err_sine_pos),
        (p_sine_neg, p_err_sine_neg),
        (p_cosine_pos, p_err_cosine_pos),
        (p_cosine_neg, p_err_cosine_neg)
    ]

    error_average = [0]*4
    for j in range(3):
        for i in range(4):
            p_val, p_err = result_list[i]
            error_average[j] = error_average[j] + p_err[j]

        error_average[j] = error_average[j]/3 # div by 3 on purpose instead of 4 so easier to check if smaller

    if ((p_err_sine_pos[0] < error_average[0]) and
            (p_err_sine_pos[1] < error_average[1]) and
            (p_err_sine_pos[2] < error_average[2])):
        return p_sine_pos, p_err_sine_pos
    elif ((p_err_sine_neg[0] < error_average[0]) and
            (p_err_sine_neg[1] < error_average[1]) and
            (p_err_sine_neg[2] < error_average[2])):
        p_sine_neg[0] = p_sine_neg[0]*(-1)
        return p_sine_neg, p_err_sine_neg
    elif ((p_err_cosine_pos[0] < error_average[0]) and
            (p_err_cosine_pos[1] < error_average[1]) and
            (p_err_cosine_pos[2] < error_average[2])):
        return p_cosine_pos, p_co_cosine_pos
    elif ((p_err_cosine_neg[0] < error_average[0]) and
            (p_err_cosine_neg[1] < error_average[1]) and
            (p_err_cosine_neg[2] < error_average[2])):
        return p_cosine_neg, p_co_cosine_neg
    else:
        print("failed")
        return None, None

