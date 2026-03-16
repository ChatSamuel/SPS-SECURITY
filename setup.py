from setuptools import setup, find_packages

setup(
    name="sps-security",
    version="1.0.0",
    author="Samuel Pontes",
    description="Malware detection tool",
    packages=find_packages(),
    install_requires=[
        "tqdm",
        "colorama",
    ],
    entry_points={
        "console_scripts": [
            "sps=sps_security.cli:run",
        ],
    },
    python_requires=">=3.8",
)
