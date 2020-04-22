# D&B - Example PySpark Pandas UDF Wheel Code Obfuscation 

This example PySpark UDF is based on a Databricks blog titled [Fine-Grained Time Series Forecasting At Scale With Facebook Prophet And Apache Spark](forecasting).

In order for you to run this example end to end, you will need to complete the following setup steps.

1. Create a Conda environment using the `conda.yaml` inside of this repo. `conda env create -f conda.yaml`
2. Create a Databricks cluster with a Databricks Runtime version 6 or above. The ML runtime will not work when trying to install using `dbutils`, so you will need to install the `FBProphet==0.5` and `holidays==0.9.12` using the Libraries page on the Clusters UI.
3. Upload the dataset from the data directory to the FileStore - `/FileStore/tables/demand_forecast/train/train.csv`.
4. Run the `build.sh` script from the root directory.
5. Install the created library from the `build` directory in the `encrypt` of the project using the Libraries page on the Clusters UI.
6. Import the forecasting notebook located in the `notebooks` directory.
7. Optionally review the encrypted `__init__.py` file which is created under the `encrypt` directory.
8. Optionally tear down the results of the `build.sh` process using `clean.sh`.


----

## Implementation Notes

If you would like a function to not be obfuscated, the function name needs to begin with two underscores (__), as demonstrated in this example. If you would like your function name during code execution to not have this, you can alias the function by using `from dnbexamplepackage import __forecast_store_item as forecast`

[PyMinifier](pyminifier) is the tool being used to obfuscate the code with non-latin character sets, and configuration for the obfuscation can be found in the `build.sh` file.

FULL DISCLOSURE: If someone wanted to rip apart the wheel, and attempt to convert the 100 non-latin character obfuscated names into something more readable, because Python is an interpreted language this cannot be considered complete code obfuscation. There are better code obfuscation tools avalaible with Java/Scala that could also be used in conjunction with Spark with a greater level of security.

[forecasting]: https://databricks.com/blog/2020/01/27/time-series-forecasting-prophet-spark.html
[pyminifier]: http://liftoff.github.io/pyminifier/

----

