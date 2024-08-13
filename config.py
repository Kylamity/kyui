# File name: config.py
# Author: Kylamity

#--LOGGING
VERBOSE_LOGGING = False
DEFAULT_LOG_DIR = "logs"

#--URL REQUESTS
MIN_REQUEST_INTERVAL = 1 # min delay between sending requests
MAX_RETRY = 3 # max retry when request recieves an error
DELAY_ON_RETRY = 5 # additional request interval delay when retrying requests
RESPONSE_TIMEOUT = 30 # max time to wait for request response
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"

#--USER INTERFACE
BANNER_ART_ENABLED = True
DEFAULT_UI_COLOR = 'green' # supported options 'red', 'green', 'blue', 'yellow', 'purple', 'cyan', 'darkcyan', 'default'

