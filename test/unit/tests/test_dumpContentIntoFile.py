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
	assert os.path.exists(str(testFilePath))

def test_dumpContentIntoFile_fileContentIsWritten(tmp_path):
	'''
	## Unit Test: test_dumpContentIntoFile_fileContentIsWritten

	Test that the target function actually writes content into file.

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

	# Assert that the file has content
	assert int(returnedSize) > 0
	assert int(actualSize) > 0

def test_dumpContentIntoFile_fileContentIsCorrect(tmp_path):
	'''
	## Unit Test: test_dumpContentIntoFile_fileContentIsCorrect

	Test that the target function actually writes content into file and the
	written data is correct.

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

	# Read the content back from the file
	with open(testFilePath, 'r') as file:
		fileContent = file.read()

	# Assert that the file content matches the original content
	assert fileContent.strip() == testContent.strip()

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
	actualSize = os.stat(str(testFilePath)).st_size

	# Assert that the returned size matches the actual size
	assert int(returnedSize) == int(actualSize)

def test_dumpContentIntoFile_validationException1(tmp_path):
	'''
	## Unit Test: test_dumpContentIntoFile_validationException1

	Test that the target function validates data by returning a
	ValueError when strP is not set.

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

	# Call the target function and expect a ValueError
	try:
		returnedSize = dumpContentIntoFile(
			strP=None,
			fileP=testFilePath
		)
	except Exception as error:
		returnedException = error

	# Assert that a ValueError was raised
	assert isinstance(returnedException, ValueError)

def test_dumpContentIntoFile_validationException2(tmp_path):
	'''
	## Unit Test: test_dumpContentIntoFile_validationException1

	Test that the target function validates data by returning a
	TypeError when strP is the wrong type.

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

	# Call the target function and expect a ValueError
	try:
		returnedSize = dumpContentIntoFile(
			strP=1,
			fileP=testFilePath
		)
	except Exception as error:
		returnedException = error

	# Assert that a TypeError was raised
	assert isinstance(returnedException, TypeError)

def test_dumpContentIntoFile_validationException3(tmp_path):
	'''
	## Unit Test: test_dumpContentIntoFile_validationException3

	Test that the target function validates data by returning a
	ValueError when strP is an empty string.

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

	# Call the target function and expect a ValueError
	try:
		returnedSize = dumpContentIntoFile(
			strP="",
			fileP=testFilePath
		)
	except Exception as error:
		returnedException = error

	# Assert that a ValueError was raised
	assert isinstance(returnedException, ValueError)

def test_dumpContentIntoFile_validationException4(tmp_path):
	'''
	## Unit Test: test_dumpContentIntoFile_validationException4

	Test that the target function validates data by returning a
	ValueError when fileP is not set.

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

	# Call the target function and expect a ValueError
	try:
		returnedSize = dumpContentIntoFile(
			strP=testContent,
			fileP=None
		)
	except Exception as error:
		returnedException = error

	# Assert that a ValueError was raised
	assert isinstance(returnedException, ValueError)

def test_dumpContentIntoFile_validationException5(tmp_path):
	'''
	## Unit Test: test_dumpContentIntoFile_validationException5

	Test that the target function validates data by returning a
	TypeError when fileP is the wrong type.

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

	# Call the target function and expect a ValueError
	try:
		returnedSize = dumpContentIntoFile(
			strP=testContent,
			fileP=1
		)
	except Exception as error:
		returnedException = error

	# Assert that a TypeError was raised
	assert isinstance(returnedException, TypeError)

def test_dumpContentIntoFile_validationException6(tmp_path):
	'''
	## Unit Test: test_dumpContentIntoFile_validationException6

	Test that the target function validates data by returning a
	ValueError when fileP is an empty string.

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

	# Call the target function and expect a ValueError
	try:
		returnedSize = dumpContentIntoFile(
			strP=testContent,
			fileP=""
		)
	except Exception as error:
		returnedException = error

	# Assert that a ValueError was raised
	assert isinstance(returnedException, ValueError)