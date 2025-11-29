'''
Name: test_getPythonFileCount.py
Author: Chris Hinkson @cmh02
Description: Unit tests for getPythonFileCount function.
'''

'''
MODULE IMPORTS
'''

# Target Module Imports
from src.MLForensics_farzana.mining.mining import getPythonFileCount

# Unit Submodule Imports
from test.unit.logging import UnitLogger

# System
import os
import textwrap

# Testing
import pytest # type: ignore[reportMissingImports]

@pytest.mark.parametrize("path2dir", [
	os.path.dirname(os.path.abspath(__file__)),
])
def test_getPythonFileCount_outputValueWhenPythonFiles(tmp_path, path2dir: str):
	'''
	## Unit Test: test_getPythonFileCount_outputValueWhenPythonFiles

		Test that the getPythonFileCount function finds python files when present.

	Args:
		tmp_path: pytest temp directory - see https://docs.pytest.org/en/stable/how-to/tmp_path.html
	'''

	# Get logger
	logger = UnitLogger()
	logger.info("Unit Testing Logger Initialized!")

	# Print statement for testing
	logger.info("Starting test_getPythonFileCount_outputValueWhenPythonFiles!")

	# Get the number of python files otw to the given directory
	foundFiles = getPythonFileCount(
		path2dir=path2dir
	)

	# Assert that usage count is valid
	assert isinstance(foundFiles, int)
	assert foundFiles > 0

def test_getPythonFileCount_outputValueWhenNoPythonFiles(tmp_path):
	'''
	## Unit Test: test_getPythonFileCount_outputValueWhenNoPythonFiles

		Test that the getPythonFileCount function finds no python files when there are no python files present.
	Args:
		tmp_path: pytest temp directory - see https://docs.pytest.org/en/stable/how-to/tmp_path.html
	'''

	# Get logger
	logger = UnitLogger()
	logger.info("Unit Testing Logger Initialized!")

	# Print statement for testing
	logger.info("Starting test_getPythonFileCount_outputValueWhenNoPythonFiles!")

	# Get the number of python files otw to temp directory (where no python files should exist)
	foundFiles = getPythonFileCount(
		path2dir=tmp_path
	)

	# Assert that usage count is 0
	assert isinstance(foundFiles, int)
	assert foundFiles == 0

@pytest.mark.parametrize("path2dir", [
	None,
	"",
	"/some/random/path/that/hopefully/does/not/exist",
])
def test_getPythonFileCount_validationValueError(tmp_path, path2dir: str):
	'''
	## Unit Test: test_getPythonFileCount_validationValueError

	Test that the getPythonFileCount function validates data by returning ValueErrors with following conditions:
	- path2dir not set
	- path2dir empty string
	- path2dir does not exist

	Args:
		tmp_path: pytest temp directory - see https://docs.pytest.org/en/stable/how-to/tmp_path.html
	'''

	# Get logger
	logger = UnitLogger()
	logger.info("Unit Testing Logger Initialized!")

	# Print statement for testing
	logger.info("Starting test_checkPythonFile_validationValueError!")

	# Get the usage count of patterns in files otw to the given directory, expecting ValueErrors
	returnedException = None
	try:
		foundFiles = getPythonFileCount(
			path2dir=path2dir
		)
	except Exception as error:

		# Grab the error
		returnedException = error

	# Assert that a ValueError was raised
	assert returnedException is not None
	assert isinstance(returnedException, ValueError)

@pytest.mark.parametrize("path2dir", [
	2002
])
def test_getPythonFileCount_validationTypeError(tmp_path, path2dir: str):
	'''
	## Unit Test: test_getPythonFileCount_validationTypeError

	Test that the getPythonFileCount function validates data by returning TypeErrors with following conditions:
	- path2dir not a string

	Args:
		tmp_path: pytest temp directory - see https://docs.pytest.org/en/stable/how-to/tmp_path.html
	'''

	# Get logger
	logger = UnitLogger()
	logger.info("Unit Testing Logger Initialized!")

	# Print statement for testing
	logger.info("Starting test_checkPythonFile_validationTypeError!")

	# Get the usage count of patterns in files otw to the given directory, expecting TypeErrors
	returnedException = None
	try:
		foundFiles = getPythonFileCount(
			path2dir=path2dir
		)
	except Exception as error:

		# Grab the error
		returnedException = error

	# Assert that a TypeError was raised
	assert returnedException is not None
	assert isinstance(returnedException, TypeError)