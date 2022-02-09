

import pandas as pd
from table import *
from matrix import *

TP = 0
TN = 0
FP = 0
FN = 0


class Node:
    def __init__(self, index, c):
        self.left = None
        self.right = None
        self.index = index
        self.c = c


def two_height_tree(passed_csv):
    group_a = df = pd.DataFrame(columns=passed_csv.columns)  # Samples that do have the mutation
    group_b = df = pd.DataFrame(columns=passed_csv.columns)
    a_entries = []
    b_entries = []
    total_max_index = calculate_max_index(passed_csv)
    # print(total_max_index)
    for i in range(0, 162):
        if passed_csv.iloc[i, total_max_index] == 1:
            a_entries.append(passed_csv.loc[[i]])
        else:
            b_entries.append(passed_csv.loc[[i]])
    # print(a_entries)
    # print(b_entries)
    group_a = pd.concat(a_entries)
    group_b = pd.concat(b_entries)
    root = Node(total_max_index, None)
    root.left = Node(calculate_max_index(group_a), None)
    # print(root.left.index)
    root.right = Node(calculate_max_index(group_b), None)
    # print(root.right.index)
    root.left.left = Node(None, "C")
    root.left.right = Node(None, "NC")
    root.right.left = Node(None, "C")
    root.right.right = Node(None, "NC")
    return root


def rigged_two_height_tree(passed_csv):
    root = Node(107, None)
    root.left = Node(107, None)
    root.right = Node(173, None)
    root.left.left = Node(None, "C")
    root.left.right = Node(None, "NC")
    root.right.left = Node(None, "C")
    root.right.right = Node(None, "NC")
    return root


def inorder(node):
    if node:
        inorder(node.left)
        print(node.index)
        inorder(node.right)


def evaluator(tree, row):
    global TP
    global TN
    global FP
    global FN
    if row.iloc[tree.index] == 1:
        tree = tree.left
    else:
        tree = tree.right
    if row.iloc[tree.index] == 1:
        tree = tree.left
    else:
        tree = tree.right
    # return tree.c

    if tree.c == "C":
        if row.iloc[0][0] == "C":
            TP += 1
        else:
            FP += 1
    elif tree.c == "NC":
        if row.iloc[0][0] == "N":
            TN += 1
        else:
            FN += 1

    return tree.c


def print_eval():
    # print("TP: " + str(TP))
    # print("FP: " + str(FP))
    # print("TN: " + str(TN))
    # print("FN: " + str(FN))
    print("Metrics for Decision Tree")
    accuracy = (TP + TN) / 162
    sensitivity = TP / (TP + FN)
    specificity = TN / (TN + FP)
    precision = TP / (TP + FP)
    miss_rate = FN / (FN + TP)
    falsedr = FP / (FP + TP)
    falseor = FN / (FN + TN)
    print("Accuracy: " + str(accuracy * 100) + "%")
    print("Sensitivity: " + str(sensitivity * 100) + "%")
    print("Specificity: " + str(specificity * 100) + "%")
    print("Precision: " + str(precision * 100) + "%")
    print("Miss Rate: " + str(miss_rate * 100) + "%")
    print("False Discovery Rate: " + str(falsedr * 100) + "%")
    print("False Omission Rate: " + str(falseor* 100) + "%")
    print("")
    print_matrix_eval(TP, TN, FP, FN)

