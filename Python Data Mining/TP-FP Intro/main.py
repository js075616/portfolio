# Calculates TP, FP, TP - FP and the top 10 features by TP - FP.
# Also creates a small decision tree that sorts samples by a given feature and creates a confusion matrix of the feature
# Written by Jake Schwarz
import pandas as pd
from tabulate import tabulate

pure_csv = pd.read_csv("mutations.csv")  # Read in the csv file as a DataFrame
# print(pure_csv)

# Initialize all arrays for storing values
TP = [0 for i in range(1411)]
FP = [0 for i in range(1411)]
TP_Minus_FP = [0 for i in range(1411)]
Gene_Names = [0 for i in range(1411)]  # Extra array to store gene names to match removal of max values later

# Loop through the columns and calculate TP and FP for each feature
for column in range(1, 1410):
    for row in range(0, 56):
        TP[column] += pure_csv.iloc[row, column]
    for row2 in range(56, 162):
        FP[column] += pure_csv.iloc[row2, column]

# Calculate TP-FP for each gene
for i in range(0, 1141):
    TP_Minus_FP[i] = TP[i] - FP[i]
    Gene_Names[i] = pure_csv.columns[i]

max_value = max(TP_Minus_FP)  # Find the max value in the array
max_index = TP_Minus_FP.index(max_value)  # Find the index value (column) of the max value
total_max_index = max_index  # 107 for DOCK3, sets a global max for the confusion matrix at the end
# print("Max value in TP - FP is " + str(max_value) + " with an index of " + str(max_index))
table = [["Mutation", "TP - FP"], [pure_csv.columns[max_index], max_value]]  # Creating the table with first entry
TP_Minus_FP.pop(max_index)  # Remove max value to find next max
Gene_Names.pop(max_index)  # Remove the name from the list

# Append the next nine rows to the table. Similar to above but in a loop
for i in range(0, 9):
    max_value = max(TP_Minus_FP)
    max_index = TP_Minus_FP.index(max_value)
    # print("Max value in TP - FP is " + str(max_value) + " with an index of " + str(max_index))
    # print(pure_csv.columns[max_index])
    table.append([Gene_Names[max_index], max_value])
    TP_Minus_FP.pop(max_index)
    Gene_Names.pop(max_index)
print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))  # Print the table

# Used to find the samples that have the feature and a confusion matrix of the feature
A_entries = []  # Samples in Group A
B_entries = []  # Samples in Group B
total_max_index = 107
for i in range(0, 162):
    if pure_csv.iloc[i, total_max_index] == 1:
        A_entries.append(pure_csv.iloc[i,0])
    else:
        B_entries.append(pure_csv.iloc[i,0])
print("")
print("Group A Samples: " + ", ".join(A_entries))
print("Group B Samples: " + ", ".join(B_entries))

# Calculate TP, FP, TN, and FN for the best feature
TP = 0
FP = 0
TN = 0
FN = 0
for row in range(0, 56):
    TP += pure_csv.iloc[row, total_max_index]
for row2 in range(56, 162):
    FP += pure_csv.iloc[row2, total_max_index]
FN = 56 - TP
TN = 106 - FP
print("")

# Print the confusion matrix
print("Confusion Matrix for " + pure_csv.columns[total_max_index])
print("                 Predicted")
print("                 C      NC")
print("Actual    C     " + str(TP) + "      " + str(FN))
print("         NC      " + str(FP) + "     " + str(TN))


