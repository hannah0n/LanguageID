# This is the program that learns using N-grams and identifies the language of
# each of the development set

import sys, re, os, analysis, operator, math
from optparse import OptionParser

langs = "ca da de en es fr is it la nl no pt ro sv".split()

def loadOptions():
    """Sets up the command line options"""
    parser = OptionParser(usage="usage %prog [options]")
    parser.add_option("-i", "--interactive", help="allows for user interaction",
            action="store_true")
    parser.add_option("-v", "--verbose", help="outputs verbose information "
            "(useful for debugging)",
            action="store_true")
    parser.add_option("-t", "--test", help="run against test data",
            action="store_true")
    parser.add_option("-x", "--notag", help="Don't include tagalog as part of"
            " P/R calculation for the test set",
            action="store_true")
    parser.add_option("-s", "--stage", metavar="SIZE",
            help="which stage to run (default is 1)",
            default=1, type="int")
    parser.add_option("-n", "--N", metavar="SIZE",
            help="Number of high frequency words to keep track of (default is 5000)",
            default=5000, type="int")
    return parser.parse_args()

def main():
    options, args = loadOptions()
    # Train & Develop Model
    s1models = {l:{} for l in langs}
    totalCount = {l:0 for l in langs}
    prob = totalCount
    train(s1models, totalCount)
    if options.stage == 2:
        s2models = trainFreqWords(options.N)

    # Run Model on Training Set
    predictions = []
    testFile = "training.txt"
    with open(testFile) as f:
        for line in f:
            line = line.split("\t", 1)[1]
            if options.stage == 2:
                prediction = predict2(line, s1models, s2models, includetl=not
                        options.notag)
            else:
                prediction = predict(line, s1models, prob)
            predictions.append(prediction[0][0])
    with open(testFile + ".out", "w") as f:
        f.write("\n".join(predictions))
    analysis.main(testFile, ignoretl = options.notag or not options.test)

    # Run Model on Development Set
    predictions = []
    testFile = "test.txt" if options.test else "dev.txt"
    with open(testFile) as f:
        for line in f.readlines():
            key, line = line.split("\t", 1)
            if options.stage == 2:
                prediction = predict2(line, s1models, s2models,
                        includetl=not options.notag)
            else:
                prediction = predict(line, s1models, prob)
            if options.verbose:
                print("PREDICTION:", prediction)
                print("LINE: " + line)
            predictions.append(prediction[0][0])

    with open(testFile + ".out", "w") as f:
        f.write("\n".join(predictions))

    print("Check " + testFile + ".out for the prediction results.")

    # Calculate the Precision and Recall
    analysis.main(testFile, ignoretl = options.notag or not options.test)

    if options.interactive:
        while True:
            try:
                line = raw_input("Line to parse: ")
            except EOFError:
                print("\nShutting Down...")
                break
            if options.stage == 2:
                prediction = predict2(line, s1models, s2models,
                        includetl= not options.notag)
            else:
                prediction = predict(line, s1models, prob)
            sum_prob = sum([p[1] for p in prediction])
            for l, p in prediction:
                print('  %s : %.2f%%' % (l, p * 100 / sum_prob))

        # This code was used for parameter tuning
# #     if True:
# #         return
# #     weights=[0.85, 0.8, .75, 0.7, 0.65, 0.6, 0.55, 0.5]
#     weights = [0.01, 0.001, 0]
# #     weights=[0.5]
#     Ns = [10000, 100000]
#     data = {n:{w:{} for w in weights} for n in Ns}
#     for n in Ns:
#         for w in weights:
#             s1models = {l:{} for l in langs}
#             totalCount = {l:0 for l in langs}
#             prob = totalCount
#             print("Testing N = %d \t w = %f " % (n, w))
#             train(s1models, totalCount)
#             s2models = trainFreqWords(n)
#             predictions = []
#             testFile = "training.txt"
#             with open(testFile) as f:
#                 for line in f:
#                     line = line.split("\t", 1)[1]
#                     prediction = predict2(line, s1models, s2models, w)
#                     predictions.append(prediction[0][0])
#             with open(testFile + ".out", "w") as f:
#                 f.write("\n".join(predictions))
#             predictions = []
#             testFile = "dev.txt"
#             data[n][w]["train"] = analysis.main(testFile)
#             with open(testFile) as f:
#                 for line in f.readlines():
#                     line = line.split("\t", 1)[1]
#                     prediction = predict2(line, s1models, s2models, w)
#                     predictions.append(prediction[0][0])
#             with open(testFile + ".out", "w") as f:
#                 f.write("\n".join(predictions))
#             data[n][w]["dev"] = analysis.main(testFile)
#     
#     for n in Ns:
#         for w in weights:
#             print("N = %d \t w = %.3f \t train = %.3f \t dev = %.3f" %(n, w,
#                 data[n][w]["train"], data[n][w]["dev"]))
# 


