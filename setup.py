# -*- coding: utf-8 -*-
"""
Created on Tue May  3 00:36:08 2022

@author: PaulJ
"""

from setuptools import setup, find_packages

setup(
    name="cashflowsim",
    version="0.1",
    description="Simulation of a Game",
    url="#",
    author="max",
    install_requires=["opencv-python"],
    author_email="",
    packages=find_packages(exclude=("tests", "docs")),
    zip_safe=False,
)
