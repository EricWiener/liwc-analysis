from collections import defaultdict  # used to create a dictionary of lists
import pandas as pd
import os


class liwc:
    def __init__(self, liwc_file_path):
        liwc_words = defaultdict(list)
        liwc_roots = defaultdict(list)

        # load LIWC2015
        # split into roots and words

        # comes in form:
        # afterlife* ,RELIG
        # agnost* ,RELIG
        # alla ,RELIG
        f = open(liwc_file_path, "r")
        for line in f:
            text = line.split(" ,")[0]
            category = line.split(" ,")[1]
            if "*" in line:
                # root
                liwc_roots[text[:-1]].append(category)
            else:
                # word
                liwc_words[text].append(category)
        f.close()

        self.words = liwc_words
        self.roots = liwc_roots
        self.result_dics = []
        self.count_dics = []
        # self.results = defaultdict(list)

    # recieves list of transcripts in string form
    def analyze(self, transcripts):
        # reset values
        self.result_dics = []
        self.count_dics = []
        self.lengths = []

        # loop through all transcripts
        for transcript in transcripts:
            self.result_dics.append(self._analysis_helper(transcript))

        # list of dictionarys containing the category and cooresponding count
        # {
        #     "RELIGION": 5,
        # }
        for dic in self.result_dics:
            self.count_dics.append(self._get_counts(dic))

        # print out counts
        # for index, dic in enumerate(countDics):
            # print(transcripts[index])
            # for category in dic:
            # print(category, dic[category])

        return self.result_dics, self.count_dics

    # return a dictionary with the category and the cooresponding count
    # internal use only
    def _get_counts(self, result_dic):
        counts = {}
        for category in result_dic:
            counts[category] = len(result_dic[category])
        return counts

    # recieve a single transcript in string form
    # recieve the LIWC2015
    # returns dictionary of category and the words that matched
    # internal use only
    def _analysis_helper(self, str_in):
        results = defaultdict(list)
        # of the form
        # {
        #     "RELIGION": ["allah", "agnost"],
        #     "OTHERCATEGORY": ["word"],
        # }

        strs = str_in.split(" ")
        self.lengths.append(len(strs))
        for word in strs:
            if word in self.words:
                for category in self.words[word]:
                    results[category].append(word)
            else:
                wordLen = len(word)
                x = 0
                while x < wordLen:
                    # len(word[:(-x)])/len(word) > .6 keeps word within 60% of original word
                    # and len(word[:(-x)])/len(word) > .6
                    if word[:(-x)] in self.roots:
                        # print(word[:(-x)], word, self.roots[word[:(-x)]])
                        for category in self.roots[word[:(-x)]]:
                            results[category].append(word)
                        break
                    x += 1

        return results

    # print out files to csv
    def print(self, output_dir, titles):
        if output_dir is "":
            raise ValueError("Output directory not specified")
        if len(titles) != len(self.count_dics):
            raise ValueError("Invalid number of titles")
        if len(self.lengths) == 0:
            raise ValueError("No transcripts analyzed")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # add total word counts to count_dics
        lengths_for_csv = [{"TOTALWORDS": length} for length in self.lengths]

        pd.DataFrame(self.count_dics).T.append(pd.DataFrame(lengths_for_csv).T).reset_index().to_csv(
            output_dir + 'LIWCcounts.csv', header=["Category"] + titles)

        # results dic (words for each category)
        pd.DataFrame(self.result_dics).T.reset_index().to_csv(
            output_dir + 'LIWCwords.csv', header=["Category"] + titles)

        # relative frequency
        relative_freq_dics = []
        for index, dic in enumerate(self.count_dics):
            temp_dic = defaultdict(int)
            for category in dic:
                temp_dic[category] = dic[category] / self.lengths[index]
            relative_freq_dics.append(temp_dic)

        pd.DataFrame(relative_freq_dics).T.reset_index().round(4).to_csv(
            output_dir + 'LIWCrelativefreq.csv', header=["Category"] + titles)
