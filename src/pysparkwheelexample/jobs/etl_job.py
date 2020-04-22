"""
etl_job.py
~~~~~~~~~~

This Python module contains an example Apache Spark ETL job definition
that implements best practices for production ETL jobs. It can be
submitted to a Spark cluster (or locally) using the "spark-submit"
command found in the "/bin" directory of all Spark distributions
(necessary for running any Spark job, locally or otherwise). For
example, this example script can be executed as follows,

where packages.zip contains Python modules required by ETL job (in
this example it contains a class to provide access to Spark"s logger),
which need to be made available to each executor process on every node
in the cluster; etl_config.json is a text file sent to the cluster,
containing a JSON object with all of the configuration parameters
required by the ETL job; and, etl_job.py contains the Spark application
to be executed by a driver process on the Spark master node.

For more details on submitting Spark applications, please see here:
http://spark.apache.org/docs/latest/submitting-applications.html

Our chosen approach for structuring jobs is to separate the individual
"units" of ETL - the Extract, Transform and Load parts - into dedicated
functions, such that the key Transform steps can be covered by tests
and jobs or called from within another environment (e.g. a Jupyter or
Zeppelin notebook).

Recommended input path - "tests/test_data/employees"
Recommended output path - "tests/loaded_data"

"""

from pyspark.sql import Row
from pyspark.sql.functions import col, concat_ws, lit

from ..dependencies.configs import config
from ..dependencies.spark import start_spark


def main(input_path, output_path):
    """Main ETL script definition.

    :return: None
    """
    # start Spark application and get Spark session, logger and config
    spark, log = start_spark(
        app_name="etl_job")

    # log that main ETL job is starting
    log.warn("etl_job is up-and-running")

    # execute ETL pipeline
    data = extract_data(spark, input_path)
    data_transformed = transform_data(data, config["steps_per_floor"])
    write_data(data_transformed, output_path)

    # log the success and terminate Spark application
    log.warn("etl_job is finished")
    spark.stop()
    return None


def extract_data(spark, input_path):
    """Load data from CSV file format.

    :param spark: Spark session object.
    :return: Spark DataFrame.
    """
    df = (
        spark
        .read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(input_path))

    return df


def transform_data(df, steps_per_floor):
    """Transform original dataset.

    :param df: Input DataFrame.
    :param steps_per_floor: The number of steps per-floor.
    :return: Transformed DataFrame.
    """
    df_transformed = (
        df
        .select(
            col("id"),
            concat_ws(
                " ",
                col("first_name"),
                col("last_name")).alias("name"),
               (col("floor") * lit(steps_per_floor)).alias("steps_to_desk")))

    return df_transformed


def write_data(df, output_path):
    """Collect data locally and write to Parquet.

    :param df: DataFrame to print.
    :return: None
    """
    (df
     .write
     .mode("overwrite")
     .parquet(output_path))
    return None


# entry point for PySpark ETL application
if __name__ == "__main__":
    main()
