import random, analysis
language = []
total = 0
count = []
with open("training.txt") as f1:
    for line in f1.readlines():
        lan, script = line.split("\t", 1)
        if lan in language:
            count[language.index(lan)] += 1
        else:
            language.append(lan)
            count.append(0)
        total += 1

for l in language:
    i = language.index(l)
    count[i] = count[i] / float(total)

# for i in language:
#     ind = language.index(i)
#     if ind > 0:
#         count[ind] += count[ind-1]

# Separate the range 0,1 into 
ranges = [count[0]]
for i in range(1, len(count)):
    ranges.append(ranges[i-1] + count[i])

ranges[len(ranges) -1] = 1

with open("dev.txt") as f2:
    with open("baseline.txt", "w") as f:
        for l in f2.readlines():
            number = random.random()
            i = 0
            while number > ranges[i]:
                i += 1
            f.write(language[i] + '\n')


analysis.main(resultsFile="baseline.txt")
