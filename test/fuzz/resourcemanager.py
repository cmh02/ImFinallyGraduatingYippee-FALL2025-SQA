'''
Name: resourcemanager.py
Author: Chris Hinkson @cmh02
Description: Provides a resource download helper.
'''

'''
MODULE IMPORTS
'''

# System
import os
from urllib import request

# Logging
from .logging import FuzzLogger

'''
CLASS DEFINITION
'''

class ResourceManager():

	@staticmethod
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

		# Get logger
		logger = FuzzLogger()

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