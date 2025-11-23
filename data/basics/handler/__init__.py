# Import handlers from the parent handler.py file
import sys
import importlib.util
from pathlib import Path

# Get the path to the parent handler.py file
handler_py_path = Path(__file__).parent.parent / 'handler.py'

# Load the handler.py module
spec = importlib.util.spec_from_file_location("basics.handler_module", handler_py_path)
handler_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(handler_module)

# Export the classes
CSVHandler = handler_module.CSVHandler
JSONHandler = handler_module.JSONHandler
XLSXHandler = handler_module.XLSXHandler

# Also export OracleHandler from this package
from .oracle_handler import OracleHandler

__all__ = ['CSVHandler', 'JSONHandler', 'XLSXHandler', 'OracleHandler']

