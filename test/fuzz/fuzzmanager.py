'''
Name: fuzzmanager.py
Author: Chris Hinkson @cmh02
Description: Provides a fuzzmanager class for easier fuzzing.
'''

'''
MODULE IMPORTS
'''

# System
import os
import tqdm
import inspect
import tempfile
import multiprocessing
from typing import Any, Dict, Iterable, Tuple

# Logging
from .logging import FuzzLogger

'''
CLASS DEFINITION
'''

class FuzzManager():
	'''
	# Fuzz Manager Class

	This class will manage fuzzing operations.
	'''

	def __init__(self):

		# Get logger
		self.logger = FuzzLogger()

		# Get subprocess manager
		self.manager = multiprocessing.Manager()

		# Make lists for holding fuzz input sources
		self.fuzzInputSources = {}

		# Create counters to track all fuzzing operations run through this instance
		self.totalFuzzesRun = 0
		self.totalFuzzesPassed = 0
		self.totalFuzzesFailed = 0

		# Log initialization
		self.logger.info(f"FuzzManager instance has been initialized with PID {os.getpid()}!")

	def registerFuzzInputSource(self, name: str, inputs: Iterable) -> None:
		'''
		## Register Fuzz Input Source

		Register a new fuzz input source by name.
		'''
		self.fuzzInputSources[name] = inputs
		self.logger.debug(f"Registered new fuzz input source '{name}' with {len(inputs)} inputs!")

	def performAllFuzzing(self, targetFunction: callable, timeout: float = 5.0) -> Dict[str, Any]:
		'''
		## Perform All Fuzzing

		Perform fuzzing on the target function using all registered fuzz input sources.
		'''

		# Log debug info
		self.logger.debug(f"Beginning fuzzing of function '{targetFunction}' with all registered input sources: {list(self.fuzzInputSources.keys())}!")

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

			# Log completion of this source
			self.logger.debug(f"Completed fuzzing of function '{targetFunction}' with input source '{fuzzInputName}'!")

		# Update instance counters
		self.totalFuzzesRun += allFuzzResults['totalFuzzes']
		self.totalFuzzesPassed += allFuzzResults['totalPass']
		self.totalFuzzesFailed += allFuzzResults['totalFail']

		# Return all fuzzing results
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
			target=FuzzManager.runFunctionWithArgs, 
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
	
	@staticmethod
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