from collections import defaultdict # used to create a dictionary of lists

# recieve a list of transcripts in string form
# recieve the LIWC2015
# returns dictionary of category and the words that matched
def liwc_analysis(strIn, LIWCwords, LIWCroots):
    # of the form
    # {
    #     "RELIGION": ["allah", "agnost"],
    #     "OTHERCATEGORY": ["word"],
    # }
    results = defaultdict(list)
    strs = strIn.split(" ")
    for word in strs:
        if word in LIWCwords:
            # print(word)
            for category in LIWCwords[word]:
                results[category].append(word)
        else:
            wordLen = len(word)
            x = 0
            while x < wordLen:
                # len(word[:(-x)])/len(word) > .6 keeps word within 60% of original word
                # and len(word[:(-x)])/len(word) > .6
                if word[:(-x)] in LIWCroots:
                    print(word[:(-x)], word, LIWCroots[word[:(-x)]])
                    for category in LIWCroots[word[:(-x)]]:
                        results[category].append(word)
                    break
                x += 1

    return results


# return a dictionary with the category and the cooresponding count
def get_counts(dictionaryResults):
    counts = {}
    for category in dictionaryResults:
        counts[category] = len(dictionaryResults[category])
    return counts



# command line wrapper
# loads transcripts from file
# loads LIWC2015 from file
# strs is a list of the string representations of the transcripts
def liwc_analysis_driver(strs, LIWCLocation):
    LIWCwords = defaultdict(list)
    LIWCroots = defaultdict(list)

    # load LIWC2015
    # split into roots and words

    # comes in form:
    # afterlife* ,RELIG
    # agnost* ,RELIG
    # alla ,RELIG
    f = open(LIWCLocation, "r" )
    for line in f:
        text = line.split(" ,")[0]
        category = line.split(" ,")[1]
        if "*" in line:
            # root
            LIWCroots[text[:-1]].append(category)
        else:
            # word
            LIWCwords[text].append(category)
    f.close()

    # list of dictionarys containing category and cooresponding matching words for each transcript
    # {
    #     "RELIGION": ["allah", "etc"],
    # }
    resultsDics = []
    for str in strs:
        resultsDics.append(liwc_analysis(str, LIWCwords, LIWCroots))

    # list of dictionarys containing the category and cooresponding count
    # {
    #     "RELIGION": 5,
    # }
    countDics = []
    for dic in resultsDics:
        countDics.append(get_counts(dic))

    # print out counts
    # for index, dic in enumerate(countDics):
        # print(transcripts[index])
        # for category in dic:
            # print(category, dic[category])

    return resultsDics, countDics
