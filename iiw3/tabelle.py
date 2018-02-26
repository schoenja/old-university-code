from messungen import *


latex_start_string_1 = r'\begin{minipage}{0.32\linewidth}' + "\n" + r'\captionof{table}{'
latex_start_string_2 = r'}\label{tab:werte_'
latex_start_string_3 = r'}' + "\n" + \
                     r'\begin{tabular}{|c|c|}' + "\n" + \
                     r'\hline' + "\n" + r'$I$ & $U_H$ \\ \hline' + "\n"

latex_end_string = r'\end{tabular}' + "\n" + r'\end{minipage}' + "\n" + r'\hfill' + "\n" + r'~'

same_meas_list = {
    "Ag10": ["Ag, 10A, #1", "Ag, 10A, #2", "Ag, 10A, #3"],
    "Ag15": ["Ag, 15A, #1", "Ag, 15A, #2", "Ag, 15A, #3"],
    "W10": ["W, 10A, #1", "W, 10A, #2", "W, 10A, #3"],
    "W15": ["W, 15A, #1", "W, 15A, #2", "W, 15A, #3"],
}

full_string = ""

for group_name, j in same_meas_list.items():
    full_string += "{\n"
    for i in j:
        x_list = messungen[i]["A"]
        y_list = messungen[i]["V"]
        name = messungen[i]["fn"][8:]
        full_string += latex_start_string_1 + "NAME" + latex_start_string_2 + name + latex_start_string_3
        for k in range(len(x_list)):
            full_string += "$" + '{:.3e}'.format(x_list[k]) + "$ & $" + '{:.3e}'.format(y_list[k]) + r'$ \\ \hline' + "\n"
        full_string += latex_end_string

    full_string += "}\n"

file_f = open('tex.txt', 'w')
file_f.write(full_string)
file_f.close()
