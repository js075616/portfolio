# This program creates lists F2-F5 of mutations that can be used to to create association rules.
# It removes permutations from the lists based on given thresholds for support and confidence.
# It displays the reduced lists as tables sorted by support x confidence.
# Written by Jake Schwarz

import pandas as pd
import numpy as np
from tabulate import tabulate
import itertools
from itertools import combinations_with_replacement
from operator import itemgetter


# Read in the csv as F1 and initilize variables
pure_csv = pd.read_csv("F1_mutations_only_c.csv")
# pure_csv = pd.read_csv("F1_mutations.csv")
number_of_rows = pure_csv.shape[0]


def apriori_pairs(min_support, min_confidence):
    final_pairs = []
    feature_count = {}
    f2_columns = []
    f2_dict = {}
    for c_name in pure_csv.columns[1:len(pure_csv.columns)]:
        count = 0
        for row in range(0, number_of_rows):
            if pure_csv[c_name][row] == 1:
                count += 1
        feature_count[c_name] = count
    columns_set = set(pure_csv.columns[1:len(pure_csv.columns)])

    for i in range(1, 3):
        c2 = list(itertools.permutations(columns_set, i))

    final = 0
    for index, combo in enumerate(list(c2)):
        count = 0
        for row in range(0, number_of_rows):
            if pure_csv[combo[0]][row] == 1 and pure_csv[combo[1]][row] == 1:
                count += 1
        if count > 3:
            f2_dict[combo[0] + ", " + combo[1]] = count
            sup = count / number_of_rows
            con = count / (feature_count[combo[0]] + 0.000000000001)
            if combo[0] not in f2_columns:
                f2_columns.append(combo[0])
            if combo[1] not in f2_columns:
                f2_columns.append(combo[1])
            if sup >= min_support or con >= min_confidence:
                final += 1
                final_pairs.append([combo[0], combo[1], count, sup, con, sup * con])

    threshold = sorted(final_pairs, key=itemgetter(5), reverse=True)
    table = [["A", "B", "Count", "Sup", "Con", "Sup * Con"]]
    print("Association Rules for " + str(2) + " size combinations with support > 7.2% or confidence > 75%")
    for item in threshold:
        table.append([item[0][:15], item[1][:15], item[2], str(round(float(item[3]) * 100, 3)), str(round(float(item[4]) * 100, 3)), str(round(float(item[5]) * 100, 3))])
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid', numalign="right"))
    print("Number of Association Rules: " + str(final))
    print("")
    return f2_columns, f2_dict


def apriori_triples(f2_columns, f2_dict, min_support, min_confidence):
    final_triples = []
    f3_columns = []
    f3_dict = {}
    columns_set = set(f2_columns)

    for i in range(1, 4):
        c3 = list(itertools.permutations(columns_set, i))

    final = 0
    for index, combo in enumerate(list(c3)):
        count = 0
        for row in range(0, number_of_rows):
            if pure_csv[combo[0]][row] == 1 and pure_csv[combo[1]][row] == 1 and pure_csv[combo[2]][row] == 1:
                count += 1
        if combo[0] + ", " + combo[1] in f2_dict and combo[0] + ", " + combo[2] in f2_dict and combo[1] + ", " + combo[2] in f2_dict:
            if count > 3:
                f3_dict[combo[0] + ", " + combo[1] + ", " + combo[2]] = count
            sup = count / number_of_rows
            con = count / (f2_dict[combo[0] + ", " + combo[1]] + 0.000000000001)
            if combo[0] not in f3_columns:
                f3_columns.append(combo[0])
            if combo[1] not in f3_columns:
                f3_columns.append(combo[1])
            if combo[2] not in f3_columns:
                f3_columns.append(combo[2])
            if sup >= min_support or con >= min_confidence:
                final += 1
                final_triples.append([combo[0], combo[1], combo[2], count, sup, con, sup * con])

    threshold = sorted(final_triples, key=itemgetter(6), reverse=True)
    table = [["A", "B", "C", "Count", "Sup", "Con", "Sup * Con"]]
    print("Association Rules for " + str(3) + " size combinations with support > 7.2% or confidence > 75%")
    for item in threshold:
        table.append([item[0][:15], item[1][:15], item[2][:15], item[3], str(round(float(item[4]) * 100, 3)), str(round(float(item[5]) * 100, 3)), str(round(float(item[6]) * 100, 3))])
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid', numalign="right"))
    print("Number of Association Rules: " + str(final))
    print("")
    return f3_columns, f3_dict


