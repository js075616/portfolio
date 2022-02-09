# Creates a confusion matrix based on the column total_max_index and the passed DataFrame
# Written by Jake Schwarz
def create_matrix(passed_csv, total_max_index):
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    c_num = 0
    nc_num = 0
    number_of_rows = passed_csv.shape[0]
    # print("Number of Rows: " + str(number_of_rows))
    for row in range(0, number_of_rows):
        if str(passed_csv.iloc[row, 0][0]) == "C":
            c_num += 1
        else:
            nc_num += 1
    # print("c_num: " + str(c_num))
    # print("nc_num: " + str(nc_num))
    for row in range(0, c_num):
        tp += passed_csv.iloc[row, total_max_index]
    for row2 in range(c_num, nc_num+c_num):
        fp += passed_csv.iloc[row2, total_max_index]
    fn = c_num - tp
    tn = nc_num - fp

    print("Confusion Matrix for " + passed_csv.columns[total_max_index] + "\n")
    print("                 Predicted")
    print("                 C      NC")
    print("Actual    C    %3d     %3d" % (tp, fn))
    print("         NC    %3d     %3d\n" % (fp, tn))
