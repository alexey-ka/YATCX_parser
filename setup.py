from setuptools import find_packages, setup

__version__ = "0.0.1b"

setup(
    name="yatcx-parser",
    version=__version__,
    description="Simple parser for advanced analytics of the Garmin TCX files",
    long_description=open("README.md").read(),
    author="Aleksei Karetnikov",
    author_email="alexey.karetnikow@gmail.com",
    url="https://github.com/alexey-ka/YATCX_parser",
    packages=find_packages(include=["src"]),
    include_package_data=True,
    license="MIT",
    zip_safe=False,
    keywords="tcx",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "lxml",
        "numpy",
    ],
)