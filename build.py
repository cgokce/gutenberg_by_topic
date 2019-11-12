import json
import re
import codecs
import sys
import argparse

from gutenbergdammit.ziputils import searchandretrieve
#import wordfilter

def err(*args):
    print(*args, file=sys.stderr)

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--srczip",
        help="path to gutenberg-dammit-files zip",
        default="gutenberg-dammit-files-v002.zip")
parser.add_option("--topic",
        help="Selected book category to gather from Gutenberg Corpus. eg. poetry",
        default=None)
options, _ = parser.parse_args()

if not options.topic:
    print("\nBook category is not provided. Please run as following:")
    print("build.py --topic someBookCategory\n")
    sys.exit()


err("\nSelected topic is {}.".format(options.topic))

def clean(s):
    "removes leading numbers and trailing numbers with whitespace"
    match = re.search(r"( {3,}\d+\.?)$", s)
    if match:
        s = s[:match.start()]
    s = re.sub(r"\[\d+\]", "", s)
    return s

# Filter lines by following criteria

checks = {
    # between five and sixty-five characters (inclusive)
    'length': lambda prev, line: 5 <= len(line),# <= 65,
    # not all upper-case
    'case': lambda prev, line: not(line.isupper()),
    # doesn't begin with a roman numeral
    'not_roman_numerals': lambda prev, line: \
            not(re.search("^[IVXDC]+\.", line)),
    # if the last line was long and this one is short, it's probably the end of
    # a paragraph
    #'not_last_para_line': lambda prev, line: \
    #        not(len(prev) >= 65 and len(line) <= 65),
    # less than 25% of the line is punctuation characters
    #'punct': lambda prev, line: \
    #    (len([ch for ch in line if ch.isalpha() or ch.isspace()]) / \
    #        (len(line)+0.01)) > 0.75,
    # doesn't begin with a bracket (angle or square)
    'no_bracket': lambda prev, line: \
            not(any([line.startswith(ch) for ch in '[<'])),
    # isn't in title case
    'not_title_case': lambda prev, line: not(line.istitle()),
    # isn't title case when considering only longer words
    'not_mostly_title_case': lambda prev, line: \
        not(" ".join([w for w in line.split() if len(w) >= 4]).istitle()),
    # not more than 50% upper-case characters
    'not_mostly_upper': lambda prev, line: \
        (len([ch for ch in line if ch.isupper()]) / (len(line)+0.01)) < 0.5,
    # doesn't begin or end with a digit
    'not_number': lambda prev, line: \
            not(re.search("^\d", line)) and not(re.search("\d$", line)),
    # passes the wordfilter
    #'wordfilter_ok': lambda prev, line: not(wordfilter.blacklisted(line))
}


if __name__ == '__main__':

    # remove some terms from wordfilter because they were filtering large
    # numbers of inoffensive lines; added one because its presence in this
    # corpus is almost always questionable. (terms in rot13 as a kind of
    # content warning)
    #wordfilter.remove_words([codecs.encode(item, "rot_13") 
    #    for item in ['ynzr', 'pevc', 'tnfu', 'fcvp']])
    #wordfilter.add_words([codecs.encode("wrj", "rot_13")])


    err("finding books of ",options.topic," in", options.srczip, "...")

    books = list(searchandretrieve(options.srczip, {
            'Language': 'English',
            'Subject': lambda x: options.topic in x.lower(),
            'Copyright Status': lambda x: not(x.startswith("Copyrighted"))
    }))

    err("done.")
    err("finding lines in", len(books), "books of ",options.topic," ...")

    poem_lines = []
    line_count = 0
    for metadata, text in books:
        prev = ""
        for line in text.split("\n"):
            line = clean(line.strip())
            check_results = {k: v(prev, line) for k, v in checks.items()}
            if all(check_results.values()):
                poem_lines.append((line, metadata['Num']))
            line_count += 1
            prev = line

    err("done.")
    err("found", len(poem_lines), "lines matching the criteria, from ", line_count, "total.")

    outfile = open("dataset.txt", "w")
    err("printing to the dataset.txt file...")
    for line in poem_lines:
        outfile.write("{}\n".format(line[0]))

    outfile.close()
    err("done.\n")
