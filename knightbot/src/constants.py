"""
constants.py
"""

import datetime
import json
import os

_constants = {}
_env_directory = '../resources/env'
_env_location = os.path.join(_env_directory, 'env.json')

# Should be in cache directory
#
# !!! FIX !!!
#
_prefix_location = os.path.join(_env_directory, 'prefix.json')

def initialise () -> None:
    """
    Reads important information from env.json where important information
    required for the Knight to run is stored
    """

    global _constants

    with open(_env_location, 'r', encoding = 'utf-8') as env:
        content = env.read()
        _constants.update(json.loads(content))

    with open(_prefix_location, 'r', encoding = 'utf-8') as prefix:
        content = prefix.read()
        _constants.update(json.loads(content))

def get_custom_prefix () -> dict:
    return _constants['custom_prefix']

def get_default_prefix () -> dict:
    return _constants['default_prefix']

def get_name () -> str:
    return _constants['name']

def get_owner () -> int:
    return int(_constants['owner'])

def get_support () -> str:
    return _constants['support']

def get_token () -> str:
    return _constants['token']

def get_cache_directory () -> str:
    return '../resources/cache'

def get_env_directory () -> str:
    return '../resources/env'

def get_log_directory () -> str:
    return '../resources/logs'

def get_current_time ():
    """Returns the UTC time with microseconds set to 0 for convenience purposes"""
    return datetime.datetime.utcnow().replace(microsecond = 0)

initialise()
