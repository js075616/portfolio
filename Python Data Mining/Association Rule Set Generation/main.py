# This program creates lists F2 and F3 which are association rules based on the list F1 passed in as a csv.
# It removes pairs and triplets from the lists based on given thresholds for support and confidence.
# It displays the reduced lists as tables sorted by support x confidence.
# Written by Jake Schwarz

import pandas as pd
from tabulate import tabulate
import itertools
from operator import itemgetter


# class Tuple:
#     def __init__(self, a, b, c):
#         self.a = a
#         self.b = b
#         self.c = c
#         self.support = None
#         self.confidence = None

# Read in the csv as F1 and initilize variables
pure_csv = pd.read_csv("F1_mutations.csv")
# print(pure_csv.columns.get_loc(pure_csv.columns[1]))
f2 = {}
final_f2 = {}
feature_count = {}
tuple_list = []

# Build F2 from F1 and add the pairs to a dictionary
for column_name in pure_csv.columns:
    for sec_column_name in pure_csv.columns[pure_csv.columns.get_loc(column_name)+1:]:
        for row in range(0, 162):
            if pure_csv[column_name][row] == 1 and pure_csv[sec_column_name][row] == 1:
                if column_name + ", " + sec_column_name not in f2:
                    f2[column_name + ", " + sec_column_name] = 1
                    f2[sec_column_name + ", " + column_name] = 1
                else:
                    f2[column_name + ", " + sec_column_name] = f2[column_name + ", " + sec_column_name] + 1
                    f2[sec_column_name + ", " + column_name] = f2[sec_column_name + ", " + column_name] + 1

# # Print F2
# for f in f2:
#     print(f + ": " + str(f2[f]))

# Create a list and a final version of the dictionary with only pairs that occur 4 or more times
for i in f2:
    if f2[i] > 3:
        final_f2[i] = f2[i]
        tmp = i.split(", ")
        tuple_list.append([tmp[0], tmp[1], f2[i], 0, 0, 0])
        count = 0
        for row in range(0, 162):
            if pure_csv[tmp[0]][row] == 1:
                count += 1
        feature_count[tmp[0]] = count
        # print(str(i) + ": " + str(f2[i]))

# Sort the list of tuples, remove duplicates, and calculate values
tuple_list.sort()
list_tuples = list(tuple_list for tuple_list, _ in itertools.groupby(tuple_list))
for tup in list_tuples:
    tup[3] = tup[2] / 162
    tup[4] = tup[2] / (feature_count[tup[0]] + 0.000000000001)
    tup[5] = tup[3] * tup[4]

# Remove pairs(tuples) that do not meet certain thresholds
final_tuples = []
for tup in list_tuples:
    if tup[3] >= 0.031 or tup[4] >= 0.50:
        final_tuples.append(tup)

# Print the table of combined pairs that meet either threshold, sorted by support x confidence
threshold = sorted(final_tuples, key=itemgetter(5), reverse=True)
print("Tuples")
table = [["A", "B", "Samples", "Sup", "Con", "Sup x Con"]]
for i in range(0, len(threshold)):
    table.append([threshold[i][0][:15], threshold[i][1][:15], threshold[i][2], threshold[i][3], threshold[i][4], threshold[i][5]])
print(tabulate(table, headers='firstrow', tablefmt='fancy_grid', numalign="right"))
print("")
print("Total number of pairs: " + str(len(final_tuples)))
print("")

# Create a list of triplet based on joining F2 with itself
c3 = []
for tuple_1 in tuple_list:
    for tuple_2 in tuple_list[tuple_list.index(tuple_1):]:
        if tuple_1[0] == tuple_2[0] or tuple_1[1] == tuple_2[0]:
            if tuple_1[0] != tuple_2[1] and tuple_1[1] != tuple_2[1]:
                c3.append([tuple_1[0], tuple_1[1], tuple_2[1]])
                # c3.append([tuple_1[0], tuple_2[1], tuple_1[1]])
                # c3.append([tuple_2[1], tuple_1[1], tuple_1[0]])
        elif tuple_1[0] == tuple_2[1] or tuple_1[1] == tuple_2[1]:
            if tuple_1[0] != tuple_2[0] and tuple_1[1] != tuple_2[0]:
                c3.append([tuple_1[0], tuple_1[1], tuple_2[0]])
                # c3.append([tuple_1[0], tuple_2[0], tuple_1[1]])
                # c3.append([tuple_2[0], tuple_1[1], tuple_1[0]])

# Remove duplicates from the list
c3.sort()
list_triplets = list(c3 for c3, _ in itertools.groupby(c3))

# Print the list of triples
# for triplet in final_triples:
#     print(triplet)

# Remove triplets that have a subset pair that occurs less than 3 times and calculate how many times that triplet occurs
f3 = []
# trips = 0
for triplet in list_triplets:
    first_pair = 0
    second_pair = 0
    third_pair = 0
    count = 0

    for row in range(0, 162):
        if pure_csv[triplet[0]][row] == 1 and pure_csv[triplet[1]][row] == 1:
            first_pair += 1
        if pure_csv[triplet[0]][row] == 1 and pure_csv[triplet[2]][row] == 1:
            second_pair += 1
        if pure_csv[triplet[1]][row] == 1 and pure_csv[triplet[2]][row] == 1:
            third_pair += 1
        if pure_csv[triplet[0]][row] == 1 and pure_csv[triplet[1]][row] == 1 and pure_csv[triplet[2]][row] == 1:
            count += 1

    if first_pair > 3 and second_pair > 3 and third_pair > 3:
        f3.append([triplet[0], triplet[1], triplet[2], count, 0, 0, 0])
        # trips += 1

# print("F3 Triplets: " + str(trips))

# Calculate values for the triplets
for triplet in f3:
    triplet[4] = triplet[3] / 162
    count = 0
    for row in range(0, 162):
        if pure_csv[triplet[0]][row] == 1 and pure_csv[triplet[1]][row] == 1:
            count += 1
    triplet[5] = triplet[3] / (count + 0.000000000001)
    triplet[6] = triplet[4] * triplet[5]

# Remove triplets that do not meet the certain thresholds
triplets = 0
final_triplets = []
for triplet in f3:
    # print(triplet)
    if triplet[4] >= 0.02 or triplet[5] >= 0.70:
        final_triplets.append(triplet)
        triplets += 1

# Print the remaining triplets in a table sorted by support x confidence
print("Triplets")
final = sorted(final_triplets, key=itemgetter(6), reverse=True)
table = [["A", "B", "C", "Samples", "Sup", "Con", "Sup x Con"]]
for i in range(0, len(final)):
    table.append([final[i][0][:15], final[i][1][:15], final[i][2][:15], final[i][3], final[i][4], final[i][5], final[i][6]])
print(tabulate(table, headers='firstrow', tablefmt='fancy_grid', numalign="right"))
print("")
print("Total number of triples: " + str(triplets))
