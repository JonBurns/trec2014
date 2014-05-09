import math

def l1(sim_matrix, s, corpus_sums): #summary is collection of indicies
    n = sim_matrix.shape[0]
    alpha = 12.0/n
    score_sum = 0.0

    for i in range(n):
        score_sum += min([sum([sim_matrix[i, j] for j in s]), (alpha * corpus_sums[i])])
    return score_sum

def r1(corpus_sums, s, groups, rqj, beta = 0.5):
    k = len(groups)
    n = len(corpus_sums)

    result = 0.0
    for p in groups:
        result2 = 0.0
        for j in set(p).intersection(set(s)):
            result2 += ((beta/n) * corpus_sums[j] + ((1 - beta) * rqj[j]))

        result += math.sqrt(result2)

    return result
