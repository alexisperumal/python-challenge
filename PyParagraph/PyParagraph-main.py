# Alexis Perumal, 11/22/19
# UCSD Data Science Bootcamp, HW#3, Extra Challenges, PyParagraph (derived from PyBoss)
#
# Assignment:
#
# In this challenge, you get to play the role of chief linguist at a local learning academy. As chief linguist, you are
# responsible for assessing the complexity of various passages of writing, ranging from the sophomoric Twilight novel to
# the nauseatingly high-minded research article. Having read so many passages, you've since come up with a fairly simple
# set of metrics for assessing complexity.
#
# Your task is to create a Python script to automate the analysis of any such passage using these metrics. Your script
# will need to do the following:
#   * Import a text file filled with a paragraph of your choosing.
#   * Assess the passage for each of the following:
#      * Approximate word count
#      * Approximate sentence count
#      * Approximate letter count (per word)
#      * Average sentence length (in words)
#      * As an example, this passage:
#
# “Adam Wayne, the conqueror, with his face flung back and his mane like a lion's, stood with his great sword point
# upwards, the red raiment of his office flapping around him like the red wings of an archangel. And the King saw, he
# knew not how, something new and overwhelming. The great green trees and the great red robes swung together in the
# wind. The preposterous masquerade, born of his own mockery, towered over him and embraced the world. This was the
# normal, this was sanity, this was nature, and he himself, with his rationality, and his detachment and his black
# frock-coat, he was the exception and the accident a blot of black upon a world of crimson and gold.”
#
# ...would yield these results:
# ```output
# Paragraph Analysis
# -----------------
# Approximate Word Count: 122
# Approximate Sentence Count: 5
# Average Letter Count: 4.6
# Average Sentence Length: 24.0
# ```
#
# * **Special Hint:** You may find this code snippet helpful when determining sentence length (look into
#     [regular expressions](https://en.wikipedia.org/wiki/Regular_expression) if interested in learning more):
#
# ```python
# import re
# re.split("(?<=[.!?]) +", paragraph)
# ```
#
# Version History:
#   • v1 (11/22/19) - Initial implementation, derived from PyBoss. It implements the assignment.
#

import os, datetime, re

####################################################################################################################
# Useful Globals
####################################################################################################################

TITLE = "PyParagraph-main.py"

INPUT_PATH = 'raw_data'
INPUT_FILENAME = 'paragraph_0.txt'
OUTPUT_PATH = "Output"
OUTPUT_FILENAME = "paragraph-log.txt"

class Log:
    def __init__(self, out_f, quiet=False, overwrite=False):
        self.write_to_file = len(out_f) != 0
        self.quiet = quiet
        if self.write_to_file:
            path_and_logfilename = out_f
            log_folder = os.path.dirname(path_and_logfilename)
            if not os.path.isdir(log_folder):
                os.makedirs(log_folder)
            if overwrite:
                self.logfile = open(path_and_logfilename, "w", encoding="utf-8")
            else:
                self.logfile = open(path_and_logfilename, "a", encoding="utf-8")

    def write(self, s, indent=True, force=False, console_only=False, silent=False):
        if ((not self.quiet) or force) and not silent:
            print(s)
        if self.write_to_file and not console_only:
            if indent:
                self.logfile.write('  ' + s + os.linesep)
            else:
                self.logfile.write(s + os.linesep)
            self.logfile.flush()

    def close(self):
        if self.write_to_file:
            self.logfile.close()



def analyzeProse(f, log):
    contents = f.read()

    # Extract sentences
    # Regex from: https://stackoverflow.com/questions/25735644/python-regex-for-splitting-text-into-sentences-sentence-tokenizing/25735848
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", contents)
    # sentences = contents.split(sep=".")
    num_sentences = len(sentences)

    # count words and letters
    num_words = 0
    num_letters = 0

    for s in sentences:
        num_words += len(s.split(" "))
        for c in s:
            if c.isalpha:
                num_letters += 1

    # Print the analysis results
    #      * Approximate word count
    #      * Approximate sentence count
    #      * Approximate letter count (per word)
    #      * Average sentence length (in words)
    log.write("Paragraph Analysis")
    log.write("-----------------")
    log.write(f"Approximate word count: {num_words}")
    log.write(f"Approximate sentence count: {num_sentences}")
    if num_words != 0:
        log.write("Approximate letter count (per word): %.02f" % (num_letters/num_words))
    else:
        log.write("Approximate letter count (per word): n/a (no words)")

    if num_sentences != 0:
        log.write("Approximate sentence length (in words): %.02f" % (num_words/num_sentences))
    else:
        log.write("Approximate sentence length (in words): n/a (no sentences)")

    log.write("")


def main():
    logpath = os.path.join('.', OUTPUT_PATH, OUTPUT_FILENAME)
    log = Log(logpath)
    log.write(str(datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S %p %Z') + "Launching " + TITLE), indent=False)

    input_file_path = os.path.join('.', INPUT_PATH, INPUT_FILENAME)
    log.write("Input file: %s" % input_file_path)
    log.write("Output log file: %s" % os.path.join('.', OUTPUT_PATH, OUTPUT_FILENAME))

    # f_in = open(input_file_path, newline='')
    f_in = open(input_file_path, "r")

    analyzeProse(f_in, log)

    f_in.close()

    log.write("Bye!", console_only=True)
    log.close()

if __name__ == '__main__':
    main()
