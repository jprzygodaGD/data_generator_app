import argparse
from unittest.mock import Mock, patch
import tempfile as tf
import pytest
from processor import ArgumentProcessor

"""Test if lines are printed if file_count argument is set to 0."""


@pytest.fixture
def arg_parser():
    temp_dir = tf.mkdtemp()
    m = Mock(return_value=argparse.Namespace(file_path=temp_dir, file_count=0, file_name="test", file_prefix="uuid",
                                             data_schema="{\"num\": \"int:rand(1, 9)\"}", data_lines=1, multiprocessing=1,
                                             clear_path=True))
    return ArgumentProcessor(m())


test_params = [
    (2, "{'num': 2}\n"),
    (5, "{'num': 5}\n")
]


@pytest.mark.parametrize("ran_int, expected", test_params)
@patch("processor.random.randint")
def test_print_lines(mocked_int, ran_int, expected, arg_parser, capfd):
    mocked_int.return_value = ran_int
    arg_parser.produce_output()
    out, err = capfd.readouterr()
    assert out == expected


