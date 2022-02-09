# Creates a decision tree based on entropy and evaluates it. Also tests the functions with 3-fold cross validation.
# Written by Jake Schwarz
import sys

import pandas as pd
from tree import *


pure_csv = pd.read_csv("mutations.csv")
# gains_table(pure_csv)
# two_height_tree_phi(pure_csv)
rs = 2
subset1 = pure_csv.sample(n=54, ignore_index=True, random_state=rs)
working_df = pure_csv[~pure_csv.Samples.isin(subset1.Samples)]
subset2 = working_df.sample(n=54, ignore_index=True, random_state=rs)
working_df = working_df[~working_df.Samples.isin(subset2.Samples)]
subset3 = working_df.sample(n=54, ignore_index=True, random_state=rs)
# print(gains_table(subset3))
# print("All Samples Tree")
# root = two_height_tree_gains(pure_csv)
# for i in range(0, 162):
#     evaluator(root, pure_csv.iloc[i])
# print_eval()
# reset_eval()
# reset_averages()

combined_df = pd.concat([subset1, subset2], ignore_index=True)
print("Subset 1 + Subset 2 Tree")
root = two_height_tree_gains(combined_df)
number_of_rows = combined_df.shape[0]
for i in range(0, 54):
    evaluator(root, subset3.iloc[i])
print_eval()
reset_eval()

combined_df = pd.concat([subset1, subset3], ignore_index=True)
print("Subset 1 + Subset 3 Tree")
root = two_height_tree_gains(combined_df)
for i in range(0, 54):
    evaluator(root, subset2.iloc[i])
print_eval()
reset_eval()

combined_df = pd.concat([subset2, subset3], ignore_index=True)
print("Subset 2 + Subset 3 Tree")
root = two_height_tree_gains(combined_df)
for i in range(0, 54):
    evaluator(root, subset1.iloc[i])
print_eval()
reset_eval()

print_avg()
