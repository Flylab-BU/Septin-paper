import csv
import tkinter as tk
from tkinter import filedialog

with open("output.txt", "w") as f:
    f.write("DATA")

for parameter in ["left_bended", "right_bended", "go_phase", "is_well_oriented", "is_coiled", "acc_dst", "velocity"]:

    # This function eliminates unnecessary rows in the input file
    # and turns parameter data into a matrix.
    def data_harvester(file):
        with open(file, newline='') as csvfile:
            fileread = csv.reader(csvfile)

            row_list = []

            for row in fileread:
                rowid = row[0].split("(")[0]

                if rowid == parameter:
                    edited_row = row[1:]
                    row_list.append(edited_row)

        return row_list

    # This function takes the matrix as input and turns it into a dictionary
    # where {larva1: [0, 0, 0, 0 ... 0]}
    def dict_creator(matrix):
        larvae_dict = {}
        larva_number = 0
        n_times = len(matrix[0])
        for x in range(n_times):
            larva_number = larva_number + 1
            larvae_dict[larva_number] = []

        return larvae_dict

    # This function assigns values to corresponding larvae
    def transfer_matrix_to_dict(matrix, larvae_dict):
        for row in matrix:
            larva_number = 0
            for larva_value in row:
                larva_number = larva_number + 1
                larvae_dict[larva_number].append(larva_value)
        return larvae_dict

    # This function prints the result as a text file where the number
    # and percentage of the parameter status is in.
    def dict_printer(value_dict):
        sum_dict = {}
        frame_numbers = []

        for value in value_dict:
            total_sum = 0
            frame_number = 0

            if parameter != "acc_dst":
                if parameter != "velocity":
                    for integer in value_dict[value]:
                        if integer == "1":
                            total_sum += 1
                            frame_number += 1
                        elif integer == "0":
                            frame_number += 1
                    frame_numbers.append(frame_number)
                else:
                    total = 0
                    counter2 = 0
                    for larvae in value_dict[value]:
                        if "e" in larvae:
                            counter2 += 1
                            pass
                        elif larvae != "" and larvae != '':
                            counter2 += 1
                            total += float(larvae)

                    if counter2 != 0:
                        total_sum = float((total / counter2)) * 1.534
                    else:
                        total_sum = 0

            else:
                if value_dict[value][-1] == "":
                    total_sum = 9999999999999999999999999
                else:
                    total_sum = float(value_dict[value][-1]) * 0.1534

            sum_dict[value] = total_sum

        return sum_dict, frame_numbers

    # This function determines the number of larva by the name of the file
    def result_size_determiner(name):
        list_from_name = name.split("/")
        number_of_larvae = list_from_name[-1].split(".")[0]
        return int(number_of_larvae)

    # This function narrows down the result dictionary by number of larvae
    def result_finalizer(number, result_dict, frame_numbers):
        final_dict = {}
        for larvaid in result_dict:
            if int(larvaid) <= int(number):
                final_dict[larvaid] = result_dict[larvaid]

        return final_dict, frame_numbers[0:int(number)]

    file = "/Users/tahaakkulah/PycharmProjects/PythonProject1/.venv/11.csv"

    parameter_matrix = data_harvester(file)

    larvae_dict = dict_creator(parameter_matrix)

    larvae_values = transfer_matrix_to_dict(parameter_matrix, larvae_dict)

    results, frame_numbers = dict_printer(larvae_values)

    result_size = result_size_determiner(file)

    final_result, final_frame_number = result_finalizer(result_size, results, frame_numbers)

    # Writer
    with open("output.txt", "a") as f:
        if parameter == "acc_dst":
            f.write("\n" + f"{parameter}:" + "\n")
            for values in final_result:
                valll = str(final_result[values])

                if len(valll.split(".")) > 1:
                    f.write((valll.split(".")[0] + "," + valll.split(".")[1]) + "\n")
                else:
                    f.write("dosyaya bak illy" + "\n")

        if parameter == "velocity":
            f.write("\n" + f"{parameter}:" + "\n")
            for values in final_result:
                vall = str(final_result[values])
                if len(vall.split(".")) > 1:
                    f.write((vall.split(".")[0] + "," + vall.split(".")[1]) + "\n")
                else:
                    f.write(vall + "\n")

        counter = 0
        if parameter != "acc_dst":
            if parameter != "velocity":
                f.write("\n" + f"Percentage of larvae {parameter}:" + "\n")
                for values in final_result:
                    if final_frame_number[counter] != 0:
                        val = str((float(final_result[values] / final_frame_number[counter]) * 100))
                        if len(val.split(".")) > 1:
                            f.write((val.split(".")[0] + "," + val.split(".")[1]) + "\n")
                        else:
                            f.write(val + "\n")
                    else:
                        f.write("0\n")
                    counter += 1