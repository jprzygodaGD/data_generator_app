import pytest
import argparse
import os
import tempfile as tf
from unittest.mock import Mock
from processor import ArgumentProcessor

"""Test handling absolute, relative and invalid file paths."""


TEST_DIR_1 = tf.mkdtemp()
TEST_DIR_2 = "test_output"

test_params_valid = [
    (TEST_DIR_1, TEST_DIR_1),
    (TEST_DIR_2, os.path.join(getcwd(), TEST_DIR_2)),
    (".", os.getcwd())
]


@pytest.mark.parametrize("path, expected", test_params_valid)
def test_process_file_path_valid(path, expected):

    m = Mock(return_value=argparse.Namespace(file_path=path, file_count=100, file_name="filetest", file_prefix="uuid",
                                             data_schema="{\"age\": \"int:rand(1, 90)\"}", data_lines=1,
                                             multiprocessing=1, clear_path=True))
    arg_parser = ArgumentProcessor(m())
    result = arg_parser.process_file_path(path)
    assert result == expected


def test_process_file_path_invalid():
    m = Mock(return_value=argparse.Namespace(file_path="invalid/path", file_count=100, file_name="filetest",
                                             file_prefix="uuid", data_schema="{\"age\": \"int:rand(1, 90)\"}",
                                             data_lines=1, multiprocessing=1, clear_path=True))
    with pytest.raises(SystemExit) as exit_raised:
        ArgumentProcessor(m())
    assert exit_raised.type == SystemExit







