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
    rlang = ['ca', 'es', 'fr', 'it', 'la', 'pt', 'ro']
    glang = ['da', 'de', 'en', 'is', 'nl', 'no', 'sv']
    romance = {"TP": 0.0, "FP": 0.0, "FN": 0.0}
    germanic = {"TP": 0.0, "FP": 0.0, "FN": 0.0}
    matrix = {}
    for k in "ca da de en es fr is it la nl no pt ro sv tl".split():
        # Create a dictionary to store counts for P/R calculation
        langs[k] = {"TP": 0.0, "FP": 0.0, "FN": 0.0}
        matrix[k] = {"ca":0.0, "da":0.0, "de":0.0, "en":0.0, "es":0.0, "fr":0.0, "is":0.0, "it":0.0, "la":0.0, "nl":0.0, "no":0.0, "pt":0.0, "ro":0.0, "sv":0.0, "tl":0.0}

    counts = {"tl": 0}

    for i in range(0, len(key)):
        trueLang = key[i].split()[0]
        predLang = results[i].split()[0]
        if trueLang == "tl" and ignoretl:
            continue  # Don't let it be part of the calculation
        if predLang == trueLang:
            langs[trueLang]["TP"] += 1
        else:
            langs[trueLang]["FN"] += 1
            langs[predLang]["FP"] += 1
            matrix[trueLang][predLang] += 1
        if trueLang in counts:
            counts[trueLang] += 1
        else:
            counts[trueLang] = 1
        if (trueLang in rlang and predLang in rlang):
            romance["TP"] += 1
        elif (trueLang in glang and predLang in glang):
            germanic["TP"] += 1
        elif (trueLang in rlang and predLang in glang):
            romance["FN"] += 1
            germanic["FP"] += 1
        elif (trueLang in glang and predLang in rlang):
            germanic["FN"] += 1
            romance["FP"] += 1
        else:
            pass

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

    # Precision/Recall calculations for language groups
    print("       \t   Prec. \tRecall \tF1 Score")

    d = romance
    returned = d["TP"] + d["FP"]
    expected = d["TP"] + d["FN"]
    d["P"] = 0.0 if returned == 0 else d["TP"] / returned
    d["R"] = 0.0 if expected == 0 else d["TP"] / expected
    d["F1"] = 0.0 if d["P"] + d["R"] == 0 else 2 * d["P"] * d["R"] / (d["P"] + d["R"])
    print("%s \t%.3f \t%.3f \t%.3f" % ("romance", d["P"], d["R"], d["F1"]))

    d = germanic
    returned = d["TP"] + d["FP"]
    expected = d["TP"] + d["FN"]
    d["P"] = 0.0 if returned == 0 else d["TP"] / returned
    d["R"] = 0.0 if expected == 0 else d["TP"] / expected
    d["F1"] = 0.0 if d["P"] + d["R"] == 0 else 2 * d["P"] * d["R"] / (d["P"] + d["R"])
    print("%s \t%.3f \t%.3f \t%.3f" % ("germanic", d["P"], d["R"], d["F1"]))

    print("")

    predicted = "\t"
    for i in matrix:
        predicted = predicted + i + "\t"
    print(predicted)

    for i in matrix.keys():
        printstr = i + "\t"
        for j in matrix.keys():
            if counts[i] == 0:
                pass
            elif i == j:
                percent = (round((langs[i]["TP"]) / counts[i] * 10000)) / 100
                space = "\t" #* (7 - len(str(percent)))
                printstr += str(percent) + "%" + space
            else:
                percent = (round((matrix[i][j]) / counts[i] * 10000)) / 100
                space = "\t" #* (7 - len(str(percent)))
                printstr += str(percent) + "%" + space
        print(printstr)
    return weighted_f1

if __name__ == "__main__":
    main(raw_input("KEY file: "), raw_input("PREDICTIONS file: "))
