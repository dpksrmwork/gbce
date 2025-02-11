import logging
import sys

# Create a logger instance
logger = logging.getLogger("gbc_app")
logger.setLevel(logging.DEBUG)  # Set minimum logging level

# Create a console handler (logs to stdout)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)  # Set log level for console

# Create a file handler (logs to a file)
file_handler = logging.FileHandler("gbc_app.log")
file_handler.setLevel(logging.INFO)  # Store only INFO+ logs in a file

# Define log format
log_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(log_format)
file_handler.setFormatter(log_format)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
