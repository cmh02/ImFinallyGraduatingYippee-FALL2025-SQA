'''
Name: logging.py
Author: Chris Hinkson @cmh02
Description: Logging setup for unit testing.
'''

'''
MODULE IMPORTS
'''

# System
import os
import logging
from datetime import datetime

'''
GLOBAL LOGGER INSTANCE / DEFINITION
'''

_logger = None
def UnitLogger(name: str = None, log_dir: str = "logs") -> logging.Logger:
    
    # If already initialized, return existing logger
    global _logger
    if _logger is not None:
        return _logger

    # Create logs directory
    os.makedirs(log_dir, exist_ok=True)

    # File path with timestamp
    log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

    # Create logger
    if name is not None:
        logger = logging.getLogger(name)
    else:
        logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Prevent adding multiple handlers if imported repeatedly
    if not logger.handlers:

        # Send all logs to file
        fileLogger = logging.FileHandler(log_file, encoding="utf-8")
        fileLogger.setLevel(logging.DEBUG)
        fileLogger.setFormatter(
            logging.Formatter(
				"[%(asctime)s] [%(levelname)s] %(message)s",
				datefmt="%Y-%m-%d %H:%M:%S"
        	)
        )
        logger.addHandler(fileLogger)

        # Send INFO+ logs to console
        consoleLogger = logging.StreamHandler()
        consoleLogger.setLevel(logging.DEBUG)
        consoleLogger.setFormatter(
            logging.Formatter(
				"%(levelname)s: %(message)s"
			)
		)
        logger.addHandler(consoleLogger)

    _logger = logger
    return logger