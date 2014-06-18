import math

def l1(s, sim_matrix, corpus_sums, alpha_numer = 12): #summary is collection of indicies
    n = sim_matrix.shape[0]
    alpha = float(alpha_numer)/float(n)
    score_sum = 0.0

    for i in range(n):
        score_sum += min([sum([sim_matrix[i, j] for j in s]), (alpha * corpus_sums[i])])
    return score_sum


def r1(s, corpus_sums, groups, rqj, beta = 0.5):
    k = len(groups)
    n = float(len(corpus_sums))

    result = 0.0
    for p in groups:
        result2 = 0.0
        for j in set(p).intersection(set(s)):
            result2 += ((beta/n) * corpus_sums[j] + ((1 - beta) * rqj[j]))

        result += math.sqrt(result2)

    return result

def rq2(s, corpus_sums, mu, rqj, beta=0.5):
    num_k = len(mu[0])
    n = len(corpus_sums)

    result = 0.0

