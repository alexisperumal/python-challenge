# Alexis Perumal, 11/20/19
# UCSD Data Science Bootcamp, HW#3, Extra Challenges, PyBoss (derived from PyPoll)
#
# Assignment:
#   In this challenge, you get to be the boss. You oversee hundreds of employees across the country developing Tuna 2.0,
#   a world-changing snack food based on canned tuna fish. Alas, being the boss isn't all fun, games, and
#   self-adulation. The company recently decided to purchase a new HR system, and unfortunately for you, the new system
#   requires employee records be stored completely differently.
#
#   Your task is to help bridge the gap by creating a Python script able to convert your employee records to the
#   required format. Your script will need to do the following:
#
#     • Import the employee_data.csv file, which currently holds employee records like the below:
#           Emp ID,Name,DOB,SSN,State
#           214,Sarah Simpson,1985-12-04,282-01-8166,Florida
#           15,Samantha Lara,1993-09-08,848-80-7526,Colorado
#           411,Stacy Charles,1957-12-20,658-75-8526,Pennsylvania
#
#     • Then convert and export the data to use the following format instead:
#           Emp ID,First Name,Last Name,DOB,SSN,State
#           214,Sarah,Simpson,12/04/1985,***-**-8166,FL
#           15,Samantha,Lara,09/08/1993,***-**-7526,CO
#           411,Stacy,Charles,12/20/1957,***-**-8526,PA
#
#     • In summary, the required conversions are as follows:
#           • The Name column should be split into separate First Name and Last Name columns.
#           • The DOB data should be re-written into MM/DD/YYYY format.
#           • The SSN data should be re-written such that the first five numbers are hidden from view.
#           • The State data should be re-written as simple two-letter abbreviations.
#
#    Special Hint: You may find this link to be helpful—Python Dictionary for State Abbreviations.
#           https://gist.github.com/afhaque/29f0f4f37463c447770517a6c17d08f5
#
# Version History:
#   • v1 (11/20/19) - Initial implementation, derived from PyPoll. It implements the assignment.
#

import os, csv, datetime

####################################################################################################################
# Useful Globals
####################################################################################################################

TITLE = "PyBoss-main.py"

INPUT_PATH = 'Resources'
INPUT_FILENAME = 'employee_data.csv'
OUTPUT_PATH = "Output"
OUTPUT_FILENAME = "pyBoss-output.csv"

EMP_ID_FIELD = 0
NAME_FIELD = 1
DOB_FIELD = 2
SSN_FIELD = 3
STATE_FIELD = 4

# From: https://gist.github.com/afhaque/29f0f4f37463c447770517a6c17d08f5
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

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

# Regenerate the record in the new format as a single string.
#           • The Name column should be split into separate First Name and Last Name columns.
#           • The DOB data should be re-written into MM/DD/YYYY format.
#           • The SSN data should be re-written such that the first five numbers are hidden from view.
#           • The State data should be re-written as simple two-letter abbreviations.
def repack_record(r):
    name = r[NAME_FIELD].split(" ")
    return str(f"{r[EMP_ID_FIELD]},"
               f"{name[0]},{name[1]},"
               f"{r[DOB_FIELD][5:7]}/{r[DOB_FIELD][-2:]}/{r[DOB_FIELD][:4]},"
               f"***-**-{r[SSN_FIELD][-4:]},"
               f"{us_state_abbrev[r[STATE_FIELD]]}")


def analyzeDataset():
    logpath = os.path.join('.', OUTPUT_PATH, OUTPUT_FILENAME)
    log = Log(logpath, overwrite=True)
    log.write(str(datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S %p %Z') + "Launching " + TITLE), indent=False, console_only=True)

    csvpath = os.path.join('.', INPUT_PATH, INPUT_FILENAME)
    csvfile = open(csvpath, newline='')

    # CSV reader specifies delimiter and variable that holds contents
    csvreader = csv.reader(csvfile, delimiter=',')

    # Read the header row first (skip this step if there is no header)
    csv_header = next(csvreader)

    # Write new header
    log.write("Emp_ID,First_Name,Last_name,DOB,SSN,STATE", indent=False)

    num_records = 0
    for record in csvreader:
        num_records += 1
        if num_records < 10:
            log.write(repack_record(record), indent=False)
        else:
            log.write(repack_record(record), indent=False, silent=True)

    log.write("Bye!", console_only=True)
    log.close()


def main():
    analyzeDataset()

if __name__ == '__main__':
    main()
