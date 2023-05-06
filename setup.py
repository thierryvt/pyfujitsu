import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyfgl",
    version="1.0.2",
    author="Thierry VT, Mehdi Modarressi",
    author_email="",
    description="Python library to control Fujitsu General Airconditioners on AylaNetworks IoT platform",
    long_description="Python library to control Fujitsu General Airconditioners on AylaNetworks IoT platform",
    url="https://github.com/thierryvt/pyfujitsu",
    license="MIT License",
    packages=['pyfgl'],
    install_requires=['requests', 'certifi', 'chardet', 'idna', 'urllib3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
