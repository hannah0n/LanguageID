# This is the file used for analysis tools including different precision and
# recall measurements

def main(testFile="dev.txt", resultsFile=None, ignoretl=True):
    if not resultsFile:
        resultsFile = testFile + ".out"
    keyf = open(testFile)
    resultsf = open(resultsFile)
    key = keyf.readlines()
    results = resultsf.readlines()
    keyf.close()
    resultsf.close()
    print("KEY: %s\nPREDICTIONS: %s" % (testFile, resultsFile))

    langs = {}
    for k in "ca da de en es fr is it la nl no pt ro sv tl".split():
        # Create a dictionary to store counts for P/R calculation
        langs[k] = {"TP":0.0, "FP":0.0, "FN":0.0}

    counts = {"tl":0}

    for i in range(0, len(key)):
        trueLang = key[i].split()[0]
        predLang = results[i].split()[0]
        if trueLang == "tl" and ignoretl:
            continue    # Don't let it be part of the calculation
        if predLang == trueLang:
            langs[trueLang]["TP"] += 1
        else:
            langs[trueLang]["FN"] += 1
            langs[predLang]["FP"] += 1
        if trueLang in counts:
            counts[trueLang] += 1
        else: 
            counts[trueLang] = 1

    print("Lang \tPrec. \tRecall \tF1 Score")
    for lang in "ca da de en es fr is it la nl no pt ro sv tl".split():
        if lang == "tl" and ignoretl:
            continue
        d = langs[lang]
        returned = d["TP"] + d["FP"]
        expected = d["TP"] + d["FN"]
        d["P"] = 0.0 if returned == 0 else d["TP"] / returned
        d["R"] = 0.0 if expected == 0 else d["TP"] / expected
        d["F1"] = 0.0 if d["P"] + d["R"] == 0 else 2 * d["P"] * d["R"] / (d["P"] + d["R"])
        print("%s \t%.3f \t%.3f \t%.3f" % (lang, d["P"], d["R"], d["F1"]))

    print("")

    # Print the weighted average
    weighted_precision = 0.0
    weighted_recall = 0.0
    weighted_f1 = 0.0
    for lang in langs:
        if lang == "tl" and ignoretl:
            continue
        values = langs[lang]
        weighted_precision += values["P"] * counts[lang]
        weighted_recall += values["R"] * counts[lang]
        weighted_f1 += values["F1"] * counts[lang]

    weighted_precision = weighted_precision / sum(counts.values())
    weighted_recall = weighted_recall / sum(counts.values())
    weighted_f1 = weighted_f1 / sum(counts.values())

    print("Weighted Average Precision: %.3f" % weighted_precision)
    print("Weighted Average Recall: %.3f" % weighted_recall)
    print("Weighted Average F1 Score: %.3f\n" % weighted_f1)
    return weighted_f1

if __name__ == "__main__":
    main(raw_input("KEY file: "), raw_input("PREDICTIONS file: "))
