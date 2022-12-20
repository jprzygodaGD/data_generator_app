import pytest
import argparse
import os
import tempfile as tf
from unittest.mock import Mock
from processor import ArgumentProcessor

"""Test for clear path file that removes files with the same name from directory."""


@pytest.fixture
def arg_parser_empty():
    temp_dir = tf.mkdtemp()

    tf.mkstemp(suffix=".json", prefix="filetest", dir=temp_dir)
    tf.mkstemp(suffix=".json", prefix="filetest", dir=temp_dir)
    tf.mkstemp(suffix=".json", prefix="filetest", dir=temp_dir)

    m = Mock(return_value=argparse.Namespace(file_path=temp_dir, file_count=3, file_name="filetest",
             file_prefix="random", data_schema="{'test': 'int'}", data_lines=1,  multiprocessing=1, clear_path=True))
    return ArgumentProcessor(m())


@pytest.fixture
def arg_parser_not_empty():
    temp_dir = tf.mkdtemp()

    tf.mkstemp(suffix=".json", prefix="test", dir=temp_dir)

    m = Mock(return_value=argparse.Namespace(file_path=temp_dir, file_count=1, file_name="filetest",
             file_prefix="random", data_schema="{'test': 'int'}", data_lines=1,  multiprocessing=1, clear_path=True))
    return ArgumentProcessor(m())


def test_clear_path_not_empty(arg_parser_not_empty):
    """Test if directory is not empty for files with different file name. """

    arg_parser_not_empty.clear_path_with_filename()
    assert len(os.listdir(arg_parser_not_empty.path)) == 1


def test_clear_path_empty(arg_parser_empty):
    """Test if directory is empty for files with the same file name. """

    arg_parser_empty.clear_path_with_filename()
    assert len(os.listdir(arg_parser_empty.path)) == 0


