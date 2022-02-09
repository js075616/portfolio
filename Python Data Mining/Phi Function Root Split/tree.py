

import pandas as pd
from table import *
from matrix import *

TP = 0
TN = 0
FP = 0
FN = 0
ROOT_NAME = ""
AVG_TP = 0
AVG_TN = 0
AVG_FP = 0
AVG_FN = 0
AVG_accuracy = 0
AVG_sensitivity = 0
AVG_miss_rate = 0
AVG_specificity = 0
AVG_precision = 0
AVG_falsedr = 0
AVG_falseor = 0


class Node:
    def __init__(self, index, c):
        self.left = None
        self.right = None
        self.index = index
        self.c = c


def two_height_tree_tpfp(passed_csv):
    group_a = df = pd.DataFrame(columns=passed_csv.columns)  # Samples that do have the mutation
    group_b = df = pd.DataFrame(columns=passed_csv.columns)
    a_entries = []
    b_entries = []
    total_max_index = calculate_max_index_tpfp(passed_csv)
    print("Root is: " + str(passed_csv.columns[total_max_index]))
    global ROOT_NAME
    ROOT_NAME = passed_csv.columns[total_max_index]
    number_of_rows = passed_csv.shape[0]
    # print(total_max_index)
    for i in range(0, number_of_rows):
        if passed_csv.iloc[i, total_max_index] == 1:
            a_entries.append(passed_csv.iloc[[i]])
        else:
            b_entries.append(passed_csv.iloc[[i]])
    # print(a_entries)
    # print(b_entries)
    group_a = pd.concat(a_entries)
    group_b = pd.concat(b_entries)
    root = Node(total_max_index, None)
    total_max_index = calculate_max_index_tpfp(group_a)
    print("Left node (A) is: " + str(passed_csv.columns[total_max_index]))
    root.left = Node(total_max_index, None)
    # print(root.left.index)
    total_max_index = calculate_max_index_tpfp(group_b)
    print("Right node (B) is: " + str(passed_csv.columns[total_max_index]))
    root.right = Node(total_max_index, None)
    # print(root.right.index)
    root.left.left = Node(None, "C")
    root.left.right = Node(None, "NC")
    root.right.left = Node(None, "C")
    root.right.right = Node(None, "NC")
    print("")
    return root


def evaluator(tree, row):
    global TP
    global TN
    global FP
    global FN
    global AVG_TP
    global AVG_TN
    global AVG_FP
    global AVG_FN
    if row.iloc[tree.index] == 1:
        tree = tree.left
    else:
        tree = tree.right
    if row.iloc[tree.index] == 1:
        tree = tree.left
    else:
        tree = tree.right

    if tree.c == "C":
        if row.iloc[0][0] == "C":
            TP += 1
            AVG_TP += 1
        else:
            FP += 1
            AVG_FP += 1
    elif tree.c == "NC":
        if row.iloc[0][0] == "N":
            TN += 1
            AVG_TN += 1
        else:
            FN += 1
            AVG_FN += 1

    return tree.c


def print_eval():
    global AVG_accuracy
    global AVG_sensitivity
    global AVG_miss_rate
    global AVG_specificity
    global AVG_precision
    global AVG_falsedr
    global AVG_falseor
    print("Metrics for Root " + str(ROOT_NAME))
    accuracy = (TP + TN) / (TP + TN + FN + FP)
    if TP + FN != 0:
        sensitivity = TP / (TP + FN)
        miss_rate = FN / (FN + TP)
    else:
        sensitivity = TP / 0.00000001
        miss_rate = FN / 0.00000001

    if TN + FP != 0:
        specificity = TN / (TN + FP)
    else:
        specificity = TN / 0.00000001

    if TP + FP != 0:
        precision = TP / (TP + FP)
    else:
        precision = TP / 0.00000001

    if FP + TP != 0:
        falsedr = FP / (FP + TP)
    else:
        falsedr = FP / 0.00000001

    if FN + TN != 0:
        falseor = FN / (FN + TN)
    else:
        falseor = FN / 0.00000001

    AVG_accuracy += accuracy
    AVG_sensitivity += sensitivity
    AVG_miss_rate += miss_rate
    AVG_specificity += specificity
    AVG_precision += precision
    AVG_falsedr += falsedr
    AVG_falseor += falseor
    print("Accuracy: " + str(accuracy * 100) + "%")
    print("Sensitivity: " + str(sensitivity * 100) + "%")
    print("Specificity: " + str(specificity * 100) + "%")
    print("Miss Rate: " + str(miss_rate * 100) + "%")
    print("Precision: " + str(precision * 100) + "%")
    print("False Discovery Rate: " + str(falsedr * 100) + "%")
    print("False Omission Rate: " + str(falseor * 100) + "%")
    print("")
    print_matrix_eval(TP, TN, FP, FN, ROOT_NAME)


def reset_eval():
    global TP
    global TN
    global FP
    global FN
    global ROOT_NAME
    TP = 0
    TN = 0
    FP = 0
    FN = 0


def print_avg():
    print("Averages:")
    print("Average Accuracy: " + str((AVG_accuracy / 3) * 100) + "%")
    print("Average Sensitivity: " + str((AVG_sensitivity / 3) * 100) + "%")
    print("Average Miss Rate: " + str((AVG_miss_rate / 3) * 100) + "%")
    print("Average Specificity: " + str((AVG_specificity / 3) * 100) + "%")
    print("Average Precision: " + str((AVG_precision / 3) * 100) + "%")
    print("Average False Discovery Rate: " + str((AVG_falsedr / 3) * 100) + "%")
    print("Average False Omission Rate: " + str((AVG_falseor / 3) * 100) + "%")
