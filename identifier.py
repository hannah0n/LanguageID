# This is the program that learns using N-grams and identifies the language of
# each of the development set

import sys, re, os, analysis, operator
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
    return parser.parse_args()

def main():
    options, args = loadOptions()
    # Train & Develop Model
    models = {}
    totalCount = {}
    prob = {}
    for lang in langs:
        models[lang] = {}
        totalCount[lang] = 0
    prob = totalCount
    train(models, totalCount)
    # Run Model on Development set
    predictions = []
    testFile = "test.txt" if options.test else "dev.txt"
    with open(testFile) as f:
        for line in f.readlines():
            prediction = predict(line.split("\t", 1)[1], models, prob)
            prediction.sort(key=lambda a: -a[1])
            if options.verbose:
                print("PREDICTION:", prediction)
                print("LINE: " + line)
            predictions.append(prediction[0][0])

    with open("results.txt", "w") as f:
        f.write("\n".join(predictions))

    print("Check results.txt for the prediction results. The Precision and Recall need to be implemented")

    # Calculate the Precision and Recall
    analysis.main(testFile)

    if options.interactive:
        while True:
            line = raw_input("Line to parse: ")
            prediction = predict(line, models, prob)
            prediction.sort(key=lambda a: -a[1])
            for p in prediction:
                print('  %s : %.3e' % p)


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

def probability(line, models):
    """
    This function returns the probability of the given line using the model.

    Keyword arguments:
    line -- the line to calculate the probability on 
    model -- the model to us

    Returns the probability of the given line being represented by the given model.
    ;5"""
    pass

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
    return prob.items()

if __name__ == "__main__":
    main()
#comment
