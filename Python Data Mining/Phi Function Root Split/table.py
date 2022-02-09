# Creates a top ten table based on the DataFrame passed in. Prints the table to the console and returns the max index
# of the first maximum
# Written by Jake Schwarz
from tabulate import tabulate


# Used to calculate the TP and FP of each sample and make a table of the top 10 based on TP - FP
def top_ten_table_tpfp(passed_csv):
    tp = [0 for i in range(1411)]
    fp = [0 for i in range(1411)]
    tp_minus_fp = [0 for i in range(1411)]
    gene_names = [0 for i in range(1411)]
    c_num = 0
    nc_num = 0
    number_of_rows = passed_csv.shape[0]
    # print("Number of Rows: " + str(number_of_rows))
    for row in range(0, number_of_rows):
        if str(passed_csv.iloc[row, 0][0]) == "C":
            c_num += 1
        else:
            nc_num += 1
    if c_num == 0:
        print("This is a pure set of NC samples, there may be no need to separate further.")
    elif nc_num == 0:
        print("This is a pure set of C samples, there may be no need to separate further.")
    # print("c_num: " + str(c_num))
    # print("nc_num: " + str(nc_num))
    for column in range(1, 1410):
        for row in range(0, c_num):
            tp[column] += passed_csv.iloc[row, column]
        for row2 in range(c_num, nc_num + c_num):
            fp[column] += passed_csv.iloc[row2, column]

    for i in range(0, 1141):
        tp_minus_fp[i] = tp[i] - fp[i]
        gene_names[i] = passed_csv.columns[i]

    max_value = max(tp_minus_fp)
    max_index = tp_minus_fp.index(max_value)
    total_max_index = max_index  # 107 for DOCK3
    # print("Max value in TP - FP is " + str(max_value) + " with an index of " + str(max_index))
    # print(passed_csv.columns[max_index])
    table = [["Mutation", "TP - FP"], [passed_csv.columns[max_index], max_value]]
    tp_minus_fp.pop(max_index)
    gene_names.pop(max_index)
    for i in range(0, 9):
        max_value = max(tp_minus_fp)
        max_index = tp_minus_fp.index(max_value)
        # print("Max value in TP - TP is " + str(max_value) + " with an index of " + str(max_index))
        # print(passed_csv.columns[max_index])
        table.append([gene_names[max_index], max_value])
        tp_minus_fp.pop(max_index)
        gene_names.pop(max_index)
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
    print("")
    return total_max_index


def accuracy_table(passed_csv):
    tp = [0 for i in range(1411)]
    fp = [0 for i in range(1411)]
    tn = [0 for i in range(1411)]
    fn = [0 for i in range(1411)]
    accuracy = [0 for i in range(1411)]
    gene_names = [0 for i in range(1411)]
    c_num = 0
    nc_num = 0
    number_of_rows = passed_csv.shape[0]
    # print("Number of Rows: " + str(number_of_rows))
    for row in range(0, number_of_rows):
        if str(passed_csv.iloc[row, 0][0]) == "C":
            c_num += 1
        else:
            nc_num += 1
    if c_num == 0:
        print("This is a pure set of NC samples, there may be no need to separate further.")
    elif nc_num == 0:
        print("This is a pure set of C samples, there may be no need to separate further.")
    # print("c_num: " + str(c_num))
    # print("nc_num: " + str(nc_num))
    for column in range(1, 1410):
        for row in range(0, c_num):
            if passed_csv.iloc[row, column] == 0:
                fn[column] += 1
            else:
                tp[column] += passed_csv.iloc[row, column]
        for row2 in range(c_num, nc_num + c_num):
            if passed_csv.iloc[row2, column] == 0:
                tn[column] += 1
            else:
                fp[column] += passed_csv.iloc[row2, column]

    for i in range(0, 1141):
        accuracy[i] = (tp[i] + tn[i]) / 162
        gene_names[i] = passed_csv.columns[i]

    max_accuracy = max(accuracy)
    max_index = accuracy.index(max_accuracy)
    current_tp = tp[max_index]
    current_tn = tn[max_index]
    current_fp = fp[max_index]
    current_fn = fn[max_index]
    total_max_index = max_index  # 107 for DOCK3
    # print("Max value in TP - FP is " + str(max_value) + " with an index of " + str(max_index))
    # print(passed_csv.columns[max_index])
    table = [["Mutation", "Accuracy", "TP", "TN", "FP", "FN"], [passed_csv.columns[max_index], max_accuracy, current_tp, current_tn, current_fp, current_fn]]
    accuracy.pop(max_index)
    tp.pop(max_index)
    tn.pop(max_index)
    fp.pop(max_index)
    fn.pop(max_index)
    gene_names.pop(max_index)
    for i in range(0, 9):
        max_accuracy = max(accuracy)
        max_index = accuracy.index(max_accuracy)
        current_tp = tp[max_index]
        current_tn = tn[max_index]
        current_fp = fp[max_index]
        current_fn = fn[max_index]
        # print("Max value in TP - TP is " + str(max_value) + " with an index of " + str(max_index))
        # print(passed_csv.columns[max_index])
        table.append([passed_csv.columns[max_index], max_accuracy, current_tp, current_tn, current_fp, current_fn])
        accuracy.pop(max_index)
        tp.pop(max_index)
        tn.pop(max_index)
        fp.pop(max_index)
        fn.pop(max_index)
        gene_names.pop(max_index)
    print("Accuracy Table")
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
    print("")


