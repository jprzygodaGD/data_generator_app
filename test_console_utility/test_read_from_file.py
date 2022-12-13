import argparse
from unittest.mock import Mock
import tempfile as tf
import pytest
import json
from processor import ArgumentProcessor

"""Test loading schema from file."""


@pytest.fixture
def arg_parser():

    # prepare files and contents
    temp_dir_1 = tf.mkdtemp()
    temp_dir_2 = tf.mkdtemp()

    json_data = {
        "date": "timestamp:",
        "name": "str:rand",
        "type": "str:['client', 'partner', 'government']",
        "age": "int:rand(1, 90)"
    }

    _, test_file = tf.mkstemp(suffix=".json", prefix="filetest", dir=temp_dir_2)

    with open(test_file, "w") as opened_file:
        json.dump(json_data, opened_file)

    m = Mock(return_value=argparse.Namespace(file_path=temp_dir_1, file_count=3, file_name="filetest",
             file_prefix="random", data_schema=f"{test_file}", data_lines=1,  multiprocessing=1, clear_path=True))

    return ArgumentProcessor(m())


def test_read_from_file_valid(arg_parser):

    expected_schema = {
        "date": "timestamp:",
        "name": "str:rand",
        "type": "str:['client', 'partner', 'government']",
        "age": "int:rand(1, 90)"
    }
    result_schema = arg_parser.load_data_schema()
    assert result_schema == expected_schema
