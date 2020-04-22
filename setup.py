from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pysparkwheelexample", # Replace with your own username
    version="0.0.1",
    author="Gray Gwizdz",
    author_email="gray@databricks.com",
    description="A small example package to demonstrate how to build a wheel for usage with Databricks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.datarbricks.com", #Should be updated with a better URL
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7', # Best to match this with the Databricks Runtime you are targeting
)
