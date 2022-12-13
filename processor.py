import argparse
import math
import os
import logging
import sys
import uuid
import random
import json
import time
import multiprocessing
logging.getLogger().setLevel(logging.INFO)


class ArgumentProcessor:
    """Process collected arguments, check their validity and produce output test data."""

    def __init__(self, args: argparse.Namespace):
        self.args_dict = vars(args)
        self.path = self.process_file_path(self.args_dict['file_path'])
        self.file_count = self.args_dict["file_count"]
        if self.file_count < 0:
            logging.error("Number of files cannot be a negative value")
            sys.exit()
        self.file_name = self.args_dict["file_name"]
        self.file_prefix = self.args_dict["file_prefix"]
        self.data_schema = self.args_dict["data_schema"]
        self.data_lines = self.args_dict["data_lines"]
        self.multiprocessing = self.args_dict["multiprocessing"]
        if self.multiprocessing < 0:
            logging.error("Number of processor cannot be a negative value")
            sys.exit()
        elif self.multiprocessing > os.cpu_count():
            self.multiprocessing = os.cpu_count()
        self.clear_path = self.args_dict['clear_path']

    def __repr__(self):
        return f"{self.args_dict}"

    @staticmethod
    def process_file_path(file_path):
        """Checks if path is a valid directory."""

        if file_path == '.':
            output_dir_path = os.getcwd()
        elif file_path.startswith('/'):
            output_dir_path = file_path
        else:
            output_dir_path = os.getcwd() + '/' + file_path

        # check if path exists
        if os.path.isdir(output_dir_path):
            return output_dir_path
        else:
            # log error message and exit
            logging.error("Specified path is not a directory")
            sys.exit(1)

    @staticmethod
    def generate_data(schema):
        """Generate a single line corresponding to the data schema."""

        json_dict = {}

        for key, value in schema.items():
            values = value.split(":")
            data_type = values[0]

            # check if schema contains only possible data types
            if data_type not in ['timestamp', 'int', 'str']:
                logging.error("Invalid data type")
                continue
            else:
                # handle standalone values
                if data_type == "timestamp":
                    json_dict[key] = str(time.time())
                elif data_type == "int":
                    json_dict[key] = None
                elif data_type == "str":
                    json_dict[key] = ""

                # process parameters with additional information about data
                if len(values) > 1:
                    additional_data_info = values[1]

                    if data_type == "timestamp" and additional_data_info != "":
                        logging.error("Additional value cannot be provided for timestamp")
                    elif data_type == "str" and additional_data_info == "rand":
                        json_dict[key] = str(uuid.uuid4())
                    elif data_type == "int" and additional_data_info == "rand":
                        json_dict[key] = str(random.randint(1, 1000))
                    elif additional_data_info.startswith("[") and additional_data_info.endswith("]") and data_type in ("str", "int"):
                        data_list = additional_data_info.lstrip("[").rstrip("]").split(", ")
                        choice = random.choice(data_list).lstrip("'").rstrip("'")
                        json_dict[key] = choice
                    elif data_type == "int" and additional_data_info.startswith("rand("):
                        edge_values = additional_data_info.split("(")[1]
                        a = int(edge_values[0])
                        b = int(edge_values.split(",")[1].strip(")").lstrip(" "))
                        json_dict[key] = random.randint(a, b)
                    elif data_type == "str" and additional_data_info.startswith("rand("):
                        logging.error("Rand with range can be used only for integer data type")
                    elif data_type == "int" and additional_data_info.isdigit():
                        json_dict[key] = int(additional_data_info)
                    elif data_type == "int" and not additional_data_info.isdigit():
                        logging.error("This value cannot be converted to int")
                    elif data_type == "str" and not additional_data_info.isdigit():
                        json_dict[key] = additional_data_info

        return json_dict

    def load_data_schema(self):
        """Reads JSON schema either from a file or directly from string."""

        if os.path.isfile(self.data_schema):
            # open and read JSON
            file = open(self.data_schema)
            schema = json.load(file)
        elif self.data_schema.startswith("/") and not os.path.isfile(self.data_schema):
            logging.error("Invalid path to data schema")
            sys.exit()
        else:
            # read schema from string
            schema = json.loads(self.data_schema)
        return schema  # returns Python dict

    def clear_path_with_filename(self):
        """Clear files with the same name in output directory."""

        for file in os.listdir(self.path):
            if file.startswith(self.file_name):
                file_to_delete = os.path.join(self.path, file)
                os.remove(file_to_delete)

    def create_files(self, num_files, schema):
        """Helper function to create files while using multiprocessing."""

        for i in range(num_files):
            if self.file_prefix == "count":
                prefix_value = i
            elif self.file_prefix == "random":
                prefix_value = random.randint(1, self.file_count * 100)
            elif self.file_prefix == "uuid":
                prefix_value = uuid.uuid4()
            else:
                prefix_value = ""

            with open(f"{self.path}/{self.file_name}{prefix_value}.json", "w") as current_opened_file:
                for j in range(self.data_lines):
                    current_opened_file.write("{")
                    line = self.generate_data(schema)
                    for key, value in line.items():
                        current_opened_file.write(f'"{key}": "{value}", ')
                    current_opened_file.write('},\n')

    def produce_output(self):
        """Writes generated lines to file or prints them."""

        data_schema = self.load_data_schema()

        if self.clear_path:
            self.clear_path_with_filename()

        if self.file_count > 0:
            logging.info("Started to generate files")
            max_tasks = math.ceil(self.file_count / self.multiprocessing)
            with multiprocessing.Pool(self.multiprocessing) as pool:
                _ = pool.starmap(self.create_files, [(self.file_count, data_schema)], chunksize=max_tasks)
            logging.info("Generating files is now finished")

        else:
            logging.info("Printing generated data ...")
            for j in range(self.data_lines):
                line = self.generate_data(data_schema)
                print(line)
            logging.info("All lines are now printed")
