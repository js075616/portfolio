# Creates a top ten table based on the DataFrame passed in. Prints the table to the console and returns the max index
# of the first maximum
# Written by Jake Schwarz
from tabulate import tabulate


# Used to calculate the TP and FP of each sample and make a table of the top 10 based on TP - FP
def top_ten_table(passed_csv):
    tp = [0 for i in range(1411)]
    fp = [0 for i in range(1411)]
    tp_minus_fp = [0 for i in range(1411)]
    gene_names = [0 for i in range(1411)]
    c_num = 0
    nc_num = 0
    number_of_rows = passed_csv.shape[0]
    # print("Number of Rows: " + str(number_of_rows))
    for row in range(0, number_of_rows):
        if str(passed_csv.iloc[row, 0][0]) == "C":
            c_num += 1
        else:
            nc_num += 1
    if c_num == 0:
        print("This is a pure set of NC samples, there may be no need to separate further.")
    elif nc_num == 0:
        print("This is a pure set of C samples, there may be no need to separate further.")
    # print("c_num: " + str(c_num))
    # print("nc_num: " + str(nc_num))
    for column in range(1, 1410):
        for row in range(0, c_num):
            tp[column] += passed_csv.iloc[row, column]
        for row2 in range(c_num, nc_num + c_num):
            fp[column] += passed_csv.iloc[row2, column]

    for i in range(0, 1141):
        tp_minus_fp[i] = tp[i] - fp[i]
        gene_names[i] = passed_csv.columns[i]

    max_value = max(tp_minus_fp)
    max_index = tp_minus_fp.index(max_value)
    total_max_index = max_index  # 107 for DOCK3
    # print("Max value in TP - FP is " + str(max_value) + " with an index of " + str(max_index))
    # print(passed_csv.columns[max_index])
    table = [["Mutation", "TP - FP"], [passed_csv.columns[max_index], max_value]]
    tp_minus_fp.pop(max_index)
    gene_names.pop(max_index)
    for i in range(0, 9):
        max_value = max(tp_minus_fp)
        max_index = tp_minus_fp.index(max_value)
        # print("Max value in TP - TP is " + str(max_value) + " with an index of " + str(max_index))
        # print(passed_csv.columns[max_index])
        table.append([gene_names[max_index], max_value])
        tp_minus_fp.pop(max_index)
        gene_names.pop(max_index)
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
    print("")
    return total_max_index


def accuracy_table(passed_csv):
    tp = [0 for i in range(1411)]
    fp = [0 for i in range(1411)]
    tn = [0 for i in range(1411)]
    fn = [0 for i in range(1411)]
    accuracy = [0 for i in range(1411)]
    gene_names = [0 for i in range(1411)]
    c_num = 0
    nc_num = 0
    number_of_rows = passed_csv.shape[0]
    # print("Number of Rows: " + str(number_of_rows))
    for row in range(0, number_of_rows):
        if str(passed_csv.iloc[row, 0][0]) == "C":
            c_num += 1
        else:
            nc_num += 1
    if c_num == 0:
        print("This is a pure set of NC samples, there may be no need to separate further.")
    elif nc_num == 0:
        print("This is a pure set of C samples, there may be no need to separate further.")
    # print("c_num: " + str(c_num))
    # print("nc_num: " + str(nc_num))
    for column in range(1, 1410):
        for row in range(0, c_num):
            if passed_csv.iloc[row, column] == 0:
                fn[column] += 1
            else:
                tp[column] += passed_csv.iloc[row, column]
        for row2 in range(c_num, nc_num + c_num):
            if passed_csv.iloc[row2, column] == 0:
                tn[column] += 1
            else:
                fp[column] += passed_csv.iloc[row2, column]

    for i in range(0, 1141):
        accuracy[i] = (tp[i] + tn[i]) / 162
        gene_names[i] = passed_csv.columns[i]

    max_accuracy = max(accuracy)
    max_index = accuracy.index(max_accuracy)
    current_tp = tp[max_index]
    current_tn = tn[max_index]
    current_fp = fp[max_index]
    current_fn = fn[max_index]
    total_max_index = max_index  # 107 for DOCK3
    # print("Max value in TP - FP is " + str(max_value) + " with an index of " + str(max_index))
    # print(passed_csv.columns[max_index])
    table = [["Mutation", "Accuracy", "TP", "TN", "FP", "FN"], [passed_csv.columns[max_index], max_accuracy, current_tp, current_tn, current_fp, current_fn]]
    accuracy.pop(max_index)
    tp.pop(max_index)
    tn.pop(max_index)
    fp.pop(max_index)
    fn.pop(max_index)
    gene_names.pop(max_index)
    for i in range(0, 9):
        max_accuracy = max(accuracy)
        max_index = accuracy.index(max_accuracy)
        current_tp = tp[max_index]
        current_tn = tn[max_index]
        current_fp = fp[max_index]
        current_fn = fn[max_index]
        # print("Max value in TP - TP is " + str(max_value) + " with an index of " + str(max_index))
        # print(passed_csv.columns[max_index])
        table.append([passed_csv.columns[max_index], max_accuracy, current_tp, current_tn, current_fp, current_fn])
        accuracy.pop(max_index)
        tp.pop(max_index)
        tn.pop(max_index)
        fp.pop(max_index)
        fn.pop(max_index)
        gene_names.pop(max_index)
    print("Accuracy Table")
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
    print("")


def calculate_max_index(passed_csv):
    tp = [0 for i in range(1411)]
    fp = [0 for i in range(1411)]
    tp_minus_fp = [0 for i in range(1411)]
    gene_names = [0 for i in range(1411)]
    c_num = 0
    nc_num = 0
    number_of_rows = passed_csv.shape[0]
    # print("Number of Rows: " + str(number_of_rows))
    for row in range(0, number_of_rows):
        if str(passed_csv.iloc[row, 0][0]) == "C":
            c_num += 1
        else:
            nc_num += 1
    # print("c_num: " + str(c_num))
    # print("nc_num: " + str(nc_num))
    for column in range(1, 1410):
        for row in range(0, c_num):
            tp[column] += passed_csv.iloc[row, column]
        for row2 in range(c_num, nc_num + c_num):
            fp[column] += passed_csv.iloc[row2, column]

    for i in range(0, 1141):
        tp_minus_fp[i] = tp[i] - fp[i]
        gene_names[i] = passed_csv.columns[i]

    max_value = max(tp_minus_fp)
    max_index = tp_minus_fp.index(max_value)
    return max_index