def calculate_max_index_tpfp(passed_csv):
    tp = [0 for i in range(1411)]
    fp = [0 for i in range(1411)]
    tp_minus_fp = [0 for i in range(1411)]
    gene_names = [0 for i in range(1411)]
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
    for column in range(1, 1410):
        for row in range(0, c_num):
            tp[column] += passed_csv.iloc[row, column]
        for row2 in range(c_num, nc_num + c_num):
            fp[column] += passed_csv.iloc[row2, column]

    for i in range(0, 1141):
        tp_minus_fp[i] = tp[i] - fp[i]
        gene_names[i] = passed_csv.columns[i]

    max_value = max(tp_minus_fp)
    max_index = tp_minus_fp.index(max_value)
    return max_index


def phi_function_table(passed_csv):
    nt = 162
    ntc = 56
    ntnc = 106
    gene_names = [0 for i in range(1411)]
    ntl = [0 for i in range(1411)]
    ntr = [0 for i in range(1411)]
    ntlc = [0 for i in range(1411)]
    ntlnc = [0 for i in range(1411)]
    ntrc = [0 for i in range(1411)]
    ntrnc = [0 for i in range(1411)]
    phi = [0 for i in range(1411)]
    for column in range(1, 1410):
        gene_names[column] = passed_csv.columns[column]
        for row in range(0, 162):
            if passed_csv.iloc[row][column] == 1:
                ntl[column] += 1
                if str(passed_csv.iloc[row, 0][0]) == "C":
                    ntlc[column] += 1
                else:
                    ntlnc[column] += 1
            else:
                ntr[column] += 1
                if str(passed_csv.iloc[row, 0][0]) == "C":
                    ntrc[column] += 1
                else:
                    ntrnc[column] += 1
        pl = ntl[column] / nt
        pr = ntr[column] / nt
        pctl = ntlc[column] / ntl[column]
        pnctl = ntlnc[column] / ntl[column]
        pctr = ntrc[column] / ntr[column]
        pnctr = ntrnc[column] / ntr[column]
        qst = abs(pctl - pctr) + abs(pnctl - pnctr)
        phi[column] = (2 * pl * pr) * qst
    # print(gene_names[107])
    # print(ntlc[107])
    # print(ntlnc[107])
    # print(ntrc[107])
    # print(ntrnc[107])
    # print(phi[column])

    # total_max_index = max_index
    table = [["Mutation", "n(tl)", "n(tr)", "n(tl,C)", "n(tl,NC)", "n(tr,C)", "n(tr,NC)", "Pl", "Pr", "P(C|tl)", "P(NC|tl)", "P(C|tr)", "P(NC|tr)", "2PlPr", "Q", "phi(s,t)"]]
    for i in range(0, 10):
        max_value = max(phi)
        max_index = phi.index(max_value)
        pl = ntl[max_index] / nt
        pr = ntr[max_index] / nt
        pctl = ntlc[max_index] / ntl[max_index]
        pnctl = ntlnc[max_index] / ntl[max_index]
        pctr = ntrc[max_index] / ntr[max_index]
        pnctr = ntrnc[max_index] / ntr[max_index]
        qst = abs(pctl - pctr) + abs(pnctl - pnctr)
        table.append(
            [gene_names[max_index][0:gene_names[max_index].find(":")]+"\n"+gene_names[max_index][gene_names[max_index].find(":"):len(gene_names[max_index])], ntl[max_index], ntr[max_index], ntlc[max_index], ntlnc[max_index], ntrc[max_index],
             ntrnc[max_index], str(round(pl * 100,3)) + "%", str(round(pr * 100,3)) + "%", str(round(pctl * 100,3)) + "%", str(round(pnctl * 100,3)) + "%",
             str(round(pctr * 100,3)) + "%", str(round(pnctr * 100,3)) + "%", str(round(2*pl*pr,3))+"%", qst, phi[max_index]])
        gene_names.pop(max_index)
        ntl.pop(max_index)
        ntr.pop(max_index)
        ntlc.pop(max_index)
        ntlnc.pop(max_index)
        ntrc.pop(max_index)
        ntrnc.pop(max_index)
        phi.pop(max_index)
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid', numalign="right"))
    print("")
    # return total_max_index
