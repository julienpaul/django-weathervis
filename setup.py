#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = []

test_requirements = [
    "pytest>=3",
]

setup(
    author="Julien Paul",
    author_email="julien.paul@uib.no",
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU GPLv3 License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    description="django weathervis webpages.",
    install_requires=requirements,
    license="GNU GPLv3 license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="django-weathervis",
    name="django-weathervis",
    maintainer="BCDC",
    packages=find_packages(include=["django-weathervis"]),
    url="https://github.com/julienpaul/django-weathervis",
    version="version=0.2.1",
    zip_safe=False,
)
