"""
test_etl_job.py
~~~~~~~~~~~~~~~

This module contains unit tests for the transformation steps of the ETL
job defined in etl_job.py. It makes use of a local version of PySpark
that is bundled with the PySpark package.
"""
import pytest
from os import listdir

from src.pysparkwheelexample.jobs.etl_job import extract_data, transform_data, write_data, main
from src.pysparkwheelexample.dependencies.spark import start_spark

@pytest.fixture(scope="session")
def spark():
    spark, log = start_spark(
        app_name="pytest")
    return spark

@pytest.fixture
def df(spark):
    return spark.createDataFrame(
        [
            ("1", "Gray", "Gwizdz", "2")
        ],
        ["id", "first_name", "last_name", "floor"]
    )

@pytest.fixture
def input_path():
    return "tests/test_data/employees"

def test_extract_data(spark):
    df = extract_data(spark, "tests/test_data/employees/")
    assert df.count() == 8


def test_transform_data(df):
    transformed = transform_data(df, 21)
    my_row = transformed.collect()
    assert my_row[0]["steps_to_desk"] == 42


def test_write_data(df, tmp_path):
    output_path = str(tmp_path)
    write_data(df, output_path)
    print(listdir(tmp_path))
    assert len(listdir(tmp_path)) > 0


def test_main(input_path, tmp_path):
    output_path = str(tmp_path)
    main(input_path, output_path)
    print(listdir(tmp_path))
    assert len(listdir(tmp_path)) > 0


def create_test_data(spark, config):
    """Create test data.

    This function creates both both pre- and post- transformation data
    saved as Parquet files in tests/test_data. This will be used for
    unit tests as well as to load as part of the example ETL job.
    :return: None
    """
    # create example data from scratch
    local_records = [
        Row(id=1, first_name="Dan", second_name="Germain", floor=1),
        Row(id=2, first_name="Dan", second_name="Sommerville", floor=1),
        Row(id=3, first_name="Alex", second_name="Ioannides", floor=2),
        Row(id=4, first_name="Ken", second_name="Lai", floor=2),
        Row(id=5, first_name="Stu", second_name="White", floor=3),
        Row(id=6, first_name="Mark", second_name="Sweeting", floor=3),
        Row(id=7, first_name="Phil", second_name="Bird", floor=4),
        Row(id=8, first_name="Kim", second_name="Suter", floor=4)
    ]

    df = spark.createDataFrame(local_records)

    # write to Parquet file format
    (df
     .coalesce(1)
     .write
     .parquet("tests/test_data/employees", mode="overwrite"))

    # create transformed version of data
    df_tf = transform_data(df, config["steps_per_floor"])

    # write transformed version of data to Parquet
    (df_tf
     .coalesce(1)
     .write
     .parquet("tests/test_data/employees_report", mode="overwrite"))

    return None