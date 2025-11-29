'''
Name: test_makeChunks.py
Author: Chris Hinkson @cmh02
Description: Unit tests for makeChunks function.
'''

'''
MODULE IMPORTS
'''

# Target Module Imports
from src.MLForensics_farzana.mining.mining import makeChunks

# Unit Submodule Imports
from test.unit.logging import UnitLogger

# System
import os
import textwrap

# Testing
import pytest # type: ignore[reportMissingImports]

@pytest.mark.parametrize("testList,chunkSize", [
	([f"item_{i}" for i in range(100)], 10),
	([f"newitem_{i}" for i in range(1000)], 50),
	([f"ne2item_{i}" for i in range(10000)], 1000),
])
def test_makeChunks_listGetsSplit(tmp_path, testList: list, chunkSize: int):
	'''
	## Unit Test: test_makeChunks_listGetsSplit

	Test that the makeChunks function actually splits a list into chunks.

	Args:
		tmp_path: pytest temp directory - see https://docs.pytest.org/en/stable/how-to/tmp_path.html
	'''

	# Get logger
	logger = UnitLogger()
	logger.info("Unit Testing Logger Initialized!")

	# Print statement for testing
	logger.info("Starting test_makeChunks_listGetsSplit!")

	# Since the target function is a generator, we need to convert the output to a list
	chunkedList = list(makeChunks(
		the_list=testList,
		size_=chunkSize
	))

	# Assert that the chunked list has multiple chunks
	assert len(chunkedList) > 1

@pytest.mark.parametrize("testList,chunkSize", [
	([f"item_{i}" for i in range(100)], 10),
	([f"newitem_{i}" for i in range(1000)], 50),
	([i for i in range(10000)], 1000),
	([{f"key_{i}": f"value_{i}"} for i in range(25)], 2),
	([(f"tuple{i}") for i in range(30)], 4),
])
def test_makeChunks_listGetsSplitToSize(tmp_path, testList: list, chunkSize: int):
	'''
	## Unit Test: test_makeChunks_listGetsSplitToSize

	Test that the makeChunks function actually splits a list into chunks of the correct size.

	Args:
		tmp_path: pytest temp directory - see https://docs.pytest.org/en/stable/how-to/tmp_path.html
	'''

	# Get logger
	logger = UnitLogger()
	logger.info("Unit Testing Logger Initialized!")

	# Print statement for testing
	logger.info("Starting test_makeChunks_listGetsSplit!")

	# Since the target function is a generator, we need to convert the output to a list
	chunkedList = list(makeChunks(
		the_list=testList,
		size_=chunkSize
	))

	# Iterate over new chunks
	for i, chunk in enumerate(chunkedList):

		# If this is not the last chunk, assert that the chunk size is correct
		if i < (len(chunkedList) - 1):
			assert len(chunk) == chunkSize

		# If this is the last chunk, assert that the chunk size is less than or equal to the chunk size
		else:
			assert len(chunk) <= chunkSize

@pytest.mark.parametrize("testList,chunkSize", [
	(None, 10),
	([], 10),
	([f"item_{i}" for i in range(100)], None),
	([f"item_{i}" for i in range(100)], 0),
	([f"item_{i}" for i in range(10)], 20),
])
def test_makeChunks_validationValueError(tmp_path, testList: list, chunkSize: int):
	'''
	## Unit Test: test_makeChunks_validationValueError

	Test that the target function validates data by returning ValueErrors with following conditions:
	- list is not set
	- list is empty
	- size is not set
	- size is less than 1
	- size is greater than the length of the list

	Args:
		tmp_path: pytest temp directory - see https://docs.pytest.org/en/stable/how-to/tmp_path.html
	'''

	# Get logger
	logger = UnitLogger()
	logger.info("Unit Testing Logger Initialized!")

	# Print statement for testing
	logger.info("Starting test_makeChunks_validationValueError!")

	# Call the target function and expect ValueErrors
	returnedException = None
	try:
		chunkedList = list(makeChunks(
			the_list=testList,
			size_=chunkSize
		))
	except Exception as error:

		# Grab the error
		returnedException = error

	# Assert that a ValueError was raised
	assert returnedException is not None
	assert isinstance(returnedException, ValueError)

@pytest.mark.parametrize("testList,chunkSize", [
	(1, 10),
	([f"item_{i}" for i in range(10)], "notaninteger"),
])
def test_makeChunks_validationTypeError(tmp_path, testList: list, chunkSize: int):
	'''
	## Unit Test: test_makeChunks_validationTypeError

	Test that the target function validates data by returning TypeErrors with following conditions:
	- list is not a list
	- size is not an integer

	Args:
		tmp_path: pytest temp directory - see https://docs.pytest.org/en/stable/how-to/tmp_path.html
	'''

	# Get logger
	logger = UnitLogger()
	logger.info("Unit Testing Logger Initialized!")

	# Print statement for testing
	logger.info("Starting test_makeChunks_validationTypeError!")

	# Call the target function and expect TypeErrors
	returnedException = None
	try:
		chunkedList = list(makeChunks(
			the_list=testList,
			size_=chunkSize
		))
	except Exception as error:

		# Grab the error
		returnedException = error

	# Assert that a TypeError was raised
	assert returnedException is not None
	assert isinstance(returnedException, TypeError)