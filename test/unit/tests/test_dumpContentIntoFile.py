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

def test_dumpContentIntoFile():

	'''
	LOGGER SETUP
	'''

	# Initialize logger
	logger = UnitLogger()
	logger.info("Unit Testing Logger Initialized!")

	# Print statement for testing
	logger.info("Starting test_dumpContentIntoFile")

	assert 1 + 1 == 2