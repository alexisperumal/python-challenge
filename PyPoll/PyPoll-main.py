# Alexis Perumal, 11/20/19
# UCSD Data Science Bootcamp, HW#3, Part 1, PyPoll (derived from PyBank)
#
# Assignment:
#   In this challenge, you are tasked with helping a small, rural town modernize its vote-counting process. (Up until
#   now, Uncle Cleetus had been trustfully tallying them one-by-one, but unfortunately, his concentration isn't what it
#   used to be.)
#
#   You will be give a set of poll data called election_data.csv. The dataset is composed of three columns: Voter ID,
#   County, and Candidate. Your task is to create a Python script that analyzes the votes and calculates each of the
#   following:
#     • The total number of votes cast
#     • A complete list of candidates who received votes
#     • The percentage of votes each candidate won
#     • The total number of votes each candidate won
#     • The winner of the election based on popular vote.
#
#   As an example, your analysis should look similar to the one below: (see instructions)
#
#   In addition, your final script should both print the analysis to the terminal and export a text file with the results.
#
# Version History:
#   • v1 (11/20/19) - Initial implementation, derived from PyBank.
#

import os, csv, datetime

####################################################################################################################
# Useful Globals
####################################################################################################################

TITLE = "PyPoll-main.py"

INPUT_PATH = 'Resources'
INPUT_FILENAME = 'election_data.csv'
OUTPUT_PATH = "Output"
OUTPUT_FILENAME = "pyPoll-analysis-output.txt"

VOTER_ID_FIELD = 0
COUNTY_FIELD = 1
CANDIDATE_FIELD = 2


class Log:
    def __init__(self, out_f, quiet=False):
        self.write_to_file = len(out_f) != 0
        self.quiet = quiet
        if self.write_to_file:
            path_and_logfilename = out_f
            log_folder = os.path.dirname(path_and_logfilename)
            if not os.path.isdir(log_folder):
                os.makedirs(log_folder)
            self.logfile = open(path_and_logfilename, "a", encoding="utf-8")

    def write(self, s, indent=True, force=False):
        if (not self.quiet) or force:
            print(s)
        if self.write_to_file:
            if indent:
                self.logfile.write('  ' + s + os.linesep)
            else:
                self.logfile.write(s + os.linesep)
            self.logfile.flush()

    def close(self):
        if self.write_to_file:
            self.logfile.close()



def analyzeDataset():
    logpath = os.path.join('.', OUTPUT_PATH, OUTPUT_FILENAME)
    log = Log(logpath)
    log.write(str(datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S %p %Z') + "Launching " + TITLE), indent=False)

    csvpath = os.path.join('.', INPUT_PATH, INPUT_FILENAME)
    csvfile = open(csvpath, newline='')

    # CSV reader specifies delimiter and variable that holds contents
    csvreader = csv.reader(csvfile, delimiter=',')
    # print(csvreader)

    # Read the header row first (skip this step if there is no header)
    csv_header = next(csvreader)
    # log.write(f"CSV Header: {csv_header}")

    #   You will be give a set of poll data called election_data.csv. The dataset is composed of three columns: Voter ID,
    #   County, and Candidate. Your task is to create a Python script that analyzes the votes and calculates each of the
    #   following:
    #     • The total number of votes cast
    #     • A complete list of candidates who received votes
    #     • The percentage of votes each candidate won
    #     • The total number of votes each candidate won
    #     • The winner of the election based on popular vote.

    # Declare necessary variables and initialize them based on the first record
    first_record = next(csvreader)  # [date, profit]
    num_records = 1

    candidates = {}

    for record in csvreader:
        num_records += 1

        #Add the vote into the candidate dictionary.
        candidates.setdefault(record[CANDIDATE_FIELD], 0)
        candidates[record[CANDIDATE_FIELD]] += 1

    # Report the results
    log.write("Election Results")
    log.write("----------------------------")
    log.write("Total Votes: %d" % num_records)
    log.write("----------------------------")

    # Print Election results by candidate, sorted by value (descending)
    for candidate in sorted(candidates.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
        log.write(candidate[0] + ": %0.3f%% (%d)" % (float(100.0*candidate[1])/float(num_records), candidate[1]))

    log.write("----------------------------")
    log.write("Winner: %s" % sorted(candidates.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)[0][0])
    log.write("----------------------------")

    log.write("Bye!")
    log.close()


def main():
    analyzeDataset()

if __name__ == '__main__':
    main()