# -*- coding: utf-8 -*-
"""Convert liwc pdf csv to txt dictionary
"""

import operator

# TODO: update these paths
CSV_FILE_PATH = 'INPUT_PATH.csv'
OUTPUT_TXT_DICT_PATH = 'OUTPUT_PATH.txt'
# END TODO

# load file and save contents to text variable
rows = []
#filepath = 'YOUR_CSV_FILE_PATH_HERE.csv'
filepath = 'test.csv'
with open(filepath) as fp:
    for line in fp:
       rows.append(line)

grid = [row.split(", ") for row in rows if len(row) > 1]

tuples = []
for r in range(1, len(grid)):
    for c in range(0, len(grid[0])):
        tuples.append((grid[r][c].strip(), grid[0][c].strip()))


tuples.sort(key=operator.itemgetter(1, 0))

# write to file
with open(OUTPUT_TXT_DICT_PATH, 'w') as f:
    for (word, category) in tuples:
        f.write("{} ,{}\n".format(word, category))
