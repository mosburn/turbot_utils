#!/usr/bin/env python

""" Main turbot utilities module, this is the most common functions
.. moduleauthor:: Michael Osburn <michael@mosburn.com>

"""

import configparser
import os
import requests
import json
import sys
import urllib.parse


def get_turbot_host():
    """Gets the turbot master information from the config file

    :return: Returns the turbot URL as turbot_host
    """

    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~/.aws/turbothq'))
    turbot_dns_name = config.get('turbot', 'host')
    turbot_host = 'https://' + turbot_dns_name
    return turbot_host


def get_turbot_user():
    """Gets the turbot master information from the config file

    :return: Returns the turbot URL as turbot_host
    """

    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~/.aws/config'))
    turbot_user_id = config.get('default', 'turbot_user_id')

    return turbot_user_id


def get_turbot_access_keys():
    """ Gets the turbot access keypair

    :return: Returns the turbot access key pairs as turbot_api_access_key, turbot_api_secret_key
    """
    # Get the turbot access keys from the config file
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~/.aws/turbothq'))

    # Set to your Turbot API access keys
    turbot_api_access_key = config.get('turbot', 'access_key')
    turbot_api_secret_key = config.get('turbot', 'secret_key')

    return turbot_api_access_key,turbot_api_secret_key


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".

    :rtype bool

    :returns true or false
    """
    valid = {"yes": True, "y": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
