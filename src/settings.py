import os
import sys
import logging

from orator import Model
from orator import DatabaseManager

from py_database_url import orator

DATABASES = orator()

db = DatabaseManager(DATABASES)
Model.set_connection_resolver(db)

# Logs

formatter = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=formatter)
