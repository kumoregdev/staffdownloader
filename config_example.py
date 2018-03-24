import logging


# Replace these department values. Anything not found will be left as is.
# Names to replace should be all lower case
REPLACE_DEPARTMENTS = {'department of the treasurer': 'Treasury',
                       'department of the secretary': 'Secretary',
                       'department of the chair': 'Chair'}

# Replace these position values. Values not found here will be left as is
REPLACE_POSITIONS = {'assistant to the director of relations (email coordinator)': 'Asst. to the Director of Relations',
                     'assistant to the director of publicity (email coordinator)': 'Asst. to the Director of Publicity',
                     'assistant director of infrastructure (hotel relations)': 'Asst. to the Director of Infrastructure (Hotel)',
                     'assistant director of infrastructure (convention)': 'Asst. Director of Infrastructure (Convention)',
                     'assistant director of relations (guests, industry, and hospitality)': 'Asst. Director of Relations (Guests)'}

# Save downloaded images here
OUTPUT_IMAGE_DIRECTORY = "/tmp/training/images"

# Save JSON files here (to be read by KumoReg)
OUTPUT_JSON_DIRECTORY = "/tmp/training/inbox"


STAFF_TOKEN_URL = 'REPLACE_ME'
IMAGE_TOKEN_URL = 'REPLACE_ME'
PASSWORD = "REPLACE_ME"

# URL pattern for staff data
STAFF_DATA_URL = 'REPLACE_ME'

# URL pattern for staff images
STAFF_IMAGE_URL = "REPLACE_ME"


# Save last run information in this file
LAST_RUN_FILENAME = "lastrun.json"

# Logging Configuration
LOG_FILENAME = "staff.log"
LOG_LEVEL = logging.INFO       # logging.INFO or logging.DEBUG

