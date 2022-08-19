from importlib.resources import path
import numpy as np
from copy import deepcopy

PAM250 = {
'A': {'A':  2, 'C': -2, 'D':  0, 'E': 0, 'F': -3, 'G':  1, 'H': -1, 'I': -1, 'K': -1, 'L': -2, 'M': -1, 'N':  0, 'P':  1, 'Q':  0, 'R': -2, 'S':  1, 'T':  1, 'V':  0, 'W': -6, 'Y': -3},
'C': {'A': -2, 'C': 12, 'D': -5, 'E':-5, 'F': -4, 'G': -3, 'H': -3, 'I': -2, 'K': -5, 'L': -6, 'M': -5, 'N': -4, 'P': -3, 'Q': -5, 'R': -4, 'S':  0, 'T': -2, 'V': -2, 'W': -8, 'Y':  0},
'D': {'A':  0, 'C': -5, 'D':  4, 'E': 3, 'F': -6, 'G':  1, 'H':  1, 'I': -2, 'K':  0, 'L': -4, 'M': -3, 'N':  2, 'P': -1, 'Q':  2, 'R': -1, 'S':  0, 'T':  0, 'V': -2, 'W': -7, 'Y': -4},
'E': {'A':  0, 'C': -5, 'D':  3, 'E': 4, 'F': -5, 'G':  0, 'H':  1, 'I': -2, 'K':  0, 'L': -3, 'M': -2, 'N':  1, 'P': -1, 'Q':  2, 'R': -1, 'S':  0, 'T':  0, 'V': -2, 'W': -7, 'Y': -4},
'F': {'A': -3, 'C': -4, 'D': -6, 'E':-5, 'F':  9, 'G': -5, 'H': -2, 'I':  1, 'K': -5, 'L':  2, 'M':  0, 'N': -3, 'P': -5, 'Q': -5, 'R': -4, 'S': -3, 'T': -3, 'V': -1, 'W':  0, 'Y':  7},
'G': {'A':  1, 'C': -3, 'D':  1, 'E': 0, 'F': -5, 'G':  5, 'H': -2, 'I': -3, 'K': -2, 'L': -4, 'M': -3, 'N':  0, 'P':  0, 'Q': -1, 'R': -3, 'S':  1, 'T':  0, 'V': -1, 'W': -7, 'Y': -5},
'H': {'A': -1, 'C': -3, 'D':  1, 'E': 1, 'F': -2, 'G': -2, 'H':  6, 'I': -2, 'K':  0, 'L': -2, 'M': -2, 'N':  2, 'P':  0, 'Q':  3, 'R':  2, 'S': -1, 'T': -1, 'V': -2, 'W': -3, 'Y':  0},
'I': {'A': -1, 'C': -2, 'D': -2, 'E':-2, 'F':  1, 'G': -3, 'H': -2, 'I':  5, 'K': -2, 'L':  2, 'M':  2, 'N': -2, 'P': -2, 'Q': -2, 'R': -2, 'S': -1, 'T':  0, 'V':  4, 'W': -5, 'Y': -1},
'K': {'A': -1, 'C': -5, 'D':  0, 'E': 0, 'F': -5, 'G': -2, 'H':  0, 'I': -2, 'K':  5, 'L': -3, 'M':  0, 'N':  1, 'P': -1, 'Q':  1, 'R':  3, 'S':  0, 'T':  0, 'V': -2, 'W': -3, 'Y': -4},
'L': {'A': -2, 'C': -6, 'D': -4, 'E':-3, 'F':  2, 'G': -4, 'H': -2, 'I':  2, 'K': -3, 'L':  6, 'M':  4, 'N': -3, 'P': -3, 'Q': -2, 'R': -3, 'S': -3, 'T': -2, 'V':  2, 'W': -2, 'Y': -1},
'M': {'A': -1, 'C': -5, 'D': -3, 'E':-2, 'F':  0, 'G': -3, 'H': -2, 'I':  2, 'K':  0, 'L':  4, 'M':  6, 'N': -2, 'P': -2, 'Q': -1, 'R':  0, 'S': -2, 'T': -1, 'V':  2, 'W': -4, 'Y': -2},
'N': {'A':  0, 'C': -4, 'D':  2, 'E': 1, 'F': -3, 'G':  0, 'H':  2, 'I': -2, 'K':  1, 'L': -3, 'M': -2, 'N':  2, 'P':  0, 'Q':  1, 'R':  0, 'S':  1, 'T':  0, 'V': -2, 'W': -4, 'Y': -2},
'P': {'A':  1, 'C': -3, 'D': -1, 'E':-1, 'F': -5, 'G':  0, 'H':  0, 'I': -2, 'K': -1, 'L': -3, 'M': -2, 'N':  0, 'P':  6, 'Q':  0, 'R':  0, 'S':  1, 'T':  0, 'V': -1, 'W': -6, 'Y': -5},
'Q': {'A':  0, 'C': -5, 'D':  2, 'E': 2, 'F': -5, 'G': -1, 'H':  3, 'I': -2, 'K':  1, 'L': -2, 'M': -1, 'N':  1, 'P':  0, 'Q':  4, 'R':  1, 'S': -1, 'T': -1, 'V': -2, 'W': -5, 'Y': -4},
'R': {'A': -2, 'C': -4, 'D': -1, 'E':-1, 'F': -4, 'G': -3, 'H':  2, 'I': -2, 'K':  3, 'L': -3, 'M':  0, 'N':  0, 'P':  0, 'Q':  1, 'R':  6, 'S':  0, 'T': -1, 'V': -2, 'W':  2, 'Y': -4},
'S': {'A':  1, 'C':  0, 'D':  0, 'E': 0, 'F': -3, 'G':  1, 'H': -1, 'I': -1, 'K':  0, 'L': -3, 'M': -2, 'N':  1, 'P':  1, 'Q': -1, 'R':  0, 'S':  2, 'T':  1, 'V': -1, 'W': -2, 'Y': -3},
'T': {'A':  1, 'C': -2, 'D':  0, 'E': 0, 'F': -3, 'G':  0, 'H': -1, 'I':  0, 'K':  0, 'L': -2, 'M': -1, 'N':  0, 'P':  0, 'Q': -1, 'R': -1, 'S':  1, 'T':  3, 'V':  0, 'W': -5, 'Y': -3},
'V': {'A':  0, 'C': -2, 'D': -2, 'E':-2, 'F': -1, 'G': -1, 'H': -2, 'I':  4, 'K': -2, 'L':  2, 'M':  2, 'N': -2, 'P': -1, 'Q': -2, 'R': -2, 'S': -1, 'T':  0, 'V':  4, 'W': -6, 'Y': -2},
'W': {'A': -6, 'C': -8, 'D': -7, 'E':-7, 'F':  0, 'G': -7, 'H': -3, 'I': -5, 'K': -3, 'L': -2, 'M': -4, 'N': -4, 'P': -6, 'Q': -5, 'R':  2, 'S': -2, 'T': -5, 'V': -6, 'W': 17, 'Y':  0},
'Y': {'A': -3, 'C':  0, 'D': -4, 'E':-4, 'F':  7, 'G': -5, 'H':  0, 'I': -1, 'K': -4, 'L': -1, 'M': -2, 'N': -2, 'P': -5, 'Q': -4, 'R': -4, 'S': -3, 'T': -3, 'V': -2, 'W':  0, 'Y': 10}
}
n, m = 0, 0
paths = []
seq1, seq2 = '', ''
switch_mark = False

