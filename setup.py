# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages
import sys

packagename = "exam_generator"

# consider the path of `setup.py` as root directory:
PROJECTROOT = os.path.dirname(sys.argv[0]) or "."
__version__ = (
    open(os.path.join(PROJECTROOT, "src", packagename, "release.py"), encoding="utf8")
    .read()
    .split('__version__ = "', 1)[1]
    .split('"', 1)[0]
)

with open("requirements.txt") as requirements_file:
    requirements = requirements_file.read()

setup(
    name=packagename,
    version=__version__,
    author='Niklas Weber',
    packages=find_packages("src"),
    package_dir = {"": "src"},
    package_data={'abc': ['templates/*']},
    url='',
    license='',
    description='Script for generating exams based on selected settings/ problems',
    long_description="""
    Exam_generator is a script which is designed to create exams/ tests from pools of problems while 
    ensuring that there will be no repetition amongst different groups. The exams/ tests are based off
    of two major components: LaTeX files (problems, solutions, templates) and user defined settings.
    """,
    keywords='',
    install_requires=requirements,
    entry_points={'console_scripts': ['{0}={0}:main'.format(packagename)]}
)