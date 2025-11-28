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
import textwrap

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

	# Downnload FuzzDB all-attacks-xplatform.txt
	FP_FUZZDB_ALLATTACKSXPLATFORM = os.path.join(DIRECTORY_RESOURCES, "all-attacks-xplatform.txt")
	URL_FUZZDB_ALLATTACKSXPLATFORM = "https://raw.githubusercontent.com/fuzzdb-project/fuzzdb/refs/heads/master/attack/all-attacks/all-attacks-xplatform.txt"
	if ResourceManager.downloadResource(URL_FUZZDB_ALLATTACKSXPLATFORM, FP_FUZZDB_ALLATTACKSXPLATFORM, "FuzzDB All Attacks X Platform"):
		logger.info(f"FuzzDB All Attacks X Platform downloaded to {FP_FUZZDB_ALLATTACKSXPLATFORM}!")
	else:
		logger.info(f"FuzzDB All Attacks X Platform already present at {FP_FUZZDB_ALLATTACKSXPLATFORM}!")

	# Big List of Naughty Strings
	FP_BLNS = os.path.join(DIRECTORY_RESOURCES, "blns.json")
	URL_BLNS = "https://raw.githubusercontent.com/minimaxir/big-list-of-naughty-strings/master/blns.json"
	if ResourceManager.downloadResource(URL_BLNS, FP_BLNS, "Big List of Naughty Strings"):
		logger.info(f"Big List of Naughty Strings downloaded to {FP_BLNS}!")
	else:
		logger.info(f"Big List of Naughty Strings already present at {FP_BLNS}!")

	# Download FuzzDB Commands-Linux.txt
	FP_FUZZDB_COMMANDSLINUX = os.path.join(DIRECTORY_RESOURCES, "commands-linux.txt")
	URL_FUZZDB_COMMANDSLINUX = "https://raw.githubusercontent.com/fuzzdb-project/fuzzdb/refs/heads/master/attack/os-cmd-execution/Commands-Linux.txt"
	if ResourceManager.downloadResource(URL_FUZZDB_COMMANDSLINUX, FP_FUZZDB_COMMANDSLINUX, "FuzzDB Commands Linux"):
		logger.info(f"FuzzDB Commands Linux downloaded to {FP_FUZZDB_COMMANDSLINUX}!")
	else:
		logger.info(f"FuzzDB Commands Linux already present at {FP_FUZZDB_COMMANDSLINUX}!")

	# Download FuzzDB Commands-OSX.txt
	FP_FUZZDB_COMMANDSOSX = os.path.join(DIRECTORY_RESOURCES, "commands-osx.txt")
	URL_FUZZDB_COMMANDSOSX = "https://raw.githubusercontent.com/fuzzdb-project/fuzzdb/refs/heads/master/attack/os-cmd-execution/Commands-OSX.txt"
	if ResourceManager.downloadResource(URL_FUZZDB_COMMANDSOSX, FP_FUZZDB_COMMANDSOSX, "FuzzDB Commands OSX"):
		logger.info(f"FuzzDB Commands OSX downloaded to {FP_FUZZDB_COMMANDSOSX}!")
	else:
		logger.info(f"FuzzDB Commands OSX already present at {FP_FUZZDB_COMMANDSOSX}!")

	# Download FuzzDB directory-indexing-generic.txt
	FP_FUZZDB_DIRECTORYINDEXINGGENERIC = os.path.join(DIRECTORY_RESOURCES, "directory-indexing-generic.txt")
	URL_FUZZDB_DIRECTORYINDEXINGGENERIC = "https://raw.githubusercontent.com/fuzzdb-project/fuzzdb/refs/heads/master/attack/disclosure-directory/directory-indexing-generic.txt"
	if ResourceManager.downloadResource(URL_FUZZDB_DIRECTORYINDEXINGGENERIC, FP_FUZZDB_DIRECTORYINDEXINGGENERIC, "FuzzDB Directory Indexing Generic"):
		logger.info(f"FuzzDB Directory Indexing Generic downloaded to {FP_FUZZDB_DIRECTORYINDEXINGGENERIC}!")
	else:
		logger.info(f"FuzzDB Directory Indexing Generic already present at {FP_FUZZDB_DIRECTORYINDEXINGGENERIC}!")

	# Download FuzzDB directory-indexing.txt
	FP_FUZZDB_DIRECTORYINDEXING = os.path.join(DIRECTORY_RESOURCES, "directory-indexing.txt")
	URL_FUZZDB_DIRECTORYINDEXING = "https://raw.githubusercontent.com/fuzzdb-project/fuzzdb/refs/heads/master/attack/os-dir-indexing/directory-indexing.txt"
	if ResourceManager.downloadResource(URL_FUZZDB_DIRECTORYINDEXING, FP_FUZZDB_DIRECTORYINDEXING, "FuzzDB Directory Indexing"):
		logger.info(f"FuzzDB Directory Indexing downloaded to {FP_FUZZDB_DIRECTORYINDEXING}!")
	else:
		logger.info(f"FuzzDB Directory Indexing already present at {FP_FUZZDB_DIRECTORYINDEXING}!")

	# Download FuzzDB format-strings.txt
	FP_FUZZDB_FORMATSTRINGS = os.path.join(DIRECTORY_RESOURCES, "format-strings.txt")
	URL_FUZZDB_FORMATSTRINGS = "https://raw.githubusercontent.com/fuzzdb-project/fuzzdb/refs/heads/master/attack/format-strings/format-strings.txt"
	if ResourceManager.downloadResource(URL_FUZZDB_FORMATSTRINGS, FP_FUZZDB_FORMATSTRINGS, "FuzzDB Format Strings"):
		logger.info(f"FuzzDB Format Strings downloaded to {FP_FUZZDB_FORMATSTRINGS}!")
	else:
		logger.info(f"FuzzDB Format Strings already present at {FP_FUZZDB_FORMATSTRINGS}!")

	# Download FuzzDB HexValsAllBytes.txt
	FP_FUZZDB_HEXVALSALLBYTES = os.path.join(DIRECTORY_RESOURCES, "HexValsAllBytes.txt")
	URL_FUZZDB_HEXVALSALLBYTES = "https://raw.githubusercontent.com/fuzzdb-project/fuzzdb/refs/heads/master/attack/control-chars/HexValsAllBytes.txt"
	if ResourceManager.downloadResource(URL_FUZZDB_HEXVALSALLBYTES, FP_FUZZDB_HEXVALSALLBYTES, "FuzzDB Hex Vals All Bytes"):
		logger.info(f"FuzzDB Hex Vals All Bytes downloaded to {FP_FUZZDB_HEXVALSALLBYTES}!")
	else:
		logger.info(f"FuzzDB Hex Vals All Bytes already present at {FP_FUZZDB_HEXVALSALLBYTES}!")

	# Download FuzzDB integer-overloads.txt
	FP_FUZZDB_INTEGEROVERLOADS = os.path.join(DIRECTORY_RESOURCES, "integer-overloads.txt")
	URL_FUZZDB_INTEGEROVERLOADS = "https://raw.githubusercontent.com/fuzzdb-project/fuzzdb/refs/heads/master/attack/integer-overflow/integer-overflows.txt"
	if ResourceManager.downloadResource(URL_FUZZDB_INTEGEROVERLOADS, FP_FUZZDB_INTEGEROVERLOADS, "FuzzDB Integer Overloads"):
		logger.info(f"FuzzDB Integer Overloads downloaded to {FP_FUZZDB_INTEGEROVERLOADS}!")
	else:
		logger.info(f"FuzzDB Integer Overloads already present at {FP_FUZZDB_INTEGEROVERLOADS}!")

	# Download FuzzDB invalid-filenames-linux.txt
	FP_FUZZDB_INVALIDFILENAMESLINUX = os.path.join(DIRECTORY_RESOURCES, "invalid-filenames-linux.txt")
	URL_FUZZDB_INVALIDFILENAMESLINUX = "https://raw.githubusercontent.com/fuzzdb-project/fuzzdb/refs/heads/master/attack/file-upload/invalid-filenames-linux.txt"
	if ResourceManager.downloadResource(URL_FUZZDB_INVALIDFILENAMESLINUX, FP_FUZZDB_INVALIDFILENAMESLINUX, "FuzzDB Invalid Filenames Linux"):
		logger.info(f"FuzzDB Invalid Filenames Linux downloaded to {FP_FUZZDB_INVALIDFILENAMESLINUX}!")
	else:
		logger.info(f"FuzzDB Invalid Filenames Linux already present at {FP_FUZZDB_INVALIDFILENAMESLINUX}!")

	# Download FuzzDB NullByteRepesentations.txt
	FP_FUZZDB_NULLBYTEREPERESENTATIONS = os.path.join(DIRECTORY_RESOURCES, "NullByteRepresentations.txt")
	URL_FUZZDB_NULLBYTEREPERESENTATIONS = "https://raw.githubusercontent.com/fuzzdb-project/fuzzdb/refs/heads/master/attack/control-chars/NullByteRepresentations.txt"
	if ResourceManager.downloadResource(URL_FUZZDB_NULLBYTEREPERESENTATIONS, FP_FUZZDB_NULLBYTEREPERESENTATIONS, "FuzzDB Null Byte Representations"):
		logger.info(f"FuzzDB Null Byte Representations downloaded to {FP_FUZZDB_NULLBYTEREPERESENTATIONS}!")
	else:
		logger.info(f"FuzzDB Null Byte Representations already present at {FP_FUZZDB_NULLBYTEREPERESENTATIONS}!")

	# Download FuzzDB path-traversal-windows.txt
	FP_FUZZDB_PATHTRAVERSALWINDOWS = os.path.join(DIRECTORY_RESOURCES, "path-traversal-windows.txt")
	URL_FUZZDB_PATHTRAVERSALWINDOWS = "https://raw.githubusercontent.com/fuzzdb-project/fuzzdb/refs/heads/master/attack/path-traversal/path-traversal-windows.txt"
	if ResourceManager.downloadResource(URL_FUZZDB_PATHTRAVERSALWINDOWS, FP_FUZZDB_PATHTRAVERSALWINDOWS, "FuzzDB Path Traversal Windows"):
		logger.info(f"FuzzDB Path Traversal Windows downloaded to {FP_FUZZDB_PATHTRAVERSALWINDOWS}!")
	else:
		logger.info(f"FuzzDB Path Traversal Windows already present at {FP_FUZZDB_PATHTRAVERSALWINDOWS}!")

	# Download FuzzDB shell-delimiters.txt
	FP_FUZZDB_SHELLDELIMITERS = os.path.join(DIRECTORY_RESOURCES, "shell-delimiters.txt")
	URL_FUZZDB_SHELLDELIMITERS = "https://raw.githubusercontent.com/fuzzdb-project/fuzzdb/refs/heads/master/attack/os-cmd-execution/shell-delimiters.txt"
	if ResourceManager.downloadResource(URL_FUZZDB_SHELLDELIMITERS, FP_FUZZDB_SHELLDELIMITERS, "FuzzDB Shell Delimiters"):
		logger.info(f"FuzzDB Shell Delimiters downloaded to {FP_FUZZDB_SHELLDELIMITERS}!")
	else:
		logger.info(f"FuzzDB Shell Delimiters already present at {FP_FUZZDB_SHELLDELIMITERS}!")

	# Download FuzzDB shell-operators.txt
	FP_FUZZDB_SHELLOPERATORS = os.path.join(DIRECTORY_RESOURCES, "shell-operators.txt")
	URL_FUZZDB_SHELLOPERATORS = "https://raw.githubusercontent.com/fuzzdb-project/fuzzdb/refs/heads/master/attack/os-cmd-execution/shell-operators.txt"
	if ResourceManager.downloadResource(URL_FUZZDB_SHELLOPERATORS, FP_FUZZDB_SHELLOPERATORS, "FuzzDB Shell Operators"):
		logger.info(f"FuzzDB Shell Operators downloaded to {FP_FUZZDB_SHELLOPERATORS}!")
	else:
		logger.info(f"FuzzDB Shell Operators already present at {FP_FUZZDB_SHELLOPERATORS}!")

	# Download FuzzDB terminal-escape-codes.txt
	FP_FUZZDB_TERMINALESCAPECODES = os.path.join(DIRECTORY_RESOURCES, "terminal-escape-codes.txt")
	URL_FUZZDB_TERMINALESCAPECODES = "https://raw.githubusercontent.com/fuzzdb-project/fuzzdb/refs/heads/master/attack/control-chars/terminal-escape-codes.txt"
	if ResourceManager.downloadResource(URL_FUZZDB_TERMINALESCAPECODES, FP_FUZZDB_TERMINALESCAPECODES, "FuzzDB Terminal Escape Codes"):
		logger.info(f"FuzzDB Terminal Escape Codes downloaded to {FP_FUZZDB_TERMINALESCAPECODES}!")
	else:
		logger.info(f"FuzzDB Terminal Escape Codes already present at {FP_FUZZDB_TERMINALESCAPECODES}!")

	# Download FuzzDB true.txt
	FP_FUZZDB_TRUE = os.path.join(DIRECTORY_RESOURCES, "true.txt")
	URL_FUZZDB_TRUE = "https://raw.githubusercontent.com/fuzzdb-project/fuzzdb/refs/heads/master/attack/control-chars/true.txt"
	if ResourceManager.downloadResource(URL_FUZZDB_TRUE, FP_FUZZDB_TRUE, "FuzzDB True"):
		logger.info(f"FuzzDB True downloaded to {FP_FUZZDB_TRUE}!")
	else:
		logger.info(f"FuzzDB True already present at {FP_FUZZDB_TRUE}!")

	'''
	RESOURCE LOADING

	This section loads the downloaded resources into memory for use as fuzzing inputs.
	'''

	# Load FuzzDB all attacks x platform
	fuzzdbAllAttacksXPlatformInputs = ResourceManager.loadTxtResource(filePath=FP_FUZZDB_ALLATTACKSXPLATFORM)
	logger.info(f"Loaded {len(fuzzdbAllAttacksXPlatformInputs)} total inputs from FuzzDB All Attacks X Platform after processing.")

	# Load Big List of Naughty Strings
	blnsInputs = ResourceManager.loadTxtResource(filePath=FP_BLNS)
	logger.info(f"Loaded {len(blnsInputs)} total inputs from Big List of Naughty Strings after processing.")

	# Load FuzzDB commands linux
	fuzzdbCommandsLinuxInputs = ResourceManager.loadTxtResource(filePath=FP_FUZZDB_COMMANDSLINUX)
	logger.info(f"Loaded {len(fuzzdbCommandsLinuxInputs)} total inputs from FuzzDB Commands Linux after processing.")

	# Load FuzzDB commands osx
	fuzzdbCommandsOsxInputs = ResourceManager.loadTxtResource(filePath=FP_FUZZDB_COMMANDSOSX)
	logger.info(f"Loaded {len(fuzzdbCommandsOsxInputs)} total inputs from FuzzDB Commands OSX after processing.")

	# Load FuzzDB directory indexing generic
	fuzzdbDirectoryIndexingGenericInputs = ResourceManager.loadTxtResource(filePath=FP_FUZZDB_DIRECTORYINDEXINGGENERIC)
	logger.info(f"Loaded {len(fuzzdbDirectoryIndexingGenericInputs)} total inputs from FuzzDB Directory Indexing Generic after processing.")

	# Load FuzzDB directory indexing
	fuzzdbDirectoryIndexingInputs = ResourceManager.loadTxtResource(filePath=FP_FUZZDB_DIRECTORYINDEXING)
	logger.info(f"Loaded {len(fuzzdbDirectoryIndexingInputs)} total inputs from FuzzDB Directory Indexing after processing.")

	# Load FuzzDB format strings
	fuzzdbFormatStringsInputs = ResourceManager.loadTxtResource(filePath=FP_FUZZDB_FORMATSTRINGS)
	logger.info(f"Loaded {len(fuzzdbFormatStringsInputs)} total inputs from FuzzDB Format Strings after processing.")

	# Load FuzzDB hex vals all bytes
	fuzzdbHexValsAllBytesInputs = ResourceManager.loadTxtResource(filePath=FP_FUZZDB_HEXVALSALLBYTES)
	logger.info(f"Loaded {len(fuzzdbHexValsAllBytesInputs)} total inputs from FuzzDB Hex Vals All Bytes after processing.")

	# Load FuzzDB integer overloads
	fuzzdbIntegerOverloadsInputs = ResourceManager.loadTxtResource(filePath=FP_FUZZDB_INTEGEROVERLOADS)
	logger.info(f"Loaded {len(fuzzdbIntegerOverloadsInputs)} total inputs from FuzzDB Integer Overloads after processing.")

	# Load FuzzDB invalid filenames linux
	fuzzdbInvalidFilenamesLinuxInputs = ResourceManager.loadTxtResource(filePath=FP_FUZZDB_INVALIDFILENAMESLINUX)
	logger.info(f"Loaded {len(fuzzdbInvalidFilenamesLinuxInputs)} total inputs from FuzzDB Invalid Filenames Linux after processing.")

	# Load FuzzDB null byte representations
	fuzzdbNullByteRepresentationsInputs = ResourceManager.loadTxtResource(filePath=FP_FUZZDB_NULLBYTEREPERESENTATIONS)
	logger.info(f"Loaded {len(fuzzdbNullByteRepresentationsInputs)} total inputs from FuzzDB Null Byte Representations after processing.")

	# Load FuzzDB path traversal windows
	fuzzdbPathTraversalWindowsInputs = ResourceManager.loadTxtResource(filePath=FP_FUZZDB_PATHTRAVERSALWINDOWS)
	logger.info(f"Loaded {len(fuzzdbPathTraversalWindowsInputs)} total inputs from FuzzDB Path Traversal Windows after processing.")

	# Load FuzzDB shell delimiters
	fuzzdbShellDelimitersInputs = ResourceManager.loadTxtResource(filePath=FP_FUZZDB_SHELLDELIMITERS)
	logger.info(f"Loaded {len(fuzzdbShellDelimitersInputs)} total inputs from FuzzDB Shell Delimiters after processing.")

	# Load FuzzDB shell operators
	fuzzdbShellOperatorsInputs = ResourceManager.loadTxtResource(filePath=FP_FUZZDB_SHELLOPERATORS)
	logger.info(f"Loaded {len(fuzzdbShellOperatorsInputs)} total inputs from FuzzDB Shell Operators after processing.")

	# Load FuzzDB terminal escape codes
	fuzzdbTerminalEscapeCodesInputs = ResourceManager.loadTxtResource(filePath=FP_FUZZDB_TERMINALESCAPECODES)
	logger.info(f"Loaded {len(fuzzdbTerminalEscapeCodesInputs)} total inputs from FuzzDB Terminal Escape Codes after processing.")

	# Load FuzzDB true
	fuzzdbTrueInputs = ResourceManager.loadTxtResource(filePath=FP_FUZZDB_TRUE)
	logger.info(f"Loaded {len(fuzzdbTrueInputs)} total inputs from FuzzDB True after processing.")

	'''
	FUZZING EXECUTION
	'''

	# Make a fuzz manager
	fuzzManager = FuzzManager()

	# Register fuzz input sources
	fuzzManager.registerFuzzInputSource("FuzzDB All Attacks X Platform", fuzzdbAllAttacksXPlatformInputs)
	fuzzManager.registerFuzzInputSource("Big List of Naughty Strings", blnsInputs)
	fuzzManager.registerFuzzInputSource("FuzzDB Commands Linux", fuzzdbCommandsLinuxInputs)
	fuzzManager.registerFuzzInputSource("FuzzDB Commands OSX", fuzzdbCommandsOsxInputs)
	fuzzManager.registerFuzzInputSource("FuzzDB Directory Indexing Generic", fuzzdbDirectoryIndexingGenericInputs)
	fuzzManager.registerFuzzInputSource("FuzzDB Directory Indexing", fuzzdbDirectoryIndexingInputs)
	fuzzManager.registerFuzzInputSource("FuzzDB Format Strings", fuzzdbFormatStringsInputs)
	fuzzManager.registerFuzzInputSource("FuzzDB Hex Vals All Bytes", fuzzdbHexValsAllBytesInputs)
	fuzzManager.registerFuzzInputSource("FuzzDB Integer Overloads", fuzzdbIntegerOverloadsInputs)
	fuzzManager.registerFuzzInputSource("FuzzDB Invalid Filenames Linux", fuzzdbInvalidFilenamesLinuxInputs)
	fuzzManager.registerFuzzInputSource("FuzzDB Null Byte Representations", fuzzdbNullByteRepresentationsInputs)
	fuzzManager.registerFuzzInputSource("FuzzDB Path Traversal Windows", fuzzdbPathTraversalWindowsInputs)
	fuzzManager.registerFuzzInputSource("FuzzDB Shell Delimiters", fuzzdbShellDelimitersInputs)
	fuzzManager.registerFuzzInputSource("FuzzDB Shell Operators", fuzzdbShellOperatorsInputs)
	fuzzManager.registerFuzzInputSource("FuzzDB Terminal Escape Codes", fuzzdbTerminalEscapeCodesInputs)
	fuzzManager.registerFuzzInputSource("FuzzDB True", fuzzdbTrueInputs)

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

	'''
	SUMMARY OUTPUT
	'''

	# Make top-level header
	summary = textwrap.dedent(f"""
			# Continuous Integration: Fuzzing Summary
			""")
	
	# Add overall results section
	summary += textwrap.dedent(f"""
				## Overall Results

				Total Fuzzed Functions: {len(functionsToFuzz)}
				Total Fuzzing Operations Run: {fuzzManager.totalFuzzesRun}  
				Total Fuzzing Operations Passed: {fuzzManager.totalFuzzesPassed}  
				Total Fuzzing Operations Failed: {fuzzManager.totalFuzzesFailed}
				""")
	
	# Add per-function results
	summary += textwrap.dedent(f"""
			## Per-Function Results
			""")
	for name, results in fuzzingResults.items():
		summary += textwrap.dedent(f"""
					### Function: {name}

					Total Fuzzing Operations Run: {results['totalFuzzes']}  
					Total Fuzzing Operations Passed: {results['totalPass']}  
					Total Fuzzing Operations Failed: {results['totalFail']}  
					""")
		
		# Sort error counts by frequency
		if 'errorCounts' is not None:
			summary += 	textwrap.dedent(f"""
						Error Counts:
						""")

			sortedErrorCounts = dict(sorted(results.get('errorCounts', {}).items(), key=lambda item: item[1], reverse=True))
			for errorName, errorCount in sortedErrorCounts.items():
				summary += textwrap.dedent(f"""
							- {errorName}: {errorCount}
							""")

	# Write summary to md file for viewing
	with open("fuzzingsummary.md", "w") as summaryFile:
		summaryFile.write(summary)