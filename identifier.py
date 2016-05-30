# This is the program that learns using N-grams and identifies the language of
# each of the development set

import sys, re, os, analysis, operator
from optparse import OptionParser
from socket import p

langs = "ca da de en es fo fr is it la nb nl nn pt ro sv tl".split()

def loadOptions():
    """Sets up the command line options"""
    parser = OptionParser(usage="usage %prog [options]")
    parser.add_option("-i", "--interactive", help="allows for user interaction",
            action="store_true")
    parser.add_option("-v", "--verbose", help="Outputs verbose information",
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
    train(models)
    # Run Model on Development set
    predictions = []
    with open("dev.txt") as f:
        for line in f.readlines():
            predictions.append(predict(line) + " " + line)

    # Calculate the Precision and Recall
    

    # Optionally run on Test set
    predict(line, models, unk, prob, predictions)

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
            if (line.split()[0]) in models: #necessary??
                language = line.split()[0]
                script = line.split(' ',1)[1]
                script = script.replace("\t", "").replace(" ", "")
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
        for c in models.get[l]:
            (models.get[l])[c] = (models.get[l]).get[c] / totalCount[l]
            if (models.get[l]).get[c] < unk.get[l]:
                unk[l] = (models.get[l]).get[c]
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

def predict(line, models, unk, prob, predictions):
    """
    This function predicts the language for the given line.

    Keyword arguments:
    line -- the line to predict the language for

    Returns the most likely language
    """
    language = line.split()[0]
    script = line.split(' ', 1)[1]
    script = script.replace("\t", "").replace(" ", "")
    unigram = {}
    num = 0
    for i in range(0, len(script)):
        if not (unigram):
            unigram = {script[0]: 0}
        cha = script[i]
        if cha in unigram:
            unigram[cha] += 1
        else:
            unigram[cha] = 1
    for lang in models:
        for char in unigram:
            if (models.get(lang)).has_key(char):
                num += unigram.get(char) * (models.get(lang)).get(char)
            else:
                num += unigram.get(char) * unk.get(lang)
        prob[lang] = num
    predictions  = sorted(prob.items(), key=operator.itemgetter(1))
    return predictions
if __name__ == "__main__":
    main()
#comment
