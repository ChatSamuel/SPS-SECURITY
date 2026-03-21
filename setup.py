from setuptools import setup, find_packages

setup(
    name="sps-security",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "rich",
        "watchdog"
    ],
    entry_points={
        "console_scripts": [
            "sps=sps_security.cli:run",
        ],
    },
)
