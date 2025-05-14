from setuptools import setup, find_packages

setup(
    name="pi-devops-toolkit",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer",
        "pyserial",
        "paramiko"
    ],
    entry_points={
        "console_scripts": [
            "pi-dev=pi_devops.cli:app"
        ]
    }
)