def do_semi_global_alignment(alignment_matrix, n, m, i, j):
    global paths
    # base condition
    if i > n:
        return 
    else:
        if i < 1 or j < 1:
            alignment_matrix[i][j] = 0
        else:
            lambdaa = PAM250[seq1[i-1]][seq2[j-1][0]]
            options = [alignment_matrix[i-1][j-1] + lambdaa, alignment_matrix[i-1][j] - 9, alignment_matrix[i][j-1] - 9]

            Hij = max(options)
            max_index = [x for x, y in enumerate(options) if y == Hij]
            alignment_matrix[i][j] = Hij
            paths[i-1][j-1] = max_index

        if j == m: 
            return do_semi_global_alignment(alignment_matrix, n, m, i+1, 0)
        else:
            return do_semi_global_alignment(alignment_matrix, n, m, i, j+1)

global_seq_i = []
global_seq_j = []

def rec_path_to_seq_i(f_seq1, f_seq2, paths, i, j):
    global global_seq_i
    if i == 0 or j == -1:
        global_seq_i.append([f_seq1, f_seq2, i, j])
        return
    else:
        if 0 in paths[i-1][j]:
            f_seq1 = seq1[i-1] + f_seq1
            f_seq2 = seq2[j] + f_seq2
            i, j = i - 1, j - 1
            rec_path_to_seq_i(f_seq1, f_seq2, paths, i, j)

        if 1 in paths[i-1][j]:
            f_seq1 = seq1[i-1] + f_seq1
            f_seq2 = '-' + f_seq2
            i, j = i - 1, j
            rec_path_to_seq_i(f_seq1, f_seq2, paths, i, j)

        if 2 in paths[i-1][j]:
            f_seq1 = '-' + f_seq1
            f_seq2 = seq2[j] + f_seq2
            i, j = i, j - 1
            rec_path_to_seq_i(f_seq1, f_seq2, paths, i, j)

