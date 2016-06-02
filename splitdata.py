# Use this script to divide the data into Training set, Dev set, and Test set

from random import randint

def main():
    # Ignoring tagalog for stage 1
    langs = "ca da de en es fr is it la no nl pt ro sv".split()
    trainf = open("training.txt", "w")
    testf = open("test.txt", "w")
    devf = open("dev.txt", "w")
    for lang in langs:
        with open("data/%s.txt" % lang) as f:
            if lang == "tl":
                for l in f:
                    n = randint(1, 10)
                    # In stage 1 we are not concerned with identifying Tagalog
                    testf.write(lang + "\t" + l)
            else:
                for l in f:
                    n = randint(1, 10)
                    if n >= 8:
                        testf.write(lang + "\t" + l)
                    elif randint(1, 10) >= 8:
                        devf.write(lang + "\t" + l)
                    else:
                        trainf.write(lang + "\t" + l)
    trainf.close()
    testf.close()
    devf.close()

if __name__ == "__main__":
    main()
