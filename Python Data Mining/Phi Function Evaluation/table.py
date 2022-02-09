# Creates a top ten table based on the DataFrame passed in. Prints the table to the console and returns the max index
# of the first maximum
# Written by Jake Schwarz
from tabulate import tabulate


# Used to calculate the TP and FP of each sample and make a table of the top 10 based on TP - FP
def top_ten_table(passed_csv):
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

    max_value = max(tp_minus_fp)
    max_index = tp_minus_fp.index(max_value)
    return max_index


def phi_function_table(passed_csv):
    nt = passed_csv.shape[0]
    print(nt)
    ntc = 0
    ntnc = 0
    phi = [0 for i in range(1411)]
    gene_names = [0 for i in range(1411)]

    for row in range(0, nt):
        if str(passed_csv.iloc[row, 0][0]) == "C":
            ntc += 1
        else:
            ntnc += 1

    for column in range(1, 1411):
        ntl = 0
        ntr = 0
        ntlc = 0
        ntlnc = 0
        ntrc = 0
        ntrnc = 0
        gene_names[column] = passed_csv.columns[column]
        for row in range(0, nt):
            if passed_csv.iloc[row][column] == 1:
                ntl += 1
                if str(passed_csv.iloc[row, 0][0]) == "C":
                    ntlc += 1
                else:
                    ntlnc += 1
            else:
                ntr += 1
                if str(passed_csv.iloc[row, 0][0]) == "C":
                    ntrc += 1
                else:
                    ntrnc += 1
        pl = ntl / nt
        pr = ntr / nt
        if ntl == 0:
            pctl = ntlc / 0.0000000001
            pnctl = ntlnc / 0.0000000001
        else:
            pctl = ntlc / ntl
            pnctl = ntlnc / ntl
        if ntr == 0:
            pctr = ntrc / 0.0000000001
            pnctr = ntrnc / 0.0000000001
        else:
            pctr = ntrc / ntr
            pnctr = ntrnc / ntr
        qst = abs(pctl - pctr) + abs(pnctl - pnctr)
        phi[column] = (2 * pl * pr) * qst
    # total_max_index = max_index

    table = [["Mutation", "n(tl)", "n(tr)", "n(tl,C)", "n(tl,NC)", "n(tr,C)", "n(tr,NC)", "Pl", "Pr", "P(C|tl)", "P(NC|tl)", "P(C|tr)", "P(NC|tr)", "2PlPr", "Q", "phi(s,t)"]]
    for i in range(0, 10):
        max_value = max(phi)
        max_index = phi.index(max_value)
        if i == 0:
            total_max_index = max_index
        ntl = 0
        ntr = 0
        ntlc = 0
        ntlnc = 0
        ntrc = 0
        ntrnc = 0
        for row in range(1, nt):
            if passed_csv.iloc[row][max_index] == 1:
                ntl += 1
                if str(passed_csv.iloc[row, 0][0]) == "C":
                    ntlc += 1
                else:
                    ntlnc += 1
            else:
                ntr += 1
                if str(passed_csv.iloc[row, 0][0]) == "C":
                    ntrc += 1
                else:
                    ntrnc += 1
        pl = ntl / nt
        pr = ntr / nt
        if ntl == 0:
            pctl = ntlc / 0.0000000001
            pnctl = ntlnc / 0.0000000001
        else:
            pctl = ntlc / ntl
            pnctl = ntlnc / ntl
        if ntr == 0:
            pctr = ntrc / 0.0000000001
            pnctr = ntrnc / 0.0000000001
        else:
            pctr = ntrc / ntr
            pnctr = ntrnc / ntr
        qst = abs(pctl - pctr) + abs(pnctl - pnctr)
        table.append(
            [gene_names[max_index], ntl, ntr, ntlc, ntlnc, ntrc,
             ntrnc, str(round(pl * 100,3)) + "%", str(round(pr * 100,3)) + "%", str(round(pctl * 100,3)) + "%", str(round(pnctl * 100,3)) + "%",
             str(round(pctr * 100,3)) + "%", str(round(pnctr * 100,3)) + "%", str(round(2*pl*pr,3))+"%", qst, phi[max_index]])
        gene_names.pop(max_index)
        phi.pop(max_index)
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid', numalign="right"))
    print("")
    return total_max_index


def calculate_max_index_phi(passed_csv):
    nt = passed_csv.shape[0]
    ntc = 0
    ntnc = 0
    phi = [0 for i in range(1411)]

    for row in range(0, nt):
        if str(passed_csv.iloc[row, 0][0]) == "C":
            ntc += 1
        else:
            ntnc += 1

    for column in range(1, 1411):
        ntl = 0
        ntr = 0
        ntlc = 0
        ntlnc = 0
        ntrc = 0
        ntrnc = 0
        for row in range(1, nt):
            if passed_csv.iloc[row][column] == 1:
                ntl += 1
                if str(passed_csv.iloc[row, 0][0]) == "C":
                    ntlc += 1
                else:
                    ntlnc += 1
            else:
                ntr += 1
                if str(passed_csv.iloc[row, 0][0]) == "C":
                    ntrc += 1
                else:
                    ntrnc += 1
        pl = ntl / nt
        pr = ntr / nt
        if ntl == 0:
            pctl = ntlc / 0.0000000001
            pnctl = ntlnc / 0.0000000001
        else:
            pctl = ntlc / ntl
            pnctl = ntlnc / ntl
        if ntr == 0:
            pctr = ntrc / 0.0000000001
            pnctr = ntrnc / 0.0000000001
        else:
            pctr = ntrc / ntr
            pnctr = ntrnc / ntr
        qst = abs(pctl - pctr) + abs(pnctl - pnctr)
        phi[column] = (2 * pl * pr) * qst

    max_value = max(phi)
    max_index = phi.index(max_value)
    return max_index
