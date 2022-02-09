# Calculates the information gain (entropy) of each feature and displays the best features in a table.
# Written by Jake Schwarz
import sys

import pandas as pd
from tree import *


pure_csv = pd.read_csv("mutations.csv")
gains_table(pure_csv)
# two_height_tree_phi(pure_csv)
# subset1 = pure_csv.sample(n=54)
# working_df = pure_csv[~pure_csv.Samples.isin(subset1.Samples)]
# subset2 = working_df.sample(n=54)
# subset3 = working_df[~working_df.Samples.isin(subset2.Samples)]
# root = two_height_tree_phi(pure_csv)
# for i in range(0, 162):
#     evaluator(root, pure_csv.iloc[i])
# print_eval()
# reset_eval()
# reset_averages()
#
# combined_df = pd.concat([subset1, subset2], ignore_index=True)
# root = two_height_tree_phi(combined_df)
# print(pure_csv[~pure_csv.Samples.isin(random_df.Samples)])
# number_of_rows = combined_df.shape[0]
# print(random_df)
# print(pure_csv)
# for i in range(0, 54):
#     # print(pure_csv.iloc[i][0])
#     # print(evaluator(root, pure_csv.iloc[i]))
#     evaluator(root, subset3.iloc[i])
# print_eval()
# reset_eval()
#
# combined_df = pd.concat([subset1, subset3], ignore_index=True)
# root = two_height_tree_phi(combined_df)
# for i in range(0, 54):
#     evaluator(root, subset2.iloc[i])
# print_eval()
# reset_eval()
#
# combined_df = pd.concat([subset2, subset3], ignore_index=True)
# root = two_height_tree_phi(combined_df)
# for i in range(0, 54):
#     evaluator(root, subset1.iloc[i])
# print_eval()
# reset_eval()
#
# print_avg()
