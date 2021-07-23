from setuptools import setup

try:
    from aziona.core.conf import const

    name = const.getconst("NAME")
    version = const.getconst("VERSION")
except Exception:
    name = "aziona"
    version = "dev"

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().split("\n")

setup(
    name=name,
    version=version,
    author="Fabrizio Cafolla",
    author_email="fabrizio.cafolla@gdue.it",
    description="aziona - CI / CD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/azionaventures/aziona",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    scripts=["bin/aziona"],
    # entry_points={"console_scripts": ["aziona = aziona.cli.main:main"]},
    install_requires=requirements,
    extras_require={
        "dev": ["check-manifest"],
        "test": ["coverage"],
    },
    setup_requires=["pytest-runner", "flake8"],
    tests_require=["pytest"],
)
