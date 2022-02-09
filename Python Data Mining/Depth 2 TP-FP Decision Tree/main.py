# Calculates TP, FP, TP - FP and the top 10 features by TP - FP.
# Also creates a small decision tree that sorts samples by a given feature and creates a confusion matrix of the feature
# Written by Jake Schwarz
import sys

import pandas as pd
from matrix import *
from table import *

pure_csv = pd.read_csv("mutations.csv")
# print(pure_csv)
# total_max_index = top_ten_table(pure_csv)
# create_matrix(pure_csv, total_max_index)

# Used to find the samples that have the feature and a confusion matrix of the feature
Group_A = df = pd.DataFrame(columns = pure_csv.columns)  # Samples that do have the mutation
Group_B = df = pd.DataFrame(columns = pure_csv.columns)  # Samples that do not have the mutation
Group_A1 = df = pd.DataFrame(columns = pure_csv.columns)
Group_A2 = df = pd.DataFrame(columns = pure_csv.columns)
Group_B1 = df = pd.DataFrame(columns = pure_csv.columns)
Group_B2 = df = pd.DataFrame(columns = pure_csv.columns)
A_entries = []
B_entries = []
A1_entries = []
A2_entries = []
B1_entries = []
B2_entries = []
# print(Group_A)
# print(Group_B)
total_max_index = 107
for i in range(0, 162):
    if pure_csv.iloc[i, total_max_index] == 1:
        A_entries.append(pure_csv.loc[[i]])
    else:
        B_entries.append(pure_csv.loc[[i]])
# print(A_entries)
# print(B_entries)
Group_A = pd.concat(A_entries)
Group_B = pd.concat(B_entries)
# print(Group_A)
# print(Group_B)
# print("Group A Samples: " + ", ".join(Group_A))
# print("Group B Samples: " + ", ".join(Group_B))
print("Group A most useful features: ")
total_max_index = top_ten_table(Group_A)
create_matrix(Group_A, total_max_index)
number_of_rows = Group_A.shape[0]
for i in range(0, number_of_rows):
    # print(Group_A.iloc[i, total_max_index])
    # print(Group_A.iloc[[i]])
    if Group_A.iloc[i, total_max_index] == 1:
        A1_entries.append(Group_A.iloc[[i]])
    else:
        A2_entries.append(Group_A.iloc[[i]])
if A1_entries:
    Group_A1 = pd.concat(A1_entries)
if A2_entries:
    Group_A2 = pd.concat(A2_entries)
print("Group A1 C Samples: ")
for i in range(0, len(A1_entries)):
    sys.stdout.write(str(Group_A1.iloc[i, 0]) + ", ")
print("")
print("Group A2 NC Samples: ")
for i in range(0, len(A2_entries)):
    sys.stdout.write(str(Group_A2.iloc[i, 0]) + ", ")
print("")

print("Group B most useful features: ")
total_max_index = top_ten_table(Group_B)
create_matrix(Group_B, total_max_index)
number_of_rows = Group_B.shape[0]
for i in range(0, number_of_rows):
    if Group_B.iloc[i, total_max_index] == 1:
        B1_entries.append(Group_B.iloc[[i]])
    else:
        B2_entries.append(Group_B.iloc[[i]])
if B1_entries:
    Group_B1 = pd.concat(B1_entries)
if B2_entries:
    Group_B2 = pd.concat(B2_entries)
print("Group B1 C Samples: ")
for i in range(0, len(B1_entries)):
    sys.stdout.write(str(Group_B1.iloc[i, 0]) + ", ")
print("")
print("Group B2 NC Samples: ")
for i in range(0, len(B2_entries)):
    sys.stdout.write(str(Group_B2.iloc[i, 0]) + ", ")



