def argmax(f, coll):
    score_element_pairs = [(f(e), e) for e in coll]
    return list(reversed(sorted(score_element_pairs, key= lambda x: x[0])))[0][1]

def argmin(f, coll):
    score_element_pairs = [(f(e), e) for e in coll]
    return list(sorted(score_element_pairs, key= lambda x: x[0]))[0][1]
