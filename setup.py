from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in alansaridigital/__init__.py
from alansaridigital import __version__ as version

setup(
	name="alansaridigital",
	version=version,
	description="Alansari Digital",
	author="Mustafa Ahmad",
	author_email="developer@alansariglobal.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
