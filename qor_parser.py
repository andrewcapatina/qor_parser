"""
    Andrew Capatina
    Description:
        This script parses a QOR report and creates a comma seperated 
        list with values to be loaded into an excel spreadsheet. 
"""

import pandas as pd
import os
import csv


# Update the below global variables if qor.rpt or clock_qor.rpt
# file reporting format changes. 
hold_violation_str = "Worst Hold Violation:"
total_hold_violation_str = 'Total Hold Violation:'
total_neg_slack_str = 'Total Negative Slack:'
wns_str = 'Critical Path Slack:'

# Labels used for columns of clock_qor report.
column_labels_clock_qor = [ 'Sinks', 'Levels', 'Clock Repeater Count',
                            'Clock Repeater Area', 'Clock Stdcell Area', 'Max Latency',
                            'Global Skew', 'Trans DRC Count', 'Cap DRC Count']


def get_design(qor_report):
    """
        Function to get the current design being tested.
    """
    for line in qor_report:
        rtn = line.find(design_str)
        if rtn != -1:
            line = line.strip(design_str)
            line = line.strip()
            line = line.split()
            design = line

    return design


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


def parse_clock_qor(qor_report):
    """
        Function to parse clock_qor.
        input: qor_report: list containing report. 
    """
    clocks = []
    for line in qor_report:
        rtn = line.find('CLK')
        if rtn != -1:
            clocks.append(line)
       
    clock_qor = []
    for clock in clocks:
        clock = clock.split()
        if(len(clock) > 3): # This is done to filter out unneeded elements of list.
            clock_qor.append(clock)
    
    return clock_qor


def read_file(file_path):
    """
        Function to read file and return the whole file.
        input: file_path - file path to qor files.
        output: qor_report - file contents returned.
    """
    with open(file_path) as fp:
        qor_report = fp.readlines()

    return qor_report


def write_qor_to_csv(file_path, reports):
    """
        Function to write the argument in a CSV file.
        input: print_row: list of lists containing timing and header information.
    """
    
    with open(file_path + '_parsed.csv', 'w') as csvfile:
        qor_writer = csv.writer(csvfile)
        for report in reports:
            report = report.values.tolist()
            for row in report:
                qor_writer.writerow(row)

def format_clock_qor_data(clock_qor, timing_paths):
    """
        Function to remove any unneeded elements from 
        the clock_qor data set. 

        input: clock_qor: list containing clock_qor report.
        input: timing_paths: list containing all clock signals in design.

        output: list containing rows of information to be printed to CSV. 
    """
    output = []
    flag = False
    for timing_path in timing_paths:
        for row in clock_qor:
            if row[0] == timing_path:
                row = row[2:]
                output.append(row)
                flag = True
        if flag == False:
            row = row[2:]
            output.append(['-'])
        flag = False
    return output

def main():
    top_design = input("Please specify a top design. String only.\n")
   
    stages= ['syn', 'cts']
    reports=[]
    for stage in stages:

        to_open = top_design + "." + stage + ".qor.rpt"
        print("Parsing file " + to_open)
        qor_report = read_file(to_open)
        timing_paths = get_timing_paths(qor_report)
        wns_times = get_wns(qor_report)
        tns_times = get_tns(qor_report)
        worst_hold_vio = get_worst_hold_violation(qor_report)
        hold_times = get_hold_times(qor_report)


        to_open = top_design + "." + stage + ".clock_qor.rpt"
        print("Parsing file " + to_open)
        clock_qor = read_file(to_open)
        clock_qor = parse_clock_qor(clock_qor)

        clock_qor = format_clock_qor_data(clock_qor, timing_paths)

        current_stage = ["Stage: " + stage]
        timing_paths.insert(0, " ")
        wns_times.insert(0, "WNS Setup.")
        tns_times.insert(0, "TNS Setup.")
        worst_hold_vio.insert(0, "WNS hold")
        hold_times.insert(0, "TNS hold")

        clock_qor.insert(0, column_labels_clock_qor)
        clock_qor = pd.DataFrame(clock_qor)
        clock_qor = clock_qor.transpose()
        clock_qor = clock_qor.values.tolist()
        report_qor = [current_stage, timing_paths, wns_times, tns_times, 
                        worst_hold_vio, hold_times]
        for row in clock_qor:
            report_qor.append(row)
        report_qor = pd.DataFrame(report_qor)

        print(report_qor)
        report_qor = report_qor.transpose()
        reports.append(report_qor)

        print(report_qor)


    write_qor_to_csv(to_open, reports)


if __name__ == "__main__":
    main()