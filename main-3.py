import copy, math
pseudocount = 2
window_size = 0

def fill_profile(PSSM_profile, seqs):
    for seq in seqs:
        for i in range(len(seq)):
            amino = seq[i]
            if amino not in PSSM_profile:
                PSSM_profile[amino] = [pseudocount for x in range(len(seq))]
                PSSM_profile[amino][i] += 1
            else:
                PSSM_profile[amino][i] += 1

    # calc score
    scored_profile = {}
    for k, v in PSSM_profile.items():
        scored_profile[k] = [round(element/(len(seqs[0]) + pseudocount*len(PSSM_profile.keys())), 3) for element in v]
        _sum = sum(scored_profile[k])
        scored_profile[k] = [round(math.log(round(element/(_sum/len(seqs[0])), 3), 2), 3) for element in scored_profile[k]]
    return scored_profile

def calc_powerset(fullset):
  listsub = list(fullset)
  subsets = []
  for i in range(2**len(listsub)):
    subset = []
    for k in range(len(listsub)):            
      if i & 1<<k:
        subset.append(listsub[k])
    subsets.append(subset)        
  return subsets

def calc_score(sub_seq, pssm_profile):
    score = 0
    for i in range(len(sub_seq)):
        score += pssm_profile[sub_seq[i]][i]
    return score

def find_best_subseq(target_seq, pssm_profile): 
    best_score = -1*math.inf
    best_sub_target = None
    power_set = calc_powerset(set([i for i in range(window_size)]))
    for gap_num in range(window_size):
        char_num = window_size - gap_num
        for i in range(len(target_seq) - char_num + 1):
            tar_part = target_seq[i:i+char_num]
            # insert gaps
            for sub_p_s in power_set:
                if len(sub_p_s) == gap_num:
                    tar_part_temp = copy.deepcopy(tar_part)
                    for sp in sub_p_s:
                        tar_part_temp = tar_part_temp[:sp] + '-' + tar_part_temp[sp:]
                        score = calc_score(tar_part_temp, pssm_profile)
                        if score > best_score:
                            best_score = score
                            best_sub_target = tar_part_temp
    return best_sub_target, best_score

if __name__=="__main__":
    seq_num = int(input())
    seqs = []

    for _ in range(seq_num):
        seqs.append(input())

    window_size = len(seqs[0])
    target_seq = input()

    PSSM_profile = {}
    pssm_profile = fill_profile(PSSM_profile, seqs)

    best_sub_target, best_score = find_best_subseq(target_seq, pssm_profile)
    print(best_sub_target)
