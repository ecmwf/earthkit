# (C) Copyright 2023- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

import io
import os

from setuptools import find_namespace_packages, setup

ROOT_DIR = os.path.dirname(__file__)


def read(fname):
    file_path = os.path.join(ROOT_DIR, fname)
    return io.open(file_path, encoding="utf-8").read()


exec(open(os.path.join(ROOT_DIR, "earthkit", "version.py")).read())


install_requires = []

test_requires = ["pytest"]

setup(
    name="earthkit",
    version=__version__,
    author="European Centre for Medium-Range Weather Forecasts (ECMWF)",
    author_email="software.support@ecmwf.int",
    license="Apache License Version 2.0",
    url="https://github.com/ecmwf/earthkit",
    description="",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_namespace_packages(include=["earthkit.*"]),
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=True,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
    ],
    test_requires=test_requires,
    test_suite="tests",
)
