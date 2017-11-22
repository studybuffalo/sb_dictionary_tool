import configparser
from django.core.wsgi import get_wsgi_application
import logging
import logging.config
import os
import sys
from unipath import Path

# APPLICATION SETUP
# Setup root path
root = Path(sys.argv[1])

# Collect the config file
config = configparser.ConfigParser()
config.read(Path(root.parent, "config", "sb_dictionary_tool.cfg"))

# Setup Logging
log_config = Path(root.parent, "config", "sb_dictionary_tool_logging.cfg")
logging.config.fileConfig(log_config, disable_existing_loggers=False)
log = logging.getLogger(__name__)

# Require critical logging for Django and Requests logging
logging.getLogger("environ").setLevel(logging.CRITICAL)

 # Setup the Django database connection
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", config.get("django", "settings")
)
sys.path.append(config.get("django", "location"))
application = get_wsgi_application()

from modules import extraction, review, upload

log.debug("STUDY BUFFALO DICTIONARY TOOL STARTED")

# Retrieve a list of all the words to review

# Access the dictionary application to retrieve all the data on things to monitor

# Access each monitored application and download all the data from the fields

# Take all the extracted data and convert it to a list of single words

# Remove any duplicate words

# For each word, check if it exists in the dictionary or excluded lists
# If not, upload the word to the pending dictionary

log.debug("STUDY BUFFALO DICTIONARY TOOL COMPLETED")