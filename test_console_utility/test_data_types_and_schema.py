import argparse
from unittest.mock import Mock, patch
import tempfile as tf
import pytest
import logging
from processor import ArgumentProcessor

"""Test generating data schemas and types from strings - generate data function."""


@pytest.fixture
def arg_parser():
    temp_dir = tf.mkdtemp()
    m = Mock(return_value=argparse.Namespace(file_path=temp_dir, file_count=3, file_name="filetest", file_prefix="uuid",
                                             data_schema="test_schema", data_lines=1, multiprocessing=1, clear_path=True))
    return ArgumentProcessor(m())


test_params_valid = [

    ({"date": "timestamp:", "type": "str:['client', 'partner', 'government']", "age": "int:rand(1, 90)", "name": "str:rand"},
     {"date": "1670832968.329983", "type": "client", "age": 40, "name": "9f9a3a31-fb90-4f89-9155-54af11c285a6"},
     1670832968.329983, "client", 40, "9f9a3a31-fb90-4f89-9155-54af11c285a6"),

    ({"date": "timestamp:", "type": "str:['client', 'partner', 'government']", "age": "int", "name": "str"},
     {"date": "1670837185.2241652", "type": "partner", "age": None, "name": ""},
     1670837185.2241652, "partner", None, ""),

    ({"date": "timestamp:", "type": "str:['client', 'partner', 'government']", "age": "int:90", "name": "str:cat"},
     {"date": "1534717898.442959", "type": "government", "age": 90, "name": "cat"},
     1534717898.442959, "government", 90, "cat"),

]

test_params_invalid = [

    ({"num": "int:cat"}, "This value cannot be converted to int"),
    ({"name": "str:rand(10, 100)"}, "Rand with range can be used only for integer data type"),
    ({"date": "timestamp:20.10"}, "Additional value cannot be provided for timestamp")
]

test_data_types = [
    ({"number": "float:rand", "choice": "int:['1', '2', '3']", "age": "int:rand(1, 90)"}, {"choice": "1", "age": 4},
     "Invalid data type", "1", 4),
    ({"choice": "list:cat", "name": "str:['Kate', 'John']", "age": "int:rand(1, 90)"}, {"name": "Kate", "age": 67},
     "Invalid data type", "Kate", 67),
    ({"choice": "list:cat", "name": "dict:['Kate', 'John']", "age": "float:rand(1, 90)"}, {},
     "Invalid data type", "Kate", 67)

]

LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize("input_schema, expected_schema, time, ran_choice, ran_int, str_uuid", test_params_valid)
@patch("processor.uuid.uuid4")
@patch("processor.random.randint")
@patch("processor.random.choice")
@patch("processor.time.time")
def test_generate_data_valid(mocked_time, mocked_choice, mocked_int, mocked_uuid, arg_parser,
                             input_schema, expected_schema, time, ran_choice, ran_int, str_uuid):
    mocked_time.return_value = time
    mocked_choice.return_value = ran_choice
    mocked_int.return_value = ran_int
    mocked_uuid.return_value = str_uuid

    result_schema = arg_parser.generate_data(input_schema)

    assert result_schema == expected_schema


@pytest.mark.parametrize("input_schema, log_message", test_params_invalid)
def test_generate_data_invalid(arg_parser, input_schema, log_message, caplog):
    with caplog.at_level(logging.ERROR):
        arg_parser.generate_data(input_schema)
    assert log_message in caplog.text


@pytest.mark.parametrize("input_schema, output_schema, log_message, choice, ran_int", test_data_types)
@patch("processor.random.randint")
@patch("processor.random.choice")
def test_generate_data_for_data_types(mocked_choice, mocked_int, input_schema, output_schema,
                                      log_message, choice, ran_int, arg_parser, caplog):
    mocked_choice.return_value = choice
    mocked_int.return_value = ran_int
    with caplog.at_level(logging.ERROR):
        result = arg_parser.generate_data(input_schema)
    assert log_message in caplog.text
    assert result == output_schema
