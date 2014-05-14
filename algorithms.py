from util import *

def greedy(elements, reward, cost, budget=250, r=0.0): #reward is a function
    st = [] #s at t
    spent = 0
    while spent <= budget: #Length violation test
        scoret = reward(st) #Maybe save the score when we calculate it in the while loop?
        max_gain = 0.0
        max_gain_idx = -1

        for i in [i for i in range(elements.shape[0]) if i not in st and cost[i] <= budget - spent]:
            temp = list(st)
            temp.append(i)
            gain = (reward(temp) - scoret) / (cost[i] ** r)
            if gain > max_gain:
                max_gain = gain
                max_gain_idx = i

        if max_gain_idx == -1:
            break

        st.append(max_gain_idx)
        spent += cost[max_gain_idx]

    vstar = argmax(lambda x: reward([x]), range(elements.shape[0]))
    if reward([vstar]) > scoret:
        return [vstar]
    return st
