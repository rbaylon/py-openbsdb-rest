import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="py-openbsd-rest",
    version="1.0.0",
    description="OpenBSD RESTful api. With initial focus on managing vm.conf(5), pf.conf(5) and hostname.if(5)",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/rbaylon/py-openbsd-rest",
    author="Ricardo Baylon",
    author_email="rbaylon@outlook.com",
    license="ISC",
    classifiers=[
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python :: 3"
    ],
    packages=["openbsdrest", "Utils"],
    include_package_data=True,
    install_requires=[
        "flask-login",
        "ipaddress",
        "Flask",
        "Flask-RESTful",
        "Flask-Script",
        "PyJWT",
        "py-bsdauth"
    ],
    entry_points={
        "console_scripts": [
            "openbsdrest=run:main",
        ]
    },
    platforms=["OpenBSD"]
)
