# Calculates TP, FP, TP - FP and the top 10 features by TP - FP.
# Also creates a small decision tree that sorts samples by a given feature and creates a confusion matrix of the feature.
# This system is then tested through 3-fold cross validation.
# Written by Jake Schwarz
import sys

import pandas as pd
from tree import *


pure_csv = pd.read_csv("mutations.csv")
subset1 = pure_csv.sample(n=54)
working_df = pure_csv[~pure_csv.Samples.isin(subset1.Samples)]
subset2 = working_df.sample(n=54)
subset3 = working_df[~working_df.Samples.isin(subset2.Samples)]
# print(subset1)
# print(subset2)
# print(subset3)
# print(pd.concat([subset1, subset2], ignore_index=True))
# print(random_df)
combined_df = pd.concat([subset1, subset2], ignore_index=True)
root = two_height_tree(combined_df)
# print(pure_csv[~pure_csv.Samples.isin(random_df.Samples)])
# number_of_rows = combined_df.shape[0]
# print(random_df)
# print(pure_csv)
for i in range(0, 54):
    # print(pure_csv.iloc[i][0])
    # print(evaluator(root, pure_csv.iloc[i]))
    evaluator(root, subset3.iloc[i])
print_eval()
reset_eval()

combined_df = pd.concat([subset1, subset3], ignore_index=True)
root = two_height_tree(combined_df)
for i in range(0, 54):
    evaluator(root, subset2.iloc[i])
print_eval()
reset_eval()

combined_df = pd.concat([subset2, subset3], ignore_index=True)
root = two_height_tree(combined_df)
for i in range(0, 54):
    evaluator(root, subset1.iloc[i])
print_eval()
reset_eval()

print_avg()
