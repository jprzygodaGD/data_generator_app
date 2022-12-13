import argparse
from configparser import ConfigParser


def collect_args():
    """Collect arguments provided in the command-line. If optional arguments are not provided use default.ini file"""

    config = ConfigParser()
    config.read("default.ini")

    parser = argparse.ArgumentParser(prog="data_generator",
                                     description=__doc__,
                                     add_help=True)
    parser.add_argument("file_path", help="Provide path to an existing directory", default=config["DEFAULT"]["file_path"])
    parser.add_argument("--file_count", help="Number of files to be created, default 0 prints data in the console",
                        type=int, default=config["DEFAULT"]["file_count"])
    parser.add_argument("--file_name", help="Default name: file", type=str, default=config["DEFAULT"]["file_name"])
    parser.add_argument("--file_prefix", help="Choose an option to create file prefixes",
                        choices=["count", "random", "uuid"], default=config["DEFAULT"]["file_prefix"])
    parser.add_argument("--data_schema", help="Provide data schema either in terminal or path to file")
    parser.add_argument("--data_lines", help="Specify how many lines should be generated",
                        type=int, default=config["DEFAULT"]["data_lines"])
    parser.add_argument("--clear_path", help="If flag is on all files with the same name file name and in the same "
                        "directory will be removed", action="store_true")
    parser.add_argument("--multiprocessing", help="Define how many processors should be used to generate file",
                        type=int, default=config["DEFAULT"]["multiprocessing"])
    return parser.parse_args()

