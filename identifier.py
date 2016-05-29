# This is the program that learns using N-grams and identifies the language of
# each of the development set

import sys, os, analysis
from optparse import OptionParser

langs = "ca da de en es fr is it la nl no pt ro sv tl".split()

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
    for lang in langs:
        if lang != "tl":
            models[lang] = train(lang)

    # Run Model on Development set
    predictions = []
    with open("dev.txt") as f:
        for line in f.readlines():
            predictions.append(predict(line.split("\t", 1)[1]) + "\t" + line)
    
    with open("results.txt", "w") as f:
        f.writelines(predictions)

    print("Check results.txt for the prediction results. The Precision and\
            Recall need to be implemented")

    # Calculate the Precision and Recall
    # TODO:

    # Optionally run on Test set
    pass

def train(lang):
    """
    This function creates a unigram frequency model for the given language
    
    Keyword arguments:
    lang -- the language to train on

    Returns a dictionary model with the frequency counts of each letter
    """
    # Example: if the training set for the language had 10000 characters and
    # 1000 of them were the letter 'e' then P(e) = 0.1 for this language and the
    # dictionary returned would store the value 1000 for the key 'e'
    with open("training.txt"):
        model = dict()
        # be sure to skip any whitespace characters
        pass

def probability(line, model):
    """
    This function returns the probability of the given line using the model.

    Keyword arguments:
    line -- the line to calculate the probability on 
    model -- the model to us
    
    Returns the probability of the given line being reprsented by the given model.
    ;5"""
    pass

def predict(line):
    """
    This function predicts the language for the given line.

    Keyword arguments:
    line -- the line to predict the language for

    Returns the most likely language
    """
    pass


if __name__ == "__main__":
    main()
#comment
