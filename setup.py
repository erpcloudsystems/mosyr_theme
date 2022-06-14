from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in mosyr_theme/__init__.py
from mosyr_theme import __version__ as version

setup(
	name="mosyr_theme",
	version=version,
	description="Theme",
	author="Mai",
	author_email="mai.mq.1995@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
