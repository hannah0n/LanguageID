# This is the program that learns using N-grams and identifies the language of
# each of the development set

import sys, re, os, analysis, operator
from optparse import OptionParser

langs = "ca da de en es fr is it la nl no pt ro sv tl".split()

def loadOptions():
    """Sets up the command line options"""
    parser = OptionParser(usage="usage %prog [options]")
    parser.add_option("-i", "--interactive", help="allows for user interaction",
            action="store_true")
    parser.add_option("-v", "--verbose", help="Outputs verbose information\
            (useful for debugging)",
            action="store_true")
    return parser.parse_args()

def main():
    options, args = loadOptions()
    # Train & Develop Model
    models = {}
    totalCount = {}
    unk = {}
    prob = {}
    for lang in langs:
        models[lang] = {}
        totalCount[lang] = 0
        unk[lang] = 100
    prob = totalCount
    train(models, totalCount, unk)
    # Run Model on Development set
    predictions = []
    with open("dev.txt") as f:
        for line in f.readlines():
            prediction = predict(line.split("\t", 1)[1], models, unk, prob)
            if options.verbose:
                print("PREDICTION: " + str(prediction))
                print("LINE: " + line)
            prediction.sort(key=lambda a: -a[1])
            predictions.append(prediction[1][0])

#     print(predictions)
    with open("results.txt", "w") as f:
        f.write("\n".join(predictions))

    print("Check results.txt for the prediction results. The Precision and Recall need to be implemented")

    # Calculate the Precision and Recall
    analysis.main()

    # Optionally run on Test set
#     predictions = predict(line, models, unk, prob)

def train(models, totalCount, unk):
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
            language = line.split()[0]
            script = line.split('\t',1)[1]
            script = script.strip().replace("\t", "").replace(" ", "")
            if not (models.get(language)):
                unigram = {script[0]:0}
                models[language] = unigram
            else:
                unigram = models.get(language)
            for i in range(0, len(script)):
                cha = script[i]
                if cha in unigram:
                    unigram[cha] += 1
                else:
                    unigram[cha] = 1
            totalCount[language] += len(script)
        f.close()
    for l in models:
        for c in models[l]:
            (models[l])[c] = (models[l])[c] / float(totalCount[l])
            if (models[l])[c] < unk[l]:
                unk[l] = (models[l])[c]

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

def predict(line, models, unk, prob):
    """
    This function predicts the language for the given line.

    Keyword arguments:
    line -- the line to predict the language for

    Returns the most likely language
    """
    script= line.strip().replace("\t", "").replace(" ", "")
    unigram = {}
    for i in range(0, len(script)):
        if not (unigram):
            unigram = {script[0]: 0}
        cha = script[i]
        if cha in unigram:
            unigram[cha] += 1
        else:
            unigram[cha] = 1
    for lang in models:
        num = 0
        for char in unigram:
            if char in models[lang]:
                num += unigram.get(char) * (models.get(lang)).get(char)
            else:
                num += unigram.get(char) * unk.get(lang)
        prob[lang] = num
    predictions = sorted(prob.items(), key=operator.itemgetter(1))
    return predictions

if __name__ == "__main__":
    main()
#comment
