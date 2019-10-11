import os
import sys
import logging
from logging.handlers import RotatingFileHandler

def configure_logging(name, log_directory, log_level):
	""" Configure File Logger

	Parameters
	----------
	name : str
	    Logger name for outputting messages.

	log_directory: str
		Directory where logs are stored.

	log_level: str
		Log Level for determining types of messages that are stored.

	Returns
	-------
	logging.Logger
	    Logger with RotatingFileHandler and StreamHandler
	"""

	# Set up logfile and message logging.

	logger = logging.getLogger(name)
	logger.setLevel(log_level)

	# Create the rotating file handler. Limit the size to 5000000Bytes ~ 5MB .
	file_path = os.path.join(log_directory, '%s.log' % name)
	rotating_handler = RotatingFileHandler(file_path, mode='a', maxBytes=5000000, backupCount=1, encoding='utf-8', delay=0)
	rotating_handler.setLevel(log_level)

	# Create a stream handler.
	stream_handler = logging.StreamHandler(sys.stdout)
	stream_handler.setLevel(log_level)

	# Create a formatter.
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

	# Add handlers and formatters.
	rotating_handler.setFormatter(formatter)
	stream_handler.setFormatter(formatter)

	logger.addHandler(rotating_handler)
	logger.addHandler(stream_handler)

	return logger