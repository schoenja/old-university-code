from messungen import *


for key, data in messungen.items():
    f = open(data["fn"][8:], 'w')

    data_string = ""
    for i in range(len(data["A"])):
        data_string += str(data["A"][i]) + ", " + str(data["V"][i]) + "\n\r"

    f.write(data_string)
    f.close()

