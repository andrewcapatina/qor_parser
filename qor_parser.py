"""
    Andrew Capatina

    Description:
        This script parses a QOR report and creates a comma seperated 
        list with values to be loaded into an excel spreadsheet. 

"""

import glob

num_hold_violation_str = 'No. of Hold Violations:'
total_hold_violation_str = 'Total Hold Violation:'
total_neg_slack_str = 'Total Negative Slack:'
wns_str = 'Critical Path Slack:'


def get_hold_times(qor_report):
    """
        Function to get worst hold time violations
        for each clock group.

        input: qor_report - text file containing contents 
                            to search for. 
        output: hold_times - times taken from report.
    """
    hold_times = []
    for line in qor_report:
        rtn = line.find(total_hold_violation_str)
        if rtn != -1:
            line = line.strip(total_hold_violation_str)
            line = line.strip()
            hold_times.append(line)

    return hold_times


def get_num_hold_violations(qor_report):
    """
        Function to get number of hold violations 
        for each clock path.

        input: qor_report - text file containing contents
                            to search for.
        output: num_hold_violations - list containing all hold violations.
    """
    num_hold_violations = []
    for line in qor_report:
        rtn = line.find(num_hold_violation_str)
        if rtn != -1:
            line = line.strip(num_hold_violation_str)
            line = line.strip()
            num_hold_violations.append(line)

    return num_hold_violations


def get_timing_paths(qor_report):
    """
        Function to parse and get all timing paths in the QOR report.

        input: qor_report - text file containing contents 
                            to search for. 

        output: timing_paths - timing paths of the current design.
    """
    timing_paths = []
    for line in qor_report:
        rtn = line.find('Timing Path Group')
        if rtn != -1:
            line = line.strip('Timing Path Group')
            line = line.strip("'")
            line = line.strip()
            line = line[:-1]
            timing_paths.append(line)

    return timing_paths


def get_tns(qor_report):
    """
        Function to get all total negative slack times in QOR.

        input: qor_report - list containing lines of file.
        output: tns_times - list containing times from file.
    """
    tns_times = []
    for line in qor_report:
        rtn = line.find(total_neg_slack_str)
        if rtn != -1:
            line = line.strip(total_neg_slack_str)
            line = line.strip()
            tns_times.append(line)

    return tns_times


def get_wns(qor_report):
    """
        Function to get all worst negative slack times from QOR.

        input: qor_report - list containing lines of file.
        output: wns_times - slack times.
    """
    wns_times = []
    for line in qor_report:
        rtn = line.find(wns_str)
        if rtn != -1:
            line = line.strip(wns_str)
            line = line.strip()
            wns_times.append(line)

    return wns_times


def read_file(file_path):
    """
        Function to read file and return the whole file.

        input: file_path - file path to qor files.
        output: qor_report - file contents returned.
    """
    with open(file_path) as fp:
        qor_report = fp.readlines()

    return qor_report


def main():
    for file_path in glob.glob("*qor*.rpt"):
        print("Parsing file " + file_path)
        qor_report = read_file(file_path)
        timing_paths = get_timing_paths(qor_report)
        wns_times = get_wns(qor_report)
        tns_times = get_tns(qor_report)
        hold_times = get_hold_times(qor_report)
        num_hold_violations = get_num_hold_violations(qor_report)
        print(num_hold_violations)



if __name__ == "__main__":
    main()