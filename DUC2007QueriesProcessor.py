
path = 'ROUGE/DUC-2007/docs/'


with open('ROUGE/DUC-2007/duc2007_topics.txt') as f:
	content = f.readlines()

lines = [line.strip() for line in content]

i = 0

while i < len(lines):
	cluster = lines[i]
	title = lines[i+1]
	query = lines[i+2]
	with open(path + cluster + '/query.txt', 'w') as f:
		f.write(title + ' ' + query)
	i += 3