def train(models, totalCount):
    """
    This function creates a unigram frequency model for the given language
    
    Keyword arguments:
    lang -- the language to train on

    Returns a dictionary model with the frequency counts of each letter
    """
    # Example: if the training set for the language had 10000 characters and
    # 1000 of them were the letter 'e' then P(e) = 0.1 for this language and the
    # dictionary returned would store the value 1000 for the key 'e'

    with open("training.txt") as f:
        # be sure to skip any whitespace characters
        for line in f.readlines():
            language, script = line.split("\t", 1)
            script = script.strip().replace("\t", "").replace(" ", "")
            if not (models.get(language)):
                unigram = {}
                models[language] = unigram
            else:
                unigram = models.get(language)
            for cha in script:
                if cha in unigram:
                    unigram[cha] += 1
                else:
                    unigram[cha] = 1
                totalCount[language] += 1

    for l in models:
        for c in models[l]:
            (models[l])[c] = (models[l])[c] / float(totalCount[l])
        # Replace the least frequent character with UNK
        sortedlist = sorted(models[l].keys(), key=lambda c: models[l][c])
        models[l]["UNK"] = models[l][sortedlist[0]]
        del models[l][sortedlist[0]]


#     for l, m in models.iteritems():
#         print("LANG: " + l)
#         print(sum(m.values()))
#         for c, p in m.iteritems():
#             print("  %s: %f" % (c, p))
        #Train data

# Returns a model for high frequency words in each language
def trainFreqWords(N = 10000):
    """
    This function creates a unigram word frequency model for each language using
    the top N words and leaving the rest as UNK.
    """
    tally = {l:{} for l in langs}
    with open("training.txt") as f:
        for inline in f.readlines():
            lang, line = inline.split("\t", 1)
            for word in line.split():
                if word in tally[lang]:
                    tally[lang][word] += 1
                else:
                    tally[lang][word] = 1
    
    for lang in tally:
        d = tally[lang]
        # Save the ten most popular words
        tally[lang] = dict(sorted(d.items(), key=lambda (k,v): -v)[0:N+1])
        totalCount = sum(tally[lang].values())
        for w in tally[lang]:
            tally[lang][w] = tally[lang][w] / float(totalCount);
        minVal = min(tally[lang].values())
        del tally[lang][sorted(tally[lang].keys(), key=lambda k: tally[lang][k])[0]]
        tally[lang]["_UNK_"] = minVal

#     for l, m in tally.items():
#         print("LANG: " + l)
#         print(sum(m.values()))
#         for c, p in sorted(m.items(), key=lambda(k,v):-v):
#             print("  %s: %.2f%%" % (c, p * 100))
# 
#     sys.exit()

    return tally

def predict(line, models, prob):
    """
    This function predicts the language for the given line.

    Keyword arguments:
    line -- the line to predict the language for

    Returns the most likely language
    """
    script= line.strip().replace("\t", "").replace(" ", "")
    for lang in models:
        num = 1.0
        for char in script:
            if char in models[lang]:
                num *= models[lang][char]
            else:
                num *= models[lang]["UNK"]
        prob[lang] = num
    return sorted(prob.items(), key=lambda (k, v): -v)

def predict2(line, s1models, s2models, s2weight=0.75, includetl=False):
    """
    This function predicts the language for the given line using the models
    developed for stage 1 and 2.

    Returns a probability dictionary mapping language to probability
    """
    p1 = {l:1.0 for l in langs}
    p2 = {l:1.0 for l in langs}
    predict(line, s1models, p1)
    totalunkcount = 0
    for lang in s1models:
        unkcount = 0
        for w in line.split():
            if w not in s2models[lang]:
                unkcount += 1
            w = w if w in s2models[lang] else "_UNK_"
            p2[lang] *= s2models[lang][w]
        totalunkcount += unkcount

    # In other words, on average none of the models knew 13/14 words
    if includetl:
        if (totalunkcount > 13 * len(line.split())):
            return [("tl", 1.0)]

    """ First, let's calculate the relative probability of one language to
    the other in both models then combine them"""
    p1Sum = sum(p1.values())
    p2Sum = sum(p2.values())
    emptycount = 0
    for p in p1.values():
        if p == 0:
            emptycount += 1
#             print(p1.values())

    # The characters multiplied together gave a low probability.
#     if includetl and emptycount > 13:
#         return [("tl", 1.0)]

    if p1Sum == 0: p1Sum = 1
    if p2Sum == 0: p2Sum = 1
    p1 = {l: p * 100 /  p1Sum for l, p in p1.items()}
    p2 = {l:p * 100 / p2Sum for l, p in p2.items()}
    p = {l:p1[l] * (1 - s2weight) + p2[l] * s2weight for l in langs}


    return sorted(p.items(), key=lambda (k, v): -v)


if __name__ == "__main__":
    main()
#comment
