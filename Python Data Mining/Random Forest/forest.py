from tree import *
import pandas as pd
from table import *


FOREST = []
OOB_SIZES = []
OOOB = pd.DataFrame
F_TP = 0
F_TN = 0
F_FP = 0
F_FN = 0
AVG_F_TP = 0
AVG_F_TN = 0
AVG_F_FP = 0
AVG_F_FN = 0
AVG_F_accuracy = 0
AVG_F_sensitivity = 0
AVG_F_miss_rate = 0
AVG_F_specificity = 0
AVG_F_precision = 0
AVG_F_falsedr = 0
AVG_F_falseor = 0


def random_tree(passed_csv, display_info, func):
    num_samples = passed_csv.shape[0]
    # print(num_samples)
    bootstrap = passed_csv.sample(n=num_samples, ignore_index=True, replace=True)
    out_of_bag = passed_csv[~passed_csv.Samples.isin(bootstrap.Samples)]
    bootstrap_less = bootstrap[['Samples']].copy()
    new_columns = bootstrap.loc[:, bootstrap.columns != 'Samples'].sample(n=20, ignore_index=True, axis="columns")
    bootstrap_less = pd.concat([bootstrap_less, new_columns], axis=1)
    if func == "phi":
        root = two_height_tree_phi(bootstrap_less)
    elif func == "gains":
        root = two_height_tree_gains(bootstrap_less)
    if display_info:
        global OOOB
        OOOB = out_of_bag
        print("First Tree Root: " + str(passed_csv.columns[root.index]))
        if passed_csv.columns[root.left.index] == "Samples":
            print("First Tree Left: No Split")
        else:
            print("First Tree Left: " + str(passed_csv.columns[root.left.index]))
        if passed_csv.columns[root.right.index] == "Samples":
            print("First Tree Right: No Split")
        else:
            print("First Tree Right: " + str(passed_csv.columns[root.right.index]))

        print("Number of Out-of-bag Samples for First Tree: " + str(len(list(out_of_bag['Samples']))))
        print("Out-of-bag Samples for First Tree: " + str(list(out_of_bag['Samples'])))
        print("")
    else:
        global OOB_SIZES
        OOB_SIZES.append(len(list(out_of_bag['Samples'])))
    return root


def create_forest(passed_csv, number_of_trees, func):
    global FOREST
    for num in range(0, number_of_trees):
        root = random_tree(passed_csv, 0, func)
        FOREST.append(root)


def print_oob():
    global OOB_SIZES
    average = 0
    print("Out-Of-Bag Sizes: " + str(sorted(OOB_SIZES)))
    for i in OOB_SIZES:
        average += i
    print("Average Out-Of-Bag Size: " + str(average/len(OOB_SIZES)))
    print("")


def forest_classifer(sample, display_info):
    global FOREST
    c = 0
    nc = 0
    final_cls = ""
    for tree in FOREST:
        cls = evaluator_noavg(tree, sample)
        if cls == "C":
            c += 1
        else:
            nc += 1

    if display_info:
        print("Trees with C: " + str(c))
        print("Trees with NC: " + str(nc))

    global F_TP
    global F_TN
    global F_FP
    global F_FN
    global AVG_F_TP
    global AVG_F_TN
    global AVG_F_FP
    global AVG_F_FN

    if c > nc:
        final_cls = "C"
    else:
        final_cls = "NC"

    if final_cls == "C":
        if sample.iloc[0][0] == "C":
            F_TP += 1
            AVG_F_TP += 1
        else:
            F_FP += 1
            AVG_F_FP += 1
    elif final_cls == "NC":
        if sample.iloc[0][0] == "N":
            F_TN += 1
            AVG_F_TN += 1
        else:
            F_FN += 1
            AVG_F_FN += 1

    return final_cls


def oob_classify():
    global OOOB
    reset_eval_forest()
    num_of_rows = OOOB.shape[0]
    for row in range(0, num_of_rows):
        forest_classifer(OOOB.iloc[row], 0)
    print_eval_forest_oob()


def df_classify(passed_csv):
    reset_eval_forest()
    num_of_rows = passed_csv.shape[0]
    for row in range(0, num_of_rows):
        forest_classifer(passed_csv.iloc[row], 0)
    calc_avg_forest()


