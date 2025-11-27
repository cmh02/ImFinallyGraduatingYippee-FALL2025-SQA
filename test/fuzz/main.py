'''
Name: main.py
Author: Chris Hinkson @cmh02
Description: Main entry point for fuzz CI testing.
'''

'''
MODULE IMPORTS
'''

# Target Module Imports
from ...src.MLForensics_farzana.mining.mining import dumpContentIntoFile, makeChunks, checkPythonFile, days_between, getPythonFileCount

# Fuzz Submodule Imports
from .fuzzmanager import FuzzManager

if __name__ == "__main__":

	# Make a fuzz handler
	fuzzManager = FuzzManager()

	# Register fuzz input sources
	fuzzManager.registerFuzzInputSource("Big List of Naughty Strings", [])
	fuzzManager.registerFuzzInputSource("FuzzDB All Attacks X Platform", [])
	fuzzManager.registerFuzzInputSource("FuzzDB Format Strings", [])
	fuzzManager.registerFuzzInputSource("FuzzDB Integer Overloads", [])
	fuzzManager.registerFuzzInputSource("FuzzDB Invalid Filenames Linux", [])

	# Define list of functions to fuzz from target module
	functionsToFuzz = [dumpContentIntoFile, makeChunks, checkPythonFile, days_between, getPythonFileCount]

	# Perform fuzzing on targets
	for func in functionsToFuzz:
		print(f"\n\n=== Fuzzing Function: {func} ===\n\n")
		fuzzManager.performAllFuzzing(
			targetFunction=func,
			timeout=5.0
		)
		print(f"\n\n=== Completed Fuzzing Function: {func} ===\n\n")