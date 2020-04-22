"""
test_etl_job.py
~~~~~~~~~~~~~~~

This module contains unit tests for the configs of the ETL
job defined in etl_job.py. It makes use of a local version of PySpark
that is bundled with the PySpark package.
"""
import pytest

import json

from pyspark.sql.functions import mean

from src.pysparkwheelexample.dependencies.configs import config
from src.pysparkwheelexample.dependencies.spark import start_spark

def test_configs():
    assert config["steps_per_floor"] == 21