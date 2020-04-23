"""
    Andrew Capatina

    Description:
        This script parses a QOR report and creates a comma seperated 
        list with values to be loaded into an excel spreadsheet. 

"""
def read_file(file_path):
    """
        Function to read file and return the whole file.

        input: file_path - file path to qor files.
        output: qor_report - file contents returned.
    """
    with open(file_path) as fp:
        qor_report = f.read()

    return qor_report


def main():
    print("Starting QOR parser.")

    file_path = ""
    qor_report = read_file(file_path)
    print(qor_report)


if __name__ == "__main__":
    main()