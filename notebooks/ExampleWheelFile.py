# Databricks notebook source
# MAGIC %pip install dbfs:/path_to_my_wheel_file.whl

# COMMAND ----------

arg1 = dbutils.widgets.get("arg1")
arg2 = dbutils.widgets.get("arg2")

# COMMAND ----------

from pysparkwheelexample.jobs import main
main(arg1, arg2)
