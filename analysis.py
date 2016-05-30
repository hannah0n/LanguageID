# This is the file used for analysis tools including different precision and
# recall measurements

def main():
    keyf = open("dev.txt")
    resultsf = open("results.txt")
    key = keyf.readlines()
    results = resultsf.readlines()
    keyf.close()
    resultsf.close()

    langs = {}
    for k in "ca da de en es fr is it la nl no pt ro sv tl".split():
        # Create a dictionary to store counts for P/R calculation
        langs[k] = {"TP":0.0, "FP":0.0, "FN":0.0}

    for i in range(0, len(key)):
        trueLang = key[i].split()[0]
        predLang = results[i].split()[0]
        if predLang == trueLang:
            langs[trueLang]["TP"] += 1
        else:
            langs[trueLang]["FN"] += 1
            langs[predLang]["FP"] += 1

    print("Lang \tPrec. \tRecall \tF1 Score")
    for lang, d in langs.iteritems():
        if d["TP"] + d["FP"] > 0:
            Precision = d["TP"] / (d["TP"] + d["FP"])
        else:
            Precision = 0.0
        if d["TP"] + d["FN"] > 0:
            Recall = d["TP"] / (d["TP"] + d["FN"])
        else:
            Recall = 0.0
        if Precision + Recall > 0:
            F1Score = (2 * Precision * Recall) / (Precision + Recall)
        else:
            F1Score = 0.0
        print("%s \t%.2f \t%.2f \t%.2f" % (lang, Precision, Recall, F1Score))

if __name__ == "__main__":
    main()
