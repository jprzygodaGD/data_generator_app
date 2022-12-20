# Data Generator App

Application generates test data in JSON fromat in a specified schema.


## Usage: <br />
1. python3 -m pip install .
2. data_generator [-h] [--file_count FILE_COUNT] [--file_name FILE_NAME] [--file_prefix {count,random,uuid}] [--data_schema DATA_SCHEMA] 
[--data_linesDATA_LINES] [--clear_path] [--multiprocessing MULTIPROCESSING] file_path
3. If data_generator is not recognized execute:
export PYTHONPATH=path_to_data_generator_app

## Contents: <br />
- app.py - main module
- parser.py - reads arguments from command line and if optional ones are not provided than it replaces them defaults from default.ini file
- processor.py - proccesses arguments according to specified data schema
