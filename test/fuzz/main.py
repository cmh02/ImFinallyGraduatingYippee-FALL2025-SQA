'''
Name: main.py
Author: Chris Hinkson @cmh02
Description: Main entry point for fuzz CI testing.
'''

'''
MODULE IMPORTS
'''

# Target Module Imports
from src.MLForensics_farzana.mining.mining import dumpContentIntoFile, makeChunks, checkPythonFile, days_between, getPythonFileCount

# Fuzz Submodule Imports
from .logging import FuzzLogger
from .fuzzmanager import FuzzManager
from .resourcemanager import ResourceManager

# System
import os
import json

if __name__ == "__main__":

	'''
	LOGGER SETUP
	'''

	# Initialize logger
	logger = FuzzLogger()
	logger.info("Fuzz Testing Logger Initialized!")

	'''
	DIRECTORY SETUP

	This section sets up directory paths for resources and output.
	'''

	# Define directory paths
	DIRECTORY_WORKING = os.getcwd()
	DIRECTORY_RESOURCES = os.path.join(DIRECTORY_WORKING, "resources")
	DIRECTORY_OUTPUT = os.path.join(DIRECTORY_WORKING, "output")

	# Make sure that subdirectories exist
	os.makedirs(DIRECTORY_RESOURCES, exist_ok=True)
	os.makedirs(DIRECTORY_OUTPUT, exist_ok=True)

	# Print status
	logger.info(f"Directory Setup has been completed!")
	logger.info(f" -> Working Directory: {DIRECTORY_WORKING}")
	logger.info(f" -> Resources Directory: {DIRECTORY_RESOURCES}")
	logger.info(f" -> Output Directory: {DIRECTORY_OUTPUT}")

	'''
	RESOURCE DOWNLOAD

	For this project, I use two main external sources of fuzzing input:
	- Big List of Naughty Strings (https://github.com/minimaxir/big-list-of-naughty-strings)
	- FuzzDB (https://github.com/fuzzdb-project/fuzzdb)

	This section will download these resources if they are not already present.
	'''

	# Big List of Naughty Strings
	FP_BLNS = os.path.join(DIRECTORY_RESOURCES, "blns.json")
	URL_BLNS = "https://raw.githubusercontent.com/minimaxir/big-list-of-naughty-strings/master/blns.json"
	if ResourceManager.downloadResource(URL_BLNS, FP_BLNS, "Big List of Naughty Strings"):
		logger.info(f"Big List of Naughty Strings downloaded to {FP_BLNS}!")
	else:
		logger.info(f"Big List of Naughty Strings already present at {FP_BLNS}!")

	# Downnload FuzzDB all attacks x platform version
	FP_FUZZDB_ALLATTACKSXPLATFORM = os.path.join(DIRECTORY_RESOURCES, "all-attacks-xplatform.txt")
	URL_FUZZDB_ALLATTACKSXPLATFORM = "https://raw.githubusercontent.com/fuzzdb-project/fuzzdb/refs/heads/master/attack/all-attacks/all-attacks-xplatform.txt"
	if ResourceManager.downloadResource(URL_FUZZDB_ALLATTACKSXPLATFORM, FP_FUZZDB_ALLATTACKSXPLATFORM, "FuzzDB All Attacks X Platform"):
		logger.info(f"FuzzDB All Attacks X Platform downloaded to {FP_FUZZDB_ALLATTACKSXPLATFORM}!")
	else:
		logger.info(f"FuzzDB All Attacks X Platform already present at {FP_FUZZDB_ALLATTACKSXPLATFORM}!")

	# Download FuzzDB format strings
	FP_FUZZDB_FORMATSTRINGS = os.path.join(DIRECTORY_RESOURCES, "format-strings.txt")
	URL_FUZZDB_FORMATSTRINGS = "https://raw.githubusercontent.com/fuzzdb-project/fuzzdb/refs/heads/master/attack/format-strings/format-strings.txt"
	if ResourceManager.downloadResource(URL_FUZZDB_FORMATSTRINGS, FP_FUZZDB_FORMATSTRINGS, "FuzzDB Format Strings"):
		logger.info(f"FuzzDB Format Strings downloaded to {FP_FUZZDB_FORMATSTRINGS}!")
	else:
		logger.info(f"FuzzDB Format Strings already present at {FP_FUZZDB_FORMATSTRINGS}!")

	# Download FuzzDB integer overloads
	FP_FUZZDB_INTEGEROVERLOADS = os.path.join(DIRECTORY_RESOURCES, "integer-overloads.txt")
	URL_FUZZDB_INTEGEROVERLOADS = "https://raw.githubusercontent.com/fuzzdb-project/fuzzdb/refs/heads/master/attack/integer-overflow/integer-overflows.txt"
	if ResourceManager.downloadResource(URL_FUZZDB_INTEGEROVERLOADS, FP_FUZZDB_INTEGEROVERLOADS, "FuzzDB Integer Overloads"):
		logger.info(f"FuzzDB Integer Overloads downloaded to {FP_FUZZDB_INTEGEROVERLOADS}!")
	else:
		logger.info(f"FuzzDB Integer Overloads already present at {FP_FUZZDB_INTEGEROVERLOADS}!")

	# Download FuzzDB invalid filenames
	FP_FUZZDB_INVALIDFILENAMESLINUX = os.path.join(DIRECTORY_RESOURCES, "invalid-filenames-linux.txt")
	URL_FUZZDB_INVALIDFILENAMESLINUX = "https://raw.githubusercontent.com/fuzzdb-project/fuzzdb/refs/heads/master/attack/file-upload/invalid-filenames-linux.txt"
	if ResourceManager.downloadResource(URL_FUZZDB_INVALIDFILENAMESLINUX, FP_FUZZDB_INVALIDFILENAMESLINUX, "FuzzDB Invalid Filenames Linux"):
		logger.info(f"FuzzDB Invalid Filenames Linux downloaded to {FP_FUZZDB_INVALIDFILENAMESLINUX}!")
	else:
		logger.info(f"FuzzDB Invalid Filenames Linux already present at {FP_FUZZDB_INVALIDFILENAMESLINUX}!")

	'''
	RESOURCE LOADING

	This section loads the downloaded resources into memory for use as fuzzing inputs.
	'''

	# Load Big List of Naughty Strings
	blnsInputs = []
	with open(FP_BLNS, "r", encoding="utf-8") as blnsFile:
		blnsInputs = json.load(blnsFile)
		logger.info(f"Loaded {len(blnsInputs)} inputs from Big List of Naughty Strings.")

	# Load FuzzDB all attacks x platform
	fuzzdbAllAttacksXPlatformInputs = []
	with open(FP_FUZZDB_ALLATTACKSXPLATFORM, "r", encoding="utf-8") as fuzzdbAllAttacksXPlatformFile:
		fuzzdbAllAttacksXPlatformInputs = fuzzdbAllAttacksXPlatformFile.readlines()
		logger.info(f"Loaded {len(fuzzdbAllAttacksXPlatformInputs)} inputs from FuzzDB All Attacks X Platform.")

	# Load FuzzDB format strings
	fuzzdbFormatStringsInputs = []
	with open(FP_FUZZDB_FORMATSTRINGS, "r", encoding="utf-8") as fuzzdbFormatStringsFile:
		fuzzdbFormatStringsInputs = fuzzdbFormatStringsFile.readlines()
		logger.info(f"Loaded {len(fuzzdbFormatStringsInputs)} inputs from FuzzDB Format Strings.")

	# Load FuzzDB integer overloads
	fuzzdbIntegerOverloadsInputs = []
	with open(FP_FUZZDB_INTEGEROVERLOADS, "r", encoding="utf-8") as fuzzdbIntegerOverloadsFile:
		fuzzdbIntegerOverloadsInputs = fuzzdbIntegerOverloadsFile.readlines()
		logger.info(f"Loaded {len(fuzzdbIntegerOverloadsInputs)} inputs from FuzzDB Integer Overloads.")

	# Load FuzzDB invalid filenames linux
	fuzzdbInvalidFilenamesLinuxInputs = []
	with open(FP_FUZZDB_INVALIDFILENAMESLINUX, "r", encoding="utf-8") as fuzzdbInvalidFilenamesLinuxFile:
		fuzzdbInvalidFilenamesLinuxInputs = fuzzdbInvalidFilenamesLinuxFile.readlines()
		logger.info(f"Loaded {len(fuzzdbInvalidFilenamesLinuxInputs)} inputs from FuzzDB Invalid Filenames Linux.")

	'''
	FUZZING EXECUTION
	'''

	# Make a fuzz manager
	fuzzManager = FuzzManager()

	# Register fuzz input sources
	fuzzManager.registerFuzzInputSource("Big List of Naughty Strings", blnsInputs)
	fuzzManager.registerFuzzInputSource("FuzzDB All Attacks X Platform", fuzzdbAllAttacksXPlatformInputs)
	fuzzManager.registerFuzzInputSource("FuzzDB Format Strings", fuzzdbFormatStringsInputs)
	fuzzManager.registerFuzzInputSource("FuzzDB Integer Overloads", fuzzdbIntegerOverloadsInputs)
	fuzzManager.registerFuzzInputSource("FuzzDB Invalid Filenames Linux", fuzzdbInvalidFilenamesLinuxInputs)

	# Define list of functions to fuzz from target module
	functionsToFuzz = [dumpContentIntoFile, makeChunks, checkPythonFile, days_between, getPythonFileCount]

	# Perform fuzzing on targets and track key metrics
	fuzzingResults = {}
	for func in functionsToFuzz:
		logger.info(f"\n\n=== Beginning Fuzzing Function: {func.__name__} ===\n\n")
		fuzzResults = fuzzManager.performAllFuzzing(
			targetFunction=func,
			timeout=5.0
		)
		fuzzingResults[func.__name__] = fuzzResults
		logger.info(f"\n\n=== Completed Fuzzing Function: {func.__name__} ===\n\n")

	# Provide summary for the entire manager
	logger.info(f"\n\nTotal Fuzzing Summary:\n\n")
	logger.info(f" -> Total Fuzzes Run: {fuzzManager.totalFuzzesRun}")
	logger.info(f" -> Total Fuzzes Passed: {fuzzManager.totalFuzzesPassed}")
	logger.info(f" -> Total Fuzzes Failed: {fuzzManager.totalFuzzesFailed}")
	logger.info(f"\n\n========================================\n\n")