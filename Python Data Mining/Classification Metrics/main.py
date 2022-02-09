# Creates a decision tree based on the best features given, and evaluates the tree based on a classifier.
# Written by Jake Schwarz
import sys

import pandas as pd
from matrix import *
from table import *
from tree import *


pure_csv = pd.read_csv("mutations.csv")
accuracy_table(pure_csv)
root = two_height_tree(pure_csv)
number_of_rows = pure_csv.shape[0]
for i in range(0, number_of_rows):
    # print(pure_csv.iloc[i][0])
    # print(evaluator(root, pure_csv.iloc[i]))
    evaluator(root, pure_csv.iloc[i])
print_eval()