def apriori_quads(f3_columns, f3_dict, min_support, min_confidence):
    final_quads = []
    f4_columns = []
    f4_dict = {}
    columns_set = set(f3_columns)

    for i in range(1, 5):
        c4 = list(itertools.permutations(columns_set, i))

    # for c in c4:
    #     print(c)

    final = 0
    for index, combo in enumerate(list(c4)):
        count = 0
        for row in range(0, number_of_rows):
            if pure_csv[combo[0]][row] == 1 and pure_csv[combo[1]][row] == 1 and pure_csv[combo[2]][row] == 1 and pure_csv[combo[3]][row] == 1:
                count += 1
        if combo[0] + ", " + combo[1] + ", " + combo[2] in f3_dict and combo[0] + ", " + combo[1] + ", " + combo[3] in f3_dict and combo[1] + ", " + combo[2] + ", " + combo[3] in f3_dict:
            if count > 2:
                f4_dict[combo[0] + ", " + combo[1] + ", " + combo[2] + ", " + combo[3]] = count
            sup = count / number_of_rows
            con = count / (f3_dict[combo[0] + ", " + combo[1] + ", " + combo[2]] + 0.000000000001)
            if combo[0] not in f4_columns:
                f4_columns.append(combo[0])
            if combo[1] not in f4_columns:
                f4_columns.append(combo[1])
            if combo[2] not in f4_columns:
                f4_columns.append(combo[2])
            if combo[3] not in f4_columns:
                f4_columns.append(combo[3])
            if sup >= min_support or con >= min_confidence:
                final += 1
                final_quads.append([combo[0], combo[1], combo[2], combo[3], count, sup, con, sup * con])

    threshold = sorted(final_quads, key=itemgetter(7), reverse=True)
    table = [["A", "B", "C", "D", "Count", "Sup", "Con", "Sup * Con"]]
    print("Association Rules for " + str(4) + " size combinations with support > 0% or confidence > 0%")
    for item in threshold:
        table.append([item[0][:15], item[1][:15], item[2][:15], item[3][:15], item[4], str(round(float(item[5]) * 100, 3)), str(round(float(item[6]) * 100, 3)), str(round(float(item[7]) * 100, 3))])
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid', numalign="right"))
    print("Number of Association Rules: " + str(final))
    print("")
    return f4_columns, f4_dict


def apriori_quins(f4_columns, f4_dict, min_support, min_confidence):
    final_quins = []
    f5_columns = []
    f5_dict = {}
    columns_set = set(f4_columns)
    # print(columns_set)

    for i in range(1, 6):
        c5 = list(itertools.permutations(columns_set, i))

    # for c in c5:
    #     print(c)
    #
    # print(str(len(c5)))
    final = 0
    for index, combo in enumerate(list(c5)):
        count = 0
        for row in range(0, number_of_rows):
            if pure_csv[combo[0]][row] == 1 and pure_csv[combo[1]][row] == 1 and pure_csv[combo[2]][row] == 1 and pure_csv[combo[3]][row] == 1 and pure_csv[combo[4]][row] == 1:
                count += 1
        if combo[0] + ", " + combo[1] + ", " + combo[2] + ", " + combo[3] in f4_dict and combo[0] + ", " + combo[1] + ", " + combo[2] + ", " + combo[4] in f4_dict and combo[1] + ", " + combo[2] + ", " + combo[3] + ", " + combo[4] in f4_dict:
            if count > 3:
                f5_dict[combo[0] + ", " + combo[1] + ", " + combo[2] + ", " + combo[3] + ", " + combo[4]] = count
            sup = count / number_of_rows
            con = count / (f4_dict[combo[0] + ", " + combo[1] + ", " + combo[2] + ", " + combo[3]] + 0.000000000001)
            if combo[0] not in f5_columns:
                f5_columns.append(combo[0])
            if combo[1] not in f5_columns:
                f5_columns.append(combo[1])
            if combo[2] not in f5_columns:
                f5_columns.append(combo[2])
            if combo[3] not in f5_columns:
                f5_columns.append(combo[3])
            if combo[4] not in f5_columns:
                f5_columns.append(combo[3])
            if sup >= min_support or con >= min_confidence:
                final += 1
                final_quins.append([combo[0], combo[1], combo[2], combo[3], combo[4], count, sup, con, sup * con])

    threshold = sorted(final_quins, key=itemgetter(8), reverse=True)
    table = [["A", "B", "C", "D", "E", "Count", "Sup", "Con", "Sup * Con"]]
    print("Association Rules for " + str(5) + " size combinations with support > 0% or confidence > 0%")
    for item in threshold:
        table.append([item[0][:15], item[1][:15], item[2][:15], item[3][:15], item[4][:15], item[5], str(round(float(item[6]) * 100, 3)), str(round(float(item[7]) * 100, 3)), str(round(float(item[8]) * 100, 3))])
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid', numalign="right"))
    print("Number of Association Rules: " + str(final))
    print("")
    return f5_columns, f5_dict


result = apriori_pairs(0.072, .75)
print("Mutations from F2:")
print(result[0])
print("Number of Distinct Mutations in F2: " + str(len(result[0])))
print("")
print("All pairs in F2 that occur at least 4 times:")
for key, value in result[1].items():
    print(key + ": " + str(value))
print("")
print("Number of Pairs: " + str(len(result[1])))
print("")

result2 = apriori_triples(result[0], result[1], 0.072, 0.75)
print("Mutations from F3:")
print(result2[0])
print("Number of Distinct Mutations in F3: " + str(len(result2[0])))
print("")
print("All triples in F3 that occur at least 4 times:")
for key, value in result2[1].items():
    print(key + ": " + str(value))
print("")
print("Number of Triples: " + str(len(result2[1])))
print("")

result3 = apriori_quads(result2[0], result2[1], 0, 0)
print("Mutations from F4:")
print(result3[0])
print("Number of Distinct Mutations in F4: " + str(len(result3[0])))
print("")
print("All quads in F4 that occur at least 1 time:")
for key, value in result3[1].items():
    print(key + ": " + str(value))
print("")
print("Number of Quads: " + str(len(result3[1])))
print("")

result4 = apriori_quins(result3[0], result3[1], 0, 0)
print("Mutations from F5:")
print(result4[0])
print("Number of Distinct Mutations in F5: " + str(len(result4[0])))
print("")
print("All quintuples in F5 that occur:")
for key, value in result4[1].items():
    print(key + ": " + str(value))
print("")
print("Number of Quintuples: " + str(len(result4[1])))
