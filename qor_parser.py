"""
    Andrew Capatina

    Description:
        This script parses a QOR report and creates a comma seperated 
        list with values to be loaded into an excel spreadsheet. 

"""

import glob
import csv


hold_violation_str = "Worst Hold Violation:"
total_hold_violation_str = 'Total Hold Violation:'
total_neg_slack_str = 'Total Negative Slack:'
wns_str = 'Critical Path Slack:'


def get_hold_times(qor_report):
    """
        Function to get worst hold time violations
        for each clock group.

        input: qor_report - text file containing contents 
                            to search for. (list)
        output: hold_times - list of times taken from report.
    """
    hold_times = []
    for line in qor_report:
        rtn = line.find(total_hold_violation_str)
        if rtn != -1:
            line = line.strip(total_hold_violation_str)
            line = line.strip()
            hold_times.append(line)

    return hold_times


def get_timing_paths(qor_report):
    """
        Function to parse and get all timing paths in the QOR report.

        input: qor_report - text file containing contents 
                            to search for. (list) 

        output: timing_paths - list of timing paths of the current design.
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
        output: wns_times - list of slack times.
    """
    wns_times = []
    for line in qor_report:
        rtn = line.find(wns_str)
        if rtn != -1:
            line = line.strip(wns_str)
            line = line.strip()
            wns_times.append(line)

    return wns_times


def get_worst_hold_violation(qor_report):
    """
        Function to get worst hold violation time from qor.

        input: qor_report - List containing lines of file.
        output: worst_hold_vio - Worst hold violation list. 
    """
    worst_hold_vio = []
    for line in qor_report:
        rtn = line.find(hold_violation_str)
        if rtn != -1:
            line = line.strip(hold_violation_str)
            line = line.strip()
            worst_hold_vio.append(line)
    return worst_hold_vio


def read_file(file_path):
    """
        Function to read file and return the whole file.

        input: file_path - file path to qor files.
        output: qor_report - file contents returned.
    """
    with open(file_path) as fp:
        qor_report = fp.readlines()

    return qor_report


def write_to_csv(print_row):
    """
        Function to write the argument in a CSV file.

        input: print_row: list of lists containing timing and header information.
    """
    with open('report_qor_parsed.csv', 'w') as csvfile:
        qor_writer = csv.writer(csvfile)
        for row in print_row:
            qor_writer.writerow(row)


def main():
    for file_path in glob.glob("*qor*.rpt"):
        print("Parsing file " + file_path)
        qor_report = read_file(file_path)
        timing_paths = get_timing_paths(qor_report)
        wns_times = get_wns(qor_report)
        tns_times = get_tns(qor_report)
        worst_hold_vio = get_worst_hold_violation(qor_report)
        hold_times = get_hold_times(qor_report)

        timing_paths.insert(0,' ')
        wns_times.insert(0, wns_str)
        tns_times.insert(0, total_neg_slack_str)
        worst_hold_vio.insert(0, hold_violation_str)
        hold_times.insert(0, total_hold_violation_str)
        print_row = [timing_paths, wns_times, tns_times, 
                     worst_hold_vio, hold_times]
        
        write_to_csv(print_row)


if __name__ == "__main__":
    main()