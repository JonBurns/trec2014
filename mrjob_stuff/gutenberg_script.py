with open('./pandp.txt', 'r') as f:
    content = f.readlines()



noDashes = []

for sentence in content:
    if len(sentence) > 2:
        sentence_temp = sentence.replace('\r\n', ' ', 1)
        noDashes.append(sentence_temp)
    else:
        noDashes.append('\n')



with open('./fixedpandp.txt', 'w') as f:
    for sentence in noDashes:
        f.write(sentence)