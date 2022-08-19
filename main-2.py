
# from tkinter import N
import copy, math

S_MATCH = 3
S_MISMATCH = -1
S_GAP = -2
S_GAP_GAP = 0
gap_indices = []
seq_num = 0

def global_align(x, y, s_match, s_mismatch, s_gap):
    global gap_indices
    A = []

    for i in range(len(y) + 1):

        A.append([0] * (len(x) + 1))

    for i in range(len(y) + 1):

        A[i][0] = s_gap * i

    for i in range(len(x) + 1):

        A[0][i] = s_gap * i

    for i in range(1, len(y) + 1):

        for j in range(1, len(x) + 1):

            A[i][j] = max(

                A[i][j - 1] + s_gap,

                A[i - 1][j] + s_gap,

                A[i - 1][j - 1] + (s_match if (y[i - 1] == x[j - 1] and y[i - 1] != '-') else 0) + (

                    s_mismatch if (y[i - 1] != x[j - 1] and y[i - 1] != '-' and x[j - 1] != '-') else 0) + (

                    s_gap if (y[i - 1] == '-' or x[j - 1] == '-') else 0)

            )

    align_X = ""

    align_Y = ""

    i = len(x)

    j = len(y)

    gap_indices = []
    while i > 0 or j > 0:

        current_score = A[j][i]

        if i > 0 and j > 0 and (

                ((x[i - 1] == y[j - 1] and y[j - 1] != '-') and current_score == A[j - 1][i - 1] + s_match) or

                ((y[j - 1] != x[i - 1] and y[j - 1] != '-' and x[i - 1] != '-') and current_score == A[j - 1][

                    i - 1] + s_mismatch) or

                ((y[j - 1] == '-' or x[i - 1] == '-') and current_score == A[j - 1][i - 1] + s_gap)

        ):

            align_X = x[i - 1] + align_X

            align_Y = y[j - 1] + align_Y

            i = i - 1

            j = j - 1

        elif i > 0 and (current_score == A[j][i - 1] + s_gap):

            align_X = x[i - 1] + align_X

            if len(gap_indices) != 0:
                gap_indices = [x+1 for x in gap_indices]
                gap_indices.append(j)
            else:
                gap_indices.append(j)

            align_Y = "-" + align_Y

            i = i - 1

        else:

            align_X = "-" + align_X

            align_Y = y[j - 1] + align_Y

            j = j - 1

    return (align_X, align_Y, A[len(y)][len(x)])

def calc_MSA_score(_seqs):
    score = 0
    for i in range(len(_seqs[0])):
        # print('i: ', i)
        for j in range(len(_seqs) - 1):
            # print('j: ', j)
            for k in range(j+1, len(_seqs)):
                # print('k: ', k)
                if _seqs[j][i] == _seqs[k][i] and _seqs[j][i] != '-':
                    score += S_MATCH
                elif _seqs[j][i] == _seqs[k][i] and _seqs[j][i] == '-':
                    score += S_GAP_GAP
                elif _seqs[j][i] != _seqs[k][i] and (_seqs[j][i] == '-' or _seqs[k][i] == '-'):
                    score += S_GAP
                else:
                    score += S_MISMATCH
    return score

