import random
lines = []
with open('master.txt', 'r') as fin:
    lines = fin.readlines()

random.shuffle(lines)

end = int(len(lines)*(.75))

with open('training.txt', 'w+') as fout:
    fout.writelines(lines[:end])

with open('test.txt','w+') as fout:
    fout.writelines(lines[end:])
