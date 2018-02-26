import csv
import os


# with open('F000a0CH1.CSV') as csvfile:
#    reader = csv.reader(csvfile)
#    for row in reader:
#        # list_row = row.split(',')
#        print(row[3], row[4])


def read_osc_file(filename: str):
    data_file_dict = {}
    data_file_dict["filename"] = os.path.basename(filename)
    data_file_dict["measurement"] = int(os.path.basename(filename).strip(".CSV")[1:-3])
    data_file_dict["channel"] = int(os.path.basename(filename).strip(".CSV")[-1:])
    data_file_dict["x"] = []
    data_file_dict["y"] = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        reader_list = list(reader)
        data_file_dict["records"] = float(reader_list[0][1])
        data_file_dict["interval"] = float(reader_list[1][1])
        data_file_dict["source"] = reader_list[6][1]
        data_file_dict["y_unit"] = reader_list[7][1]
        # data_file_dict["x_scale"]
        data_file_dict["x_unit"] = reader_list[10][1]

        for row in reader_list:
            data_file_dict["x"].append(float(row[3]))
            data_file_dict["y"].append(float(row[4]))

    return data_file_dict


def read_directory(directory: str):

    directory_data = {}

    file_data = []

    if os.path.exists(directory):
        # print(os.walk(directory))
        for (dirpath, dirnames, filenames) in os.walk(directory):
            directory_data["file_count"] = len(filenames)

            for file in filenames:
                filename = os.path.join(dirpath, file)
                file_data.append(read_osc_file(filename))

    # return file_data
    # print(len(file_data))
    for measurement in file_data:
        meas_no = measurement["measurement"]
        meas_ch = measurement["channel"]

        if str(meas_no) not in directory_data:
            directory_data[str(meas_no)] = {}


        directory_data[str(meas_no)][str(meas_ch)] = measurement

    return directory_data