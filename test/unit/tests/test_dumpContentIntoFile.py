'''
Name: test_dumpContentIntoFile.py
Author: Chris Hinkson @cmh02
Description: Main entry point for unit CI testing.
'''

'''
MODULE IMPORTS
'''

# Target Module Imports
from src.MLForensics_farzana.mining.mining import dumpContentIntoFile

# Unit Submodule Imports
from test.unit.logging import UnitLogger

# System
import os
import json
import textwrap

def test_dumpContentIntoFile_fileIsWritten(tmp_path):
	'''
	## Unit Test: test_dumpContentIntoFile_fileIsWritten

	Test that the target function actually writes to file.

	Args:
		tmp_path: pytest temp directory - see https://docs.pytest.org/en/stable/how-to/tmp_path.html
	'''

	# Get logger
	logger = UnitLogger()
	logger.info("Unit Testing Logger Initialized!")

	# Print statement for testing
	logger.info("Starting test_dumpContentIntoFile_returnval!")

	# Make some new file path in the temp directory
	testFilePath = os.path.join(tmp_path, "test_output.txt")

	# Make some content to write to the file
	testContent = textwrap.dedent(
		"""
		I am gonna graduate in like 2 weeks!!!
		"""
	)

	# Call the target function
	returnedSize = dumpContentIntoFile(
		strP=testContent,
		fileP=testFilePath
	)

	# Get the size of the content we wrote
	actualSize = str(os.stat(testFilePath).st_size)

	# Assert that the file was created
	assert os.path.exists(testFilePath)
	assert returnedSize > 0
	assert actualSize > 0

def test_dumpContentIntoFile_returnVal(tmp_path):
	'''
	## Unit Test: test_dumpContentIntoFile_returnVal

	Test that the target function returns the size of the content written to file.

	Args:
		tmp_path: pytest temp directory - see https://docs.pytest.org/en/stable/how-to/tmp_path.html
	'''

	# Get logger
	logger = UnitLogger()
	logger.info("Unit Testing Logger Initialized!")

	# Print statement for testing
	logger.info("Starting test_dumpContentIntoFile_returnval!")

	# Make some new file path in the temp directory
	testFilePath = os.path.join(tmp_path, "test_output.txt")

	# Make some content to write to the file
	testContent = textwrap.dedent(
		"""
		I am gonna graduate in like 2 weeks!!!
		"""
	)

	# Call the target function
	returnedSize = dumpContentIntoFile(
		strP=testContent,
		fileP=testFilePath
	)

	# Get the size of the content we wrote
	actualSize = str(os.stat(testFilePath).st_size)

	# Assert that the returned size matches the actual size
	assert returnedSize == actualSize