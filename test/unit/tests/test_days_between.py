'''
Name: test_days_between.py
Author: Chris Hinkson @cmh02
Description: Unit tests for days_between function.
'''

'''
MODULE IMPORTS
'''

# Target Module Imports
from src.MLForensics_farzana.mining.mining import days_between

# Unit Submodule Imports
from test.unit.logging import UnitLogger

# System
import os
import textwrap
from datetime import datetime

# Testing
import pytest # type: ignore[reportMissingImports]

@pytest.mark.parametrize("d1_, d2_", [
	(datetime(year=2025, month=11, day=28), datetime(year=2025, month=11,  day=28)),
	(datetime(year=2002, month=5, day=14), datetime(year=2002, month=5,  day=14)),
])
def test_days_between_outputWhenSameDate(tmp_path, d1_: datetime, d2_: datetime):
	'''
	## Unit Test: test_days_between_outputWhenSameDate

		Test that the days_between function when given the same date (should return 0).
	Args:
		tmp_path: pytest temp directory - see https://docs.pytest.org/en/stable/how-to/tmp_path.html
	'''

	# Get logger
	logger = UnitLogger()
	logger.info("Unit Testing Logger Initialized!")

	# Print statement for testing
	logger.info("Starting test_days_between_outputValueWhenPatterns!")

	# Get the days between the two dates
	daysDiff = days_between(
		d1_=d1_,
		d2_=d2_
	)

	# Assert that days difference is 0
	assert isinstance(daysDiff, int)
	assert daysDiff == 0
	
@pytest.mark.parametrize("d1_, d2_", [
	(datetime(year=2025, month=11, day=28), datetime(year=2002, month=5,  day=14)),
])
def test_days_between_outputWhenFirstMoreRecent(tmp_path, d1_: datetime, d2_: datetime):
	'''
	## Unit Test: test_days_between_outputWhenFirstMoreRecent

		Test that the days_between function when given two dates where
		the first date is more recent than the second date (should return
		a negative integer == days difference).
	Args:
		tmp_path: pytest temp directory - see https://docs.pytest.org/en/stable/how-to/tmp_path.html
	'''

	# Get logger
	logger = UnitLogger()
	logger.info("Unit Testing Logger Initialized!")

	# Print statement for testing
	logger.info("Starting test_days_between_outputValueWhenPatterns!")

	# Get the days between the two dates
	daysDiff = days_between(
		d1_=d1_,
		d2_=d2_
	)

	# Assert that days difference is 0
	assert isinstance(daysDiff, int)
	assert daysDiff < 0

@pytest.mark.parametrize("d1_, d2_", [
	(datetime(year=2002, month=5, day=14), datetime(year=2025, month=11,  day=28)),
])
def test_days_between_outputWhenSecondMoreRecent(tmp_path, d1_: datetime, d2_: datetime):
	'''
	## Unit Test: test_days_between_outputWhenSecondMoreRecent

		Test that the days_between function when given two dates where
		the second date is more recent than the first date (should return
		a positive integer == days difference).
	Args:
		tmp_path: pytest temp directory - see https://docs.pytest.org/en/stable/how-to/tmp_path.html
	'''

	# Get logger
	logger = UnitLogger()
	logger.info("Unit Testing Logger Initialized!")

	# Print statement for testing
	logger.info("Starting test_days_between_outputValueWhenPatterns!")

	# Get the days between the two dates
	daysDiff = days_between(
		d1_=d1_,
		d2_=d2_
	)

	# Assert that days difference is 0
	assert isinstance(daysDiff, int)
	assert daysDiff > 0

@pytest.mark.parametrize("d1_, d2_", [
	(None, datetime(year=2025, month=11,  day=28)),
	(datetime(year=2002, month=5, day=14), None),
])
def test_days_between_validationValueError(tmp_path, d1_: datetime, d2_: datetime):
	'''
	## Unit Test: test_days_between_validationValueError

	Test that the days_between function validates data by returning ValueErrors with following conditions:
	- d1_ not set
	- d2_ not set

	Args:
		tmp_path: pytest temp directory - see https://docs.pytest.org/en/stable/how-to/tmp_path.html
	'''

	# Get logger
	logger = UnitLogger()
	logger.info("Unit Testing Logger Initialized!")

	# Print statement for testing
	logger.info("Starting test_days_between_validationValueError!")

	# Get days between two dates, expecting ValueErrors
	returnedException = None
	try:
		daysDiff = days_between(
			d1_=d1_,
			d2_=d2_
		)
	except Exception as error:

		# Grab the error
		returnedException = error

	# Assert that a ValueError was raised
	assert returnedException is not None
	assert isinstance(returnedException, ValueError)

@pytest.mark.parametrize("d1_, d2_", [
	("lolthisisnotadatetimeobject", datetime(year=2025, month=11,  day=28)),
	(datetime(year=2002, month=5, day=14), "lolthisisnotadatetimeobject"),
])
def test_days_between_validationTypeError(tmp_path, d1_: datetime, d2_: datetime):
	'''
	## Unit Test: test_days_between_validationTypeError

	Test that the days_between function validates data by returning TypeErrors with following conditions:
	- d1_ not a datetime object
	- d2_ not a datetime object

	Args:
		tmp_path: pytest temp directory - see https://docs.pytest.org/en/stable/how-to/tmp_path.html
	'''

	# Get logger
	logger = UnitLogger()
	logger.info("Unit Testing Logger Initialized!")

	# Print statement for testing
	logger.info("Starting test_makeChunks_listGetsSplit!")

	# Get days between two dates, expecting TypeErrors
	returnedException = None
	try:
		daysDiff = days_between(
			d1_=d1_,
			d2_=d2_
		)
	except Exception as error:

		# Grab the error
		returnedException = error

	# Assert that a TypeError was raised
	assert returnedException is not None
	assert isinstance(returnedException, TypeError)