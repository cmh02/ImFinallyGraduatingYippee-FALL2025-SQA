'''
Name: test_checkPythonFile.py
Author: Chris Hinkson @cmh02
Description: Unit tests for checkPythonFile function.
'''

'''
MODULE IMPORTS
'''

# Target Module Imports
from src.MLForensics_farzana.mining.mining import checkPythonFile

# Unit Submodule Imports
from test.unit.logging import UnitLogger

# System
import os
import textwrap

# Testing
import pytest # type: ignore[reportMissingImports]

# To make this a valid file for this test, import sklearn and gym
import sklearn # type: ignore[reportMissingImports]
import gym # type: ignore[reportMissingImports]

@pytest.mark.parametrize("path2dir", [
	os.path.dirname(os.path.abspath(__file__)),
])
def test_checkPythonFile_outputValueWhenPatterns(tmp_path, path2dir: str):
	'''
	## Unit Test: test_checkPythonFile_outputValueWhenPatterns

		Test that the checkPythonFile function actually checks for patterns in Python files.

	Args:
		tmp_path: pytest temp directory - see https://docs.pytest.org/en/stable/how-to/tmp_path.html
	'''

	# Get logger
	logger = UnitLogger()
	logger.info("Unit Testing Logger Initialized!")

	# Print statement for testing
	logger.info("Starting test_makeChunks_listGetsSplit!")

	# Get the usage count of patterns in files otw to the given directory
	usageCount = checkPythonFile(
		path2dir=path2dir
	)

	# Assert that usage count is valid
	assert isinstance(usageCount, int)
	assert usageCount > 0

def test_checkPythonFile_outputValueWhenNoPatterns(tmp_path):
	'''
	## Unit Test: test_checkPythonFile_outputValueWhenNoPatterns

		Test that the checkPythonFile function actually checks for patterns in Python files when there are no patterns present.

	Args:
		tmp_path: pytest temp directory - see https://docs.pytest.org/en/stable/how-to/tmp_path.html
	'''

	# Get logger
	logger = UnitLogger()
	logger.info("Unit Testing Logger Initialized!")

	# Print statement for testing
	logger.info("Starting test_makeChunks_listGetsSplit!")

	# Make a new file with no patterns in the temp diretory
	newFilePath = os.path.join(tmp_path, "no_pattern_file.py")
	with open(newFilePath, "w", encoding="utf-8") as f:
		f.write(textwrap.dedent("""
		# Blah blah test file without patterns
		def funcWithNoPatterns():
			print("i'm graduating woop woop!")
		"""))

	# Get the usage count of patterns in files otw to the given directory
	usageCount = checkPythonFile(
		path2dir=newFilePath
	)

	# Assert that usage count is 0
	assert isinstance(usageCount, int)
	assert usageCount == 0

@pytest.mark.parametrize("path2dir", [
	None,
	"",
	"/some/random/path/that/hopefully/does/not/exist",
])
def test_checkPythonFile_validationValueError(tmp_path, path2dir: str):
	'''
	## Unit Test: test_checkPythonFile_validationValueError

	Test that the checkPythonFile function validates data by returning ValueErrors with following conditions:
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
	logger.info("Starting test_makeChunks_listGetsSplit!")

	# Get the usage count of patterns in files otw to the given directory, expecting ValueErrors
	returnedException = None
	try:
		usageCount = checkPythonFile(
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
def test_checkPythonFile_validationTypeError(tmp_path, path2dir: str):
	'''
	## Unit Test: test_checkPythonFile_validationTypeError

	Test that the checkPythonFile function validates data by returning TypeErrors with following conditions:
	- path2dir not a string

	Args:
		tmp_path: pytest temp directory - see https://docs.pytest.org/en/stable/how-to/tmp_path.html
	'''

	# Get logger
	logger = UnitLogger()
	logger.info("Unit Testing Logger Initialized!")

	# Print statement for testing
	logger.info("Starting test_makeChunks_listGetsSplit!")

	# Get the usage count of patterns in files otw to the given directory, expecting TypeErrors
	returnedException = None
	try:
		usageCount = checkPythonFile(
			path2dir=path2dir
		)
	except Exception as error:

		# Grab the error
		returnedException = error

	# Assert that a TypeError was raised
	assert returnedException is not None
	assert isinstance(returnedException, TypeError)