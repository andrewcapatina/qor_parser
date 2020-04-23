"""
    Andrew Capatina

    Description:
        This script parses a QOR report and creates a comma seperated 
        list with values to be loaded into an excel spreadsheet. 

"""

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
    print(timing_paths)



if __name__ == "__main__":
    main()