def print_eval_forest_oob():
    global F_FP
    global F_TN
    global F_FN
    global F_FP
    global AVG_F_accuracy
    global AVG_F_sensitivity
    global AVG_F_miss_rate
    global AVG_F_specificity
    global AVG_F_precision
    global AVG_F_falsedr
    global AVG_F_falseor
    print("Metrics for Out-of-Bag")
    print("TP: " + str(F_TP))
    print("TN: " + str(F_TN))
    print("FN: " + str(F_FN))
    print("FP: " + str(F_FP))

    accuracy = (F_TP + F_TN) / (F_TP + F_TN + F_FN + F_FP + 0.00000000001)
    sensitivity = F_TP / (F_TP + F_FN + 0.00000000001)
    miss_rate = F_FN / (F_FN + F_TP + 0.00000000001)
    specificity = F_TN / (F_TN + F_FP + 0.00000000001)
    precision = F_TP / (F_TP + F_FP + 0.00000000001)
    falsedr = F_FP / (F_FP + F_TP + 0.00000000001)
    falseor = F_FN / (F_FN + F_TN + 0.00000000001)

    print("Accuracy: " + str(round(accuracy * 100, 3)) + "%")
    print("Sensitivity: " + str(round(sensitivity * 100, 3)) + "%")
    print("Specificity: " + str(round(specificity* 100, 3)) + "%")
    print("Miss Rate: " + str(round(miss_rate * 100, 3)) + "%")
    print("Precision: " + str(round(precision * 100, 3)) + "%")
    print("False Discovery Rate: " + str(round(falsedr * 100, 3)) + "%")
    print("False Omission Rate: " + str(round(falseor * 100, 3)) + "%")
    print("")
    # print_matrix_eval(F_TP, F_TN, F_FP, F_FN, ROOT_NAME)


def calc_avg_forest():
    global F_FP
    global F_TN
    global F_FN
    global F_FP
    global AVG_F_accuracy
    global AVG_F_sensitivity
    global AVG_F_miss_rate
    global AVG_F_specificity
    global AVG_F_precision
    global AVG_F_falsedr
    global AVG_F_falseor

    print("TP: " + str(F_TP))
    print("TN: " + str(F_TN))
    print("FN: " + str(F_FN))
    print("FP: " + str(F_FP))

    accuracy = (F_TP + F_TN) / (F_TP + F_TN + F_FN + F_FP + 0.00000000001)
    sensitivity = F_TP / (F_TP + F_FN + 0.00000000001)
    miss_rate = F_FN / (F_FN + F_TP + 0.00000000001)
    specificity = F_TN / (F_TN + F_FP + 0.00000000001)
    precision = F_TP / (F_TP + F_FP + 0.00000000001)
    falsedr = F_FP / (F_FP + F_TP + 0.00000000001)
    falseor = F_FN / (F_FN + F_TN + 0.00000000001)
    AVG_F_accuracy += accuracy
    AVG_F_sensitivity += sensitivity
    AVG_F_miss_rate += miss_rate
    AVG_F_specificity += specificity
    AVG_F_precision += precision
    AVG_F_falsedr += falsedr
    AVG_F_falseor += falseor

    print("Accuracy: " + str(round(accuracy * 100, 3)) + "%")
    print("Sensitivity: " + str(round(sensitivity * 100, 3)) + "%")
    print("Specificity: " + str(round(specificity * 100, 3)) + "%")
    print("Miss Rate: " + str(round(miss_rate * 100, 3)) + "%")
    print("Precision: " + str(round(precision * 100, 3)) + "%")
    print("False Discovery Rate: " + str(round(falsedr * 100, 3)) + "%")
    print("False Omission Rate: " + str(round(falseor * 100, 3)) + "%")
    print("")
    reset_eval_forest()
    # print_matrix_eval(F_TP, F_TN, F_FP, F_FN, ROOT_NAME)


def reset_eval_forest():
    global F_TP
    global F_TN
    global F_FP
    global F_FN
    F_TP = 0
    F_TN = 0
    F_FP = 0
    F_FN = 0


def print_forest_avg():
    print("Averages:")
    print("Average Accuracy: " + str(round((AVG_F_accuracy / 3) * 100, 3)) + "%")
    print("Average Sensitivity: " + str(round((AVG_F_sensitivity / 3) * 100, 3)) + "%")
    print("Average Miss Rate: " + str(round((AVG_F_miss_rate / 3) * 100, 3)) + "%")
    print("Average Specificity: " + str(round((AVG_F_specificity / 3) * 100, 3)) + "%")
    print("Average Precision: " + str(round((AVG_F_precision / 3) * 100, 3)) + "%")
    print("Average False Discovery Rate: " + str(round((AVG_F_falsedr / 3) * 100, 3)) + "%")
    print("Average False Omission Rate: " + str(round((AVG_F_falseor / 3) * 100, 3)) + "%")
