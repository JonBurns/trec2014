

with open('./wandp.txt', 'r') as f:
    content = f.readlines()



noDashes = []

for sentence in content:
    if len(sentence) > 2:
        sentence_temp = sentence.replace('\n', ' ', 1)
        noDashes.append(sentence_temp)
    else:
        noDashes.append('\n')



with open('./fixedwandp_t.txt', 'w') as f:
    for sentence in noDashes:
        f.write(sentence)