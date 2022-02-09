# Creats a random forest based on entropy and uses it to test specific samples.
# Written by Jake Schwarz
import sys

import pandas as pd
from tree import *
from forest import *


# pure_csv = pd.read_csv("rem_samp_feat_mutations.csv")
pure_csv = pd.read_csv("rem_feat_mutations.csv")
# pure_csv = pd.read_csv("mutations.csv")

# i = 0
# current_count = 0
# for column_name in pure_csv.columns:
#     if i != 0:
#         for row in range(0, pure_csv.shape[0]):
#             if pure_csv[column_name][row] == 1:
#                 current_count += 1
#         if current_count < 4:
#             pure_csv.drop(column_name, axis=1, inplace=True)
#         current_count = 0
#     i += 1
# i = 0
# current_count = 0
# for row in range(0, pure_csv.shape[0]):
#     if i != 0:
#         for column_name in pure_csv.columns:
#             if pure_csv[column_name][row] == 1:
#                 current_count += 1
#         if current_count < 4 and pure_csv["Samples"][0][0] == 'C':
#             pure_csv.drop(row, inplace=True)
#         elif current_count > 4 and pure_csv["Samples"][0][0] == 'N':
#             pure_csv.drop(row, inplace=True)
#         current_count = 0
#     i += 1
# pure_csv.to_csv("updated_updated_mutations.csv", index=False)

random_tree(pure_csv, True, "gains")
reset_nodes()
create_forest(pure_csv, 101, "gains")
print_oob()
print_nodes()
print(pure_csv.iloc[0][0])
print("Final: " + forest_classifer(pure_csv.iloc[0], 1))
print(pure_csv.iloc[9][0])
print("Final: " + forest_classifer(pure_csv.iloc[9], 1))
print(pure_csv.iloc[155][0])
print("Final: " + forest_classifer(pure_csv.iloc[155], 1))
print(pure_csv.iloc[60][0])
print("Final: " + forest_classifer(pure_csv.iloc[60], 1))
print(pure_csv.iloc[70][0])
print("Final: " + forest_classifer(pure_csv.iloc[70], 1))
print("")
oob_classify()

# rs = 2
# sample_num = int(pure_csv.shape[0] / 3)
# subset1 = pure_csv.sample(n=sample_num, ignore_index=True, random_state=rs)
# working_df = pure_csv[~pure_csv.Samples.isin(subset1.Samples)]
# subset2 = working_df.sample(n=sample_num, ignore_index=True, random_state=rs)
# working_df = working_df[~working_df.Samples.isin(subset2.Samples)]
# subset3 = working_df.sample(n=sample_num, ignore_index=True, random_state=rs)

# sample_num = int(pure_csv.shape[0] / 3)
# subset1 = pure_csv.sample(n=sample_num, ignore_index=True)
# working_df = pure_csv[~pure_csv.Samples.isin(subset1.Samples)]
# subset2 = working_df.sample(n=sample_num, ignore_index=True)
# working_df = working_df[~working_df.Samples.isin(subset2.Samples)]
# subset3 = working_df.sample(n=sample_num, ignore_index=True)
#
# num_trees = 51
# func = "gains"
# combined_df = pd.concat([subset1, subset2], ignore_index=True)
# print("Subset 1 + Subset 2 Forest")
# create_forest(combined_df, num_trees, func)
# print_nodes()
# df_classify(subset3)
#
# combined_df = pd.concat([subset1, subset3], ignore_index=True)
# print("Subset 1 + Subset 3 Forest")
# create_forest(combined_df, num_trees, func)
# print_nodes()
# df_classify(subset2)
#
# combined_df = pd.concat([subset2, subset3], ignore_index=True)
# print("Subset 2 + Subset 3 Forest")
# create_forest(combined_df, num_trees, func)
# print_nodes()
# df_classify(subset1)
#
# print_forest_avg()


# rs = 2
# subset1 = pure_csv.sample(n=54, ignore_index=True, random_state=rs)
# working_df = pure_csv[~pure_csv.Samples.isin(subset1.Samples)]
# subset2 = working_df.sample(n=54, ignore_index=True, random_state=rs)
# working_df = working_df[~working_df.Samples.isin(subset2.Samples)]
# subset3 = working_df.sample(n=54, ignore_index=True, random_state=rs)
# print(gains_table(subset3))
# print("All Samples Tree")
# root = two_height_tree_gains(pure_csv)
# for i in range(0, 162):
#     evaluator(root, pure_csv.iloc[i])
# print_eval()
# reset_eval()
# reset_averages()

# combined_df = pd.concat([subset1, subset2], ignore_index=True)
# print("Subset 1 + Subset 2 Forest")
# root = two_height_tree_gains(combined_df)
# number_of_rows = combined_df.shape[0]
# for i in range(0, 54):
#     evaluator(root, subset3.iloc[i])
# print_eval()
# reset_eval()

# combined_df = pd.concat([subset1, subset3], ignore_index=True)
# print("Subset 1 + Subset 3 Forest")
# root = two_height_tree_gains(combined_df)
# print_nodes()
# for i in range(0, 54):
#     evaluator(root, subset2.iloc[i])
# print_eval()
# reset_eval()

# combined_df = pd.concat([subset2, subset3], ignore_index=True)
# print("Subset 2 + Subset 3 Forest")
# root = two_height_tree_gains(combined_df)
# print_nodes()
# for i in range(0, 54):
#     evaluator(root, subset1.iloc[i])
# print_eval()
# reset_eval()
#
# print_avg()