def calc_MSA_seqs(_seqs):
    pairwise_similarities_matrix = [[None for x in range(seq_num)] for x in range(seq_num)]
    alignments_with_center = []

    for i in range(seq_num):
        for j in range(seq_num):
            if i == j:
                pairwise_similarities_matrix[i][j] = 0
            else:
                pairwise_similarities_matrix[i][j] = global_align(_seqs[i], _seqs[j], S_MATCH, S_MISMATCH, S_GAP)[2]

    # aggregate score of every sequence
    sum_score_seqs = [sum(x) for x in pairwise_similarities_matrix]

    # center sequence
    # No Duplicates
    center_index = sum_score_seqs.index(max(sum_score_seqs))
    center_seq = _seqs[center_index]

    seqs_in_descending_order = [i[0] for i in sorted(enumerate(pairwise_similarities_matrix[center_index]), key=lambda k: k[1], reverse=True)]
    seqs_in_descending_order.remove(center_index)
    
    alignments_with_center_2 = {}
    # Add sequences to center one by one
    for i in range(len(seqs_in_descending_order)):
        align_X, align_Y, s = global_align(_seqs[seqs_in_descending_order[i]], center_seq, S_MATCH, S_MISMATCH, S_GAP)
        alignments_with_center_2[seqs_in_descending_order[i]] = [align_X, align_Y, s]
        center_seq = copy.deepcopy(align_Y)
        for j in seqs_in_descending_order[0:i]:
            if j != center_index:
                gap_indices.reverse()
                for k in gap_indices:
                    alignments_with_center_2[j][0] = alignments_with_center_2[j][0][:k] + '-' + alignments_with_center_2[j][0][k:]
                alignments_with_center_2[j] = [alignments_with_center_2[j][0], center_seq, alignments_with_center_2[j][2]]

    # print(alignments_with_center_2)
    
    MSA_seqs = [[None for x in range(seq_num)] for x in range(seq_num)]
    MSA_seqs[center_index] = center_seq
    for k, v in alignments_with_center_2.items():
        MSA_seqs[k] = v[0]
    
    # print(MSA_seqs)
    # print(calc_MSA_score(MSA_seqs))

    return MSA_seqs, calc_MSA_score(MSA_seqs)

def pick_blocks(_seqs):
    blocks = []
    for i in range(len(_seqs[0])):
        matches_num = 0
        for j in range(len(_seqs) - 1):
            for k in range(j+1, len(_seqs)):
                if _seqs[j][i] == _seqs[k][i]:
                    matches_num += 1
        if matches_num != math.factorial(seq_num)/((2)*math.factorial(seq_num - 2)):
            if len(blocks) % 2 == 0:
                blocks.append(i)
        elif matches_num == math.factorial(seq_num)/((2)*math.factorial(seq_num - 2)): 
            if len(blocks) > 0:
                if i - blocks[-1] > 1:
                    blocks.append(i)
                else:
                    blocks.pop()
    if len(blocks) % 2 == 1:
        blocks.append(i)
    return blocks

def delete_gaps_from_block(_MSA_seqs, start, end):
    _MSA_seqs = copy.deepcopy(_MSA_seqs)
    for i in range(seq_num):
        _MSA_seqs[i] = _MSA_seqs[i][start:end+1].replace('-', '')
    return _MSA_seqs

if __name__=="__main__":
    seq_num = int(input())
    seqs = []

    for _ in range(seq_num):
        seqs.append(input())

    MSA_seqs, MSA_score = calc_MSA_seqs(seqs)
    # print(blocks)
    # print(MSA_score)
    MSA_score_2 = 100000000
    while MSA_score_2 > MSA_score:

        blocks = pick_blocks(MSA_seqs)
        # print(blocks)
        for i in range(0, len(blocks), 2):
            start, end = blocks[i], blocks[i+1]
            if start == end:
                continue
            # print(start)
            # print(end)
            block_without_gap = delete_gaps_from_block(MSA_seqs, start, end)
            # print(block_without_gap)

            MSA_seqs_2, MSA_score_2 = calc_MSA_seqs(block_without_gap)
            # print(MSA_seqs_2)
            for i in range(seq_num):
                MSA_seqs_2[i] = MSA_seqs[i][:start] + MSA_seqs_2[i] + MSA_seqs[i][end+1:]
            MSA_score_2 = calc_MSA_score(MSA_seqs_2)
            # print(MSA_score_2)
            if MSA_score_2 > MSA_score:
                MSA_seqs = copy.deepcopy(MSA_seqs_2)
                MSA_score = MSA_score_2
            # print(MSA_score_2)
            # print(MSA_seqs)
    
    print(MSA_score)
    for i in range(seq_num):
        print(MSA_seqs[i])





# 4
# MEKKITGYTT
# NMFFVSANPW
# MLNELQQ
# MNAHTAFL
