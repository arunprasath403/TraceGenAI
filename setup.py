from setuptools import setup, find_packages

setup(
    name="ai_testcase",
    version="0.1",
    packages=find_packages(include=[
        "agents*",
        "tools*",
        "utils*",
        "config*",
        "ui*"
    ]),
)
