'''
Name: unit.py
Author: Chris Hinkson @cmh02
Description: Main entry point for fuzz CI testing.
'''

'''
MODULE IMPORTS
'''

# Target Module Imports
from src.MLForensics_farzana.mining.mining import dumpContentIntoFile, makeChunks, checkPythonFile, days_between, getPythonFileCount

# Unit Submodule Imports


# System
import os
import json
import textwrap