def rec_path_to_seq_j(f_seq1, f_seq2, paths, i, j):
    global global_seq_j
    if i == -1 or j == 0:
        global_seq_j.append([f_seq1, f_seq2, i, j])
        return
    else:
        if 0 in paths[i][j-1]:
            f_seq1 = seq1[i] + f_seq1
            f_seq2 = seq2[j-1] + f_seq2
            i, j = i - 1, j - 1
            rec_path_to_seq_j(f_seq1, f_seq2, paths, i, j)

        if 1 in paths[i][j-1]:
            f_seq1 = seq1[i] + f_seq1
            f_seq2 = '-' + f_seq2
            i, j = i - 1, j
            rec_path_to_seq_j(f_seq1, f_seq2, paths, i, j)

        if 2 in paths[i][j-1]:
            f_seq1 = '-' + f_seq1
            f_seq2 = seq2[j-1] + f_seq2
            i, j = i, j - 1
            rec_path_to_seq_j(f_seq1, f_seq2, paths, i, j)

def conv_path_to_seq(alignment_matrix, paths, m, n):
    score = max(np.max(alignment_matrix, axis=1)[-1], np.max(alignment_matrix, axis=0)[-1])
    max_index_i = [x for x, y in enumerate([i[-1] for i in alignment_matrix]) if y == score]
    max_index_j = [x for x, y in enumerate(alignment_matrix[-1][:]) if y == score]
    seqs = []
    # i
    for i in max_index_i:
        j = m - 1
        f_seq1 = ''
        f_seq2 = ''
        #start
        f_seq1 += seq1[i:]
        f_seq2 += '-'*(n - i)
        rec_path_to_seq_i(f_seq1, f_seq2, paths, i, j)

    for [f_seq1, f_seq2, i, j] in global_seq_i:
        if i < 1:
            f_seq1 = seq1[:j+1] + f_seq1 
            f_seq2 = '-'*(j+1) + f_seq2
        else:
            f_seq1 = seq1[:i] + f_seq1 
            f_seq2 = '-'*(i) + f_seq2
        if switch_mark:
            seqs.append((f_seq2, f_seq1))
        else:
            seqs.append((f_seq1, f_seq2))
    # j
    for j in max_index_j:
        i = n - 1
        f_seq1 = ''
        f_seq2 = ''
        #start
        f_seq1 += '-'*(m - j)
        f_seq2 += seq2[j:]
        rec_path_to_seq_j(f_seq1, f_seq2, paths, i, j)

    for [f_seq1, f_seq2, i, j] in global_seq_j:
        if j < 1:
            f_seq1 = seq1[:i+1] + f_seq1 
            f_seq2 = '-'*(i+1) + f_seq2
        else:
            f_seq1 = seq1[:j] + f_seq1 
            f_seq2 = '-'*(j) + f_seq2

        if switch_mark:
            seqs.append((f_seq2, f_seq1))
        else:
            seqs.append((f_seq1, f_seq2))

    return list(set(seqs))

def print_res(score, seq):
    print(score)
    sortedSeq = [i[0]+i[1] for i in seq]
    sortedSeq.sort()
    for i in sortedSeq:
        print(i[0:int(len(i)/2)])
        print(i[int(len(i)/2):])

def main(_seq_1, _seq_2):
    global m, n
    global paths
    global seq1, seq2
    seq1, seq2 = _seq_1, _seq_2
    n = len(seq1)
    m = len(seq2)
    paths = [[None for t in range(m)] for u in range(n)]
    alignment_matrix = [[None for j in range(m+1)] for i in range(n+1)]
    do_semi_global_alignment(alignment_matrix, n, m, 0, 0)
    score = max(np.max(alignment_matrix, axis=1)[-1], np.max(alignment_matrix, axis=0)[-1])
    seqs = conv_path_to_seq(alignment_matrix, paths, m, n)
    print_res(score, seqs)
    
if __name__=="__main__":
    seq1 = input()
    seq2 = input()
    if len(seq1) > len(seq2):
        main(seq1, seq2)
    else:
        switch_mark = True
        main(seq2, seq1)


