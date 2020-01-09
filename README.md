# liwc-analysis
This package serves as a driver for the LIWC2015 .txt dictionary. The dictionary is not included and can be purchased directly from LIWC.

## Usage
The usage is fairly straight forward. First import the package
```python
import liwcanalysis
```

Then you need to create an instance of the LIWC analysis with the path to the .txt file.
```python
LIWCLocation = "/Users/Eric/repositories/transcript-analysis/LIWC/LIWC.2015.all.txt"
LIWC = liwcanalysis.liwc(LIWCLocation)
```

Then you can pass in a list of strings to analyze to receive a tuple of results dictionary and count dictionary.
```python
transcripts = {
    "Example1": "This is a single transcript. Red hat angry.",
    "Example2": "This is another single transcript. Dog boy cat.",
}

str_list = []
for key in transcripts:
    str_list.append(transcripts[key])

result_dics, count_dics = LIWC.analyze(str_list)
```

Please note that `analyze()` can take either a single string argument or a list of strings. Example:
```python
# this is valid
result_dics, coutn_dics = LIWC.analyze(["this is a string", "here is another", "one more"])
# this is also valid
result_dics, coutn_dics = LIWC.analyze("this is a string")
```

`result_dics` is a list of dictionaries. Each dictionary corresponds to one of the strings passed into `analyze`. Each dictionary follows the form of `"LIWC Category": [list, of, words, matched]`. For instance the dictionary for one string might look something like:
```
{
    "FUNCTION": ["is", "a"],
    "QUANT": ["single"],
    ...
}
```

`count_dics` is very similar to `result_dics`, but instead of giving a list of words matched, it gives the length of each list of words matched:
```
{
    "FUNCTION": 2,
    "QUANT": 1,
    ...
}
```

Finally, you can print out the results to csv using:
```python
LIWC.print(output_dir, titles)
```
You need to specify the output directory, as well as a list of titles for each string. See the full example for more details.

You can also retrieve an alphabetically sorted (A->Z) list of LIWC categories using `LIWC.get_categories()`.

## FAQ
### Where is LIWC2015.txt?
You need to supply this yourself. For legal reasons, I am unable to provide you with this.

### I don't have a LIWC2015.txt file. How do I create one?
You will first need to buy access to LIWC from [here](https://liwc.wpengine.com/).

Then, you can export the dictionary as a PDF. You can then convert the pdf table to csv with [tabula](https://tabula.technology/). I’ve used it in the past and it works very well. Once you download the table it should be pretty straightforward to convert it into the correct dictionary form.

I’m assuming you will get a csv file of the form:

> category, category1, category2
word1, word2, word3,
word4, word5, word6,
word7, word8, word9,

Here is an excerpt from my dictionary so you know what the format should look like:
> young ,ADJ
younger ,ADJ
youngest ,ADJ
yummy ,ADJ
about ,PREP
above ,PREP
abt ,PREP
...
after ,PREPS
against ,PREPS
ahead ,PREPS
along ,PREPS
among* ,PREPS


The * denotes that something is a root of a word. For instance, “among*" means thats “among" will be matched in “amongst”.

Included in the repo is a file (`convert_liwc_pdf_to_txt_dict.py`) that with some modification (see the TODO’s) should convert the csv created by Tabula to the correct format. Make sure to edit the file and insert the correct file paths (see the TODO in the file).   

## Full Example
```python
import liwcanalysis

transcripts = {
    "Example1": "This is a single transcript. Red hat angry.",
    "Example2": "This is another single transcript. Dog boy cat.",
}

str_list = []
for key in transcripts:
    strs.append(transcripts[key])

LIWCLocation = "/Users/Downloads/LIWC/LIWC.2015.all.txt"
output_dir = "/Path/to/my/file/"

LIWC = liwcanalysis.liwc(LIWCLocation)
result_dics, count_dics = LIWC.analyze(str_list)
LIWC.print(output_dir, list(transcript.keys()))
```
Using print will return the following tables:
/Path/to/my/file/LIWCcounts.csv:

| Category      | Example1 | Example2 |
|---------------|----------|----------|
| ADJ           | 1        | 1        |
| ARTICLE       | 1        |          |
| AUXVERB       | 1        | 1        |
| FOCUSPRESENT  | 1        | 1        |
| FUNCTION      | 2        | 2        |
| IPRON         |          | 1        |
| MALE          |          | 1        |
| NUMBER        | 1        | 1        |
| PRONOUN       |          | 1        |
| QUANT         | 1        | 2        |
| SOCIAL        |          | 1        |
| VERB          | 1        | 1        |
| WORK          | 1        | 1        |
| TOTAL         | 8        | 8        |

/Path/to/my/file/LIWCwords.csv:

| Category      | Example1        | Example2              |
|---------------|-----------------|-----------------------|
| ADJ           | ['single']      | ['single']            |
| ARTICLE       | ['a']           |                       |
| AUXVERB       | ['is']          | ['is']                |
| FOCUSPRESENT  | ['is']          | ['is']                |
| FUNCTION      | ['is', 'a']     | ['is', 'another']     |
| IPRON         |                 | ['another']           |
| MALE          |                 | ['boy']               |
| NUMBER        | ['single']      | ['single']            |
| PRONOUN       |                 | ['another']           |
| QUANT         | ['single']      | ['another', 'single'] |
| SOCIAL        |                 | ['boy']               |
| VERB          | ['is']          | ['is']                |
| WORK          | ['transcript.'] | ['transcript.']       |

/Path/to/my/file/LIWCrelativefreq.csv

| Category      | Example1 | Example2 |
|---------------|----------|----------|
| ADJ           | 0.125    | 0.125    |
| ARTICLE       | 0.125    |          |
| AUXVERB       | 0.125    | 0.125    |
| FOCUSPRESENT  | 0.125    | 0.125    |
| FUNCTION      | 0.25     | 0.25     |
| IPRON         |          | 0.125    |
| MALE          |          | 0.125    |
| NUMBER        | 0.125    | 0.125    |
| PRONOUN       |          | 0.125    |
| QUANT         | 0.125    | 0.25     |
| SOCIAL        |          | 0.125    |
| VERB          | 0.125    | 0.125    |
| WORK          | 0.125    | 0.125    |

Please let me know if you have any questions or features requests. Please feel free to open up a pull request or issue.
