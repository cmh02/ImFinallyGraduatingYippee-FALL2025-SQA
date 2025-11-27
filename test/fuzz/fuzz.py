'''
Name: fuzz.py
Author: Chris Hinkson @cmh02
Description: Fuzzing for the provided codebase in term project assignment.
'''

'''
GLOBAL MODULE IMPORTS
'''

# Typing Support
from multiprocessing import managers
from typing import Dict, Tuple, Iterable, Any

'''
GLOBAL FUZZING HELPER

This function will help with fuzzing target functions. It is kept global so that
it can be used with subprocessing.
'''

def runFunctionWithArgs(target: callable, args: Tuple[Any, ...], results: Dict, expectedExceptions: Tuple[type, ...] = (TypeError, ValueError)):
	results['target'] = str(target)
	results['args'] = str(args)
	results['result'] = None
	results['error'] = None
	results['status'] = None
	try:
		result = target(*args)
		results['result'] = result
		results['status'] = f"pass"
	except Exception as e:

		# Expected errors still get to pass
		if isinstance(e, expectedExceptions):
			results["error"] = f"Expected exception: {e}"
			results["status"] = f"pass"

		# Unexpected errors are fails
		else:
			results['error'] = str(e)
			results['status'] = f"fail"

'''
MAIN EXECUTION PATH
'''
if __name__ == "__main__":

	'''
	MODULE IMPORTS
	'''

	# System
	import os
	import json
	import tqdm
	import inspect
	import tempfile
	import multiprocessing
	from urllib import request

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
	print(f"Directory Setup has been completed!")
	print(f" -> Working Directory: {DIRECTORY_WORKING}")
	print(f" -> Resources Directory: {DIRECTORY_RESOURCES}")
	print(f" -> Output Directory: {DIRECTORY_OUTPUT}")

	'''
	RESOURCE DOWNLOAD

	For this project, I use two main external sources of fuzzing input:
	- Big List of Naughty Strings (https://github.com/minimaxir/big-list-of-naughty-strings)
	- FuzzDB (https://github.com/fuzzdb-project/fuzzdb)

	This section will download these resources if they are not already present.
	'''
		
	def downloadResource(url: str, filepath: str, name: str | None = None) -> bool:
		'''
		# Download Resource Helper

		Download a resource from a given URL to a specified filepath if it does not already exist.

		Args:
			url (str | None): The URL of the resource to download.
			filepath (str): The local file path where the resource should be saved.
			name (str): The name of the resource for logging purposes. Not required.

		Returns:
			out (bool): True if the resource was downloaded, False if it was already present.
		'''

		# Perform validation on inputs
		if not url or isinstance(url, str) is False:
			raise ValueError("An invalid url was supplied to the resource download helper!")
		if not filepath or isinstance(filepath, str) is False:
			raise ValueError("An invalid filepath was supplied to the resource download helper!")
		if name is not None and isinstance(name, str) is False:
			raise ValueError("An invalid name was supplied to the resource download helper!")
		
		# If no name was given, just use a general string
		if name is None:
			name = "Resource File"

		# Check if the file exists
		if os.path.exists(filepath):
			return False

		# Use urllib to download the resource
		with request.urlopen(url) as response:
			data = response.read()

		# Write the resource to the specified filepath
		with open(filepath, "wb") as resourceFile:
			resourceFile.write(data)

		# Return success
		return True

	# Big List of Naughty Strings
	FP_BLNS = os.path.join(DIRECTORY_RESOURCES, "blns.json")
	URL_BLNS = "https://raw.githubusercontent.com/minimaxir/big-list-of-naughty-strings/master/blns.json"
	if downloadResource(URL_BLNS, FP_BLNS, "Big List of Naughty Strings"):
		print(f"Big List of Naughty Strings downloaded to {FP_BLNS}!")
	else:
		print(f"Big List of Naughty Strings already present at {FP_BLNS}!")

	# Downnload FuzzDB all attacks x platform version
	FP_FUZZDB_ALLATTACKSXPLATFORM = os.path.join(DIRECTORY_RESOURCES, "all-attacks-xplatform.txt")
	URL_FUZZDB_ALLATTACKSXPLATFORM = "https://raw.githubusercontent.com/fuzzdb-project/fuzzdb/refs/heads/master/attack/all-attacks/all-attacks-xplatform.txt"
	if downloadResource(URL_FUZZDB_ALLATTACKSXPLATFORM, FP_FUZZDB_ALLATTACKSXPLATFORM, "FuzzDB All Attacks X Platform"):
		print(f"FuzzDB All Attacks X Platform downloaded to {FP_FUZZDB_ALLATTACKSXPLATFORM}!")
	else:
		print(f"FuzzDB All Attacks X Platform already present at {FP_FUZZDB_ALLATTACKSXPLATFORM}!")

	# Download FuzzDB format strings
	FP_FUZZDB_FORMATSTRINGS = os.path.join(DIRECTORY_RESOURCES, "format-strings.txt")
	URL_FUZZDB_FORMATSTRINGS = "https://raw.githubusercontent.com/fuzzdb-project/fuzzdb/refs/heads/master/attack/format-strings/format-strings.txt"
	if downloadResource(URL_FUZZDB_FORMATSTRINGS, FP_FUZZDB_FORMATSTRINGS, "FuzzDB Format Strings"):
		print(f"FuzzDB Format Strings downloaded to {FP_FUZZDB_FORMATSTRINGS}!")
	else:
		print(f"FuzzDB Format Strings already present at {FP_FUZZDB_FORMATSTRINGS}!")

	# Download FuzzDB integer overloads
	FP_FUZZDB_INTEGEROVERLOADS = os.path.join(DIRECTORY_RESOURCES, "integer-overloads.txt")
	URL_FUZZDB_INTEGEROVERLOADS = "https://raw.githubusercontent.com/fuzzdb-project/fuzzdb/refs/heads/master/attack/integer-overflow/integer-overflows.txt"
	if downloadResource(URL_FUZZDB_INTEGEROVERLOADS, FP_FUZZDB_INTEGEROVERLOADS, "FuzzDB Integer Overloads"):
		print(f"FuzzDB Integer Overloads downloaded to {FP_FUZZDB_INTEGEROVERLOADS}!")
	else:
		print(f"FuzzDB Integer Overloads already present at {FP_FUZZDB_INTEGEROVERLOADS}!")

	# Download FuzzDB invalid filenames
	FP_FUZZDB_INVALIDFILENAMESLINUX = os.path.join(DIRECTORY_RESOURCES, "invalid-filenames-linux.txt")
	URL_FUZZDB_INVALIDFILENAMESLINUX = "https://raw.githubusercontent.com/fuzzdb-project/fuzzdb/refs/heads/master/attack/file-upload/invalid-filenames-linux.txt"
	if downloadResource(URL_FUZZDB_INVALIDFILENAMESLINUX, FP_FUZZDB_INVALIDFILENAMESLINUX, "FuzzDB Invalid Filenames Linux"):
		print(f"FuzzDB Invalid Filenames Linux downloaded to {FP_FUZZDB_INVALIDFILENAMESLINUX}!")
	else:
		print(f"FuzzDB Invalid Filenames Linux already present at {FP_FUZZDB_INVALIDFILENAMESLINUX}!")

	'''
	RESOURCE LOADING

	This section loads the downloaded resources into memory for use as fuzzing inputs.
	'''

	# Load Big List of Naughty Strings
	blnsInputs = []
	with open(FP_BLNS, "r", encoding="utf-8") as blnsFile:
		blnsInputs = json.load(blnsFile)
		print(f"Loaded {len(blnsInputs)} inputs from Big List of Naughty Strings.")

	# Load FuzzDB all attacks x platform
	fuzzdbAllAttacksXPlatformInputs = []
	with open(FP_FUZZDB_ALLATTACKSXPLATFORM, "r", encoding="utf-8") as fuzzdbAllAttacksXPlatformFile:
		fuzzdbAllAttacksXPlatformInputs = fuzzdbAllAttacksXPlatformFile.readlines()
		print(f"Loaded {len(fuzzdbAllAttacksXPlatformInputs)} inputs from FuzzDB All Attacks X Platform.")

	# Load FuzzDB format strings
	fuzzdbFormatStringsInputs = []
	with open(FP_FUZZDB_FORMATSTRINGS, "r", encoding="utf-8") as fuzzdbFormatStringsFile:
		fuzzdbFormatStringsInputs = fuzzdbFormatStringsFile.readlines()
		print(f"Loaded {len(fuzzdbFormatStringsInputs)} inputs from FuzzDB Format Strings.")

	# Load FuzzDB integer overloads
	fuzzdbIntegerOverloadsInputs = []
	with open(FP_FUZZDB_INTEGEROVERLOADS, "r", encoding="utf-8") as fuzzdbIntegerOverloadsFile:
		fuzzdbIntegerOverloadsInputs = fuzzdbIntegerOverloadsFile.readlines()
		print(f"Loaded {len(fuzzdbIntegerOverloadsInputs)} inputs from FuzzDB Integer Overloads.")

	# Load FuzzDB invalid filenames linux
	fuzzdbInvalidFilenamesLinuxInputs = []
	with open(FP_FUZZDB_INVALIDFILENAMESLINUX, "r", encoding="utf-8") as fuzzdbInvalidFilenamesLinuxFile:
		fuzzdbInvalidFilenamesLinuxInputs = fuzzdbInvalidFilenamesLinuxFile.readlines()
		print(f"Loaded {len(fuzzdbInvalidFilenamesLinuxInputs)} inputs from FuzzDB Invalid Filenames Linux.")

	'''
	FUZZING SUPPORT
	'''
	
	class FuzzHandler():
		'''
		# Fuzz Handler Class

		This class will manage fuzzing operations.
		'''

		def __init__(self):

			# Get subprocess manager
			self.manager = multiprocessing.Manager()

			# Make lists for holding fuzz input sources
			self.fuzzInputSources = {}

		def registerFuzzInputSource(self, name: str, inputs: Iterable) -> None:
			'''
			## Register Fuzz Input Source

			Register a new fuzz input source by name.
			'''
			self.fuzzInputSources[name] = inputs

		def performAllFuzzing(self, targetFunction: callable, timeout: float = 5.0) -> Dict[str, Any]:
			'''
			## Perform All Fuzzing

			Perform fuzzing on the target function using all registered fuzz input sources.
			'''

			# Make a dict to hold all results
			allFuzzResults = {'sources': {}, 'totalPass': 0, 'totalFail': 0, 'totalFuzzes': 0}

			# Iterate over all registered fuzz input sources
			fuzzSourceIterator = tqdm.tqdm(
				iterable=self.fuzzInputSources.items(),
				desc=f"Performing Fuzzing On {targetFunction} With All Sources!",
				unit=f"source",
				colour=f"blue", 
				total=len(self.fuzzInputSources)
			)
			for fuzzInputName, fuzzInputs in fuzzSourceIterator:

				# Make a temporary directory for this fuzzing session
				with tempfile.TemporaryDirectory() as temporaryWorkingDirectory:

					try:
						# Change to the temporary directory
						originalWorkingDirectory = os.getcwd()
						os.chdir(temporaryWorkingDirectory)

						# Get results for this input source
						allFuzzResults['sources'][fuzzInputName] = self._performFuzzing(
							fuzzInputName=fuzzInputName,
							fuzzInputs=fuzzInputs,
							targetFunction=targetFunction,
							timeout=timeout
						)

					finally:

						# Change back to the original directory
						os.chdir(originalWorkingDirectory)

				# Update total counts
				allFuzzResults['totalPass'] += allFuzzResults['sources'][fuzzInputName]['totalPass']
				allFuzzResults['totalFail'] += allFuzzResults['sources'][fuzzInputName]['totalFail']
				allFuzzResults['totalFuzzes'] += allFuzzResults['sources'][fuzzInputName]['totalInputs']

				# Update progress bar
				fuzzSourceIterator.set_postfix({
					"Total Fuzzes Pass": allFuzzResults['totalPass'],
					"Total Fuzzes Fail": allFuzzResults['totalFail'],
					"Total Fuzzes": allFuzzResults['totalFuzzes']
				})
			return allFuzzResults

		def _performFuzzing(self, fuzzInputName: str, fuzzInputs: Iterable, targetFunction: callable, timeout: float = 5.0) -> Tuple[str, Any]:

			# Determine how many arguments the function has
			numArgs = len(inspect.signature(targetFunction).parameters)

			# Make trackers for this fuzz iteration
			results = []
			totalInputs = len(fuzzInputs)
			totalPass = 0
			totalFail = 0

			# Iterate over the fuzz inputs
			fuzzIterator = tqdm.tqdm(
				iterable=fuzzInputs, 
				desc=f" -> Performing Fuzzing with {fuzzInputName}!", 
				unit=f"input",
				colour=f"green", 
				total=totalInputs
			)
			for fuzzInput in fuzzIterator:

				# Prepare args based on the number of function arguments
				args = tuple(fuzzInput for _ in range(numArgs))

				# Fuzz the function with the current input
				processResults = self._fuzzFunctionWithInput(
					targetFunction=targetFunction, 
					args=args, 
					timeout=timeout
				)

				# Determine if the fuzzing was a pass or fail
				if processResults['status'] == f"pass":
					totalPass += 1
				else:
					totalFail += 1

				# Update progress bar
				fuzzIterator.set_postfix({
					"Fuzzes Passed": f"{totalPass:04d}",
					"Fuzzes Failed": f"{totalFail:04d}"
				})

				# Store the result
				results.append(processResults)

			# Return summary of fuzzing
			return {
				"fuzzInputName": fuzzInputName,
				"targetFunction": targetFunction,
				"numberOfArguments:": numArgs,
				"totalInputs": totalInputs,
				"totalPass": totalPass,
				"totalFail": totalFail,
				"results": results
			}

		def _fuzzFunctionWithInput(self, targetFunction: callable, args: Tuple[Any, ...], timeout: float = 5.0) -> Dict[str, Any]:
			'''
			## Fuzz Function With Input

			Fuzz a target function with given arguments using multiprocessing to enforce a timeout.
			'''

			# Create a dict that can be accessed in the new process
			processResults = self.manager.dict()

			# Start a process to run the target function with args and time it out if it takes too long
			p = multiprocessing.Process(
				target=runFunctionWithArgs, 
				args=(targetFunction, args, processResults)
			)
			p.start()
			p.join(timeout=timeout)

			# If the process is still alive after the timeout, terminate it and record a timeout error
			if p.is_alive():
				p.kill()
				processResults['error'] = f"TimeoutError: Function execution exceeded time limit ({timeout} seconds)!"
				processResults['status'] = f"fail"

			# Return the results as a normal dict
			return dict(processResults)



	'''
	MAIN EXECUTION
	'''

	# Make a fuzz handler
	fuzzHandler = FuzzHandler()

	# Register fuzz input sources
	fuzzHandler.registerFuzzInputSource("Big List of Naughty Strings", blnsInputs)
	fuzzHandler.registerFuzzInputSource("FuzzDB All Attacks X Platform", fuzzdbAllAttacksXPlatformInputs)
	fuzzHandler.registerFuzzInputSource("FuzzDB Format Strings", fuzzdbFormatStringsInputs)
	fuzzHandler.registerFuzzInputSource("FuzzDB Integer Overloads", fuzzdbIntegerOverloadsInputs)
	fuzzHandler.registerFuzzInputSource("FuzzDB Invalid Filenames Linux", fuzzdbInvalidFilenamesLinuxInputs)

	# Define list of functions to fuzz from target module
	from ...src.MLForensics_farzana.mining.mining import dumpContentIntoFile, makeChunks, checkPythonFile, days_between, getPythonFileCount
	functionsToFuzz = [dumpContentIntoFile, makeChunks, checkPythonFile, days_between, getPythonFileCount]

	# Perform fuzzing on targets
	for func in functionsToFuzz:
		print(f"\n\n=== Fuzzing Function: {func} ===\n\n")
		fuzzHandler.performAllFuzzing(
			targetFunction=func,
			timeout=5.0
		)
		print(f"\n\n=== Completed Fuzzing Function: {func} ===\n\n")