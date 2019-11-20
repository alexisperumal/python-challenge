# Alexis Perumal, 11/19/19
# UCSD Data Science Bootcamp, HW#3, Part 1, PyBank
#
# In this challenge, you are tasked with creating a Python script for analyzing the financial records of your company. You will give a set of financial data called budget_data.csv. The dataset is composed of two columns: Date and Profit/Losses. (Thankfully, your company has rather lax standards for accounting so the records are simple.)
#
# Your task is to create a Python script that analyzes the records to calculate each of the following:
#   • The total number of months included in the dataset
#   • The net total amount of "Profit/Losses" over the entire period
#   • The average of the changes in "Profit/Losses" over the entire period
#   • The greatest increase in profits (date and amount) over the entire period
#   • The greatest decrease in losses (date and amount) over the entire period
#
# As an example, your analysis should look similar to the one below: (see instructions)
#
# In addition, your final script should both print the analysis to the terminal and export a text file with the results.
#
# v1 (11/20/19) - Open the dataset csv file and read it into a list.
# v2 (11/20/19) - Since the results can be computed in one pass, don't store the dataset locally, just find the
#                 results we need and report them.

import os, csv, datetime

####################################################################################################################
# Useful Globals
####################################################################################################################

TITLE = "PyBank-main.py"


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
    logpath = os.path.join('.', 'Output', 'pyBank-analysis-output.txt')
    log = Log(logpath)
    log.write(str(datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S %p %Z') + "Launching " + TITLE), indent=False)

    csvpath = os.path.join('.', 'Resources', 'budget_data.csv')
    csvfile = open(csvpath, newline='')

    # CSV reader specifies delimiter and variable that holds contents
    csvreader = csv.reader(csvfile, delimiter=',')
    # print(csvreader)

    # Read the header row first (skip this step if there is no header)
    csv_header = next(csvreader)
    # print(f"CSV Header: {csv_header}")

    # Your task is to create a Python script that analyzes the records to calculate each of the following:
    #   • The total number of months included in the dataset
    #   • The net total amount of "Profit/Losses" over the entire period
    #   • The average of the changes in "Profit/Losses" over the entire period
    #   • The greatest increase in profits (date and amount) over the entire period
    #   • The greatest decrease in losses (date and amount) over the entire period

    # Declare necessary variables and initialize them based on the first record
    first_record = next(csvreader)  # [date, profit]
    num_months = 1
    total_profit = int(first_record[1])
    prior_profit = int(first_record[1])
    total_change = 0
    greatest_inc_mo = first_record[0]
    greatest_inc_amt = 0
    greatest_dec_mo = first_record[0]
    greatest_dec_amt = 0

    for record in csvreader:
        num_months += 1
        month = record[0]
        profit = int(record[1])
        # print(month, profit)
        total_profit += profit  # Accumulate total profit

        # Keep track of accumulated change in profit
        chg = (profit - prior_profit)
        total_change += chg
        prior_profit = profit  # setup for the next loop iteration calculation

        # Update if there is a new high or low
        if chg > greatest_inc_amt:
            greatest_inc_amt = chg
            greatest_inc_mo = month
        elif chg < greatest_dec_amt:
            greatest_dec_amt = chg
            greatest_dec_mo = month

    # Report the results
    log.write("Financial Analysis")
    log.write("----------------------------")
    log.write("Total Months: %d" % num_months)
    log.write("Total: $%d" % total_profit)
    log.write("Average Change: $%0.2f" % float(total_change / (num_months - 1)))
    log.write("Greatest Increase in Profits: %s ($%d)" % (greatest_inc_mo, greatest_inc_amt))
    log.write("Greatest Decrease in Profits: %s ($%d)" % (greatest_dec_mo, greatest_dec_amt))

    log.write("Bye!")
    log.close()


def main():
    analyzeDataset()

if __name__ == '__main__':
    main()