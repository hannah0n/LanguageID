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

    print("Lang \tPrec. \trecall \tF1 Score")
    for lang in langs:
        d = langs[lang]
        returned = d["TP"] + d["FP"]
        expected = d["TP"] + d["FN"]
        d["P"] = 0.0 if returned == 0 else d["TP"] / returned
        d["R"] = 0.0 if expected == 0 else d["TP"] / expected
        d["F1"] = 0.0 if d["P"] + d["R"] == 0 else (2 * d["P"] * d["R"]) / (d["P"] + d["R"])
        print("%s \t%.2f \t%.2f \t%.2f" % (lang, d["P"], d["R"], d["F1"]))

    print()
    print("Average P: %.2f Average R: %.2f Average F1: %.2f" 
            % (sum([l["P"] for l in langs.values()]) / len(langs),
               sum([l["R"] for l in langs.values()]) / len(langs),
               sum([l["F1"] for l in langs.values()]) / len(langs)))

if __name__ == "__main__":
    main()
