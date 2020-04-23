"""
    Andrew Capatina

    Description:
        This script parses a QOR report and creates a comma seperated 
        list with values to be loaded into an excel spreadsheet. 

"""

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
        rtn = line.find('Total Hold Violation:')
        if(rtn != -1):
            line = line.strip('Total Hold Violation:')
            line = line.strip()
            hold_times.append(line)

    return hold_times


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
        rtn = line.find('Total Negative Slack:')
        if rtn != -1:
            line = line.strip('Total Negative Slack:')
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
        rtn = line.find('Critical Path Slack:')
        if rtn != -1:
            line = line.strip('Critical Path Slack:')
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
    print("Starting QOR parser.")

    file_path = "ORCA_TOP.cts2.qor.rpt"
    qor_report = read_file(file_path)
    timing_paths = get_timing_paths(qor_report)
    wns_times = get_wns(qor_report)
    tns_times = get_tns(qor_report)
    hold_times = get_hold_times(qor_report)
    print(hold_times)



if __name__ == "__main__":
    main()