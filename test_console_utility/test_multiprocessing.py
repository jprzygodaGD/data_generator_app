import argparse
from unittest.mock import Mock
import tempfile as tf
import os
import pytest
from processor import ArgumentProcessor

"""Test number of created files while using more than one CPU."""


@pytest.fixture
def arg_parser():
    temp_dir = tf.mkdtemp()
    m = Mock(return_value=argparse.Namespace(file_path=temp_dir, file_count=100, file_name="filetest", file_prefix="uuid",
                                             data_schema="{\"age\": \"int:rand(1, 90)\"}", data_lines=1,
                                             multiprocessing=8, clear_path=True))
    return ArgumentProcessor(m())


def test_multiprocessing(arg_parser):
    arg_parser.produce_output()

    file_counter = 0
    for _ in os.listdir(arg_parser.path):
        file_counter += 1
    assert file_counter == 100


