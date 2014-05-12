def greedy(sim_matrix, reward, lengths, max_length=250): #reward is a function
    st = [] #s at t
    length = 0
    while length <= max_length: #Length violation test
        scoret = reward(st) #Maybe save the score when we calculate it in the while loop?
        max_gain = 0.0
        max_gain_idx = -1

        for i in [i for i in range(sim_matrix.shape[0]) if i not in st and lengths[i] <= max_length - length]:
            temp = list(st)
            temp.append(i)
            gain = (reward(temp) - scoret)
            if gain > max_gain:
                max_gain = gain
                max_gain_idx = i

        if max_gain_idx == -1:
            break

        st.append(max_gain_idx)
        length += lengths[max_gain_idx]

    return st

