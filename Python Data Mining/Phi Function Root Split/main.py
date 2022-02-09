# Calculates the phi funcction for the root node and displays a table of the best features.
# Written by Jake Schwarz
import sys

import pandas as pd
from tree import *


pure_csv = pd.read_csv("mutations.csv")
phi_function_table(pure_csv)