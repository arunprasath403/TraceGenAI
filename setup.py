from setuptools import setup, find_packages

setup(
    name="tracegenai",
    version="0.1.0",
    description="Agentic AI system for SDLC traceability",
    author="Arun Prasath",
    packages=find_packages(include=[
        "agents*",
        "tools*",
        "utils*",
        "config*",
        "ui*",
        "rag*"
    ]),
    install_requires=[
        line.strip()
        for line in open("requirements.txt").readlines()
        if line.strip() and not line.startswith("#")
    ],
    python_requires=">=3.10",
)
