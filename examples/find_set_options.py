#!/usr/bin/env python

import turbotutils
import requests
import json
import urllib.parse


def get_cluster_id(turbot_host, turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification):
    """ Gets the cluster id
    # TODO: put this in cluster.py
    """
    api_method = "GET"
    api_url = "/api/v1/cluster"

    response = requests.request(
        api_method,
        urllib.parse.urljoin(turbot_host, api_url),
        auth=(turbot_api_access_key, turbot_api_secret_key),
        verify=turbot_host_certificate_verification,
        headers={
            'content-type': "application/json",
            'cache-control': "no-cache"
        }
    )

    # Convert the response JSON into a Python object
    responseObj = json.loads(response.text)
    urn = responseObj['urn']

    return urn

def get_option_list(turbot_host, turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, urn):
    """ Gets the turbot option list

    """
    api_method = "GET"
    api_url = "/api/v1/resources/" + urn + "/options/"

    response = requests.request(
        api_method,
        urllib.parse.urljoin(turbot_host, api_url),
        auth=(turbot_api_access_key, turbot_api_secret_key),
        verify=turbot_host_certificate_verification,
        headers={
            'content-type': "application/json",
            'cache-control': "no-cache"
        }
    )

    options_obj = json.loads(response.text)

    return options_obj['items']


def get_set_option(turbot_host, turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, urn, set_option):
    """ gets the set options"""

    api_method = "GET"
    api_url = "/api/v1/resources/" + urn + "/options/" + set_option


    response = requests.request(
        api_method,
        urllib.parse.urljoin(turbot_host, api_url),
        auth=(turbot_api_access_key, turbot_api_secret_key),
        verify=turbot_host_certificate_verification,
        headers={
            'content-type': "application/json",
            'cache-control': "no-cache"
        }
    )

    options_obj = json.loads(response.text)

    for child in options_obj['children']:
        print(child)


if __name__ == '__main__':
    # Set to False if you do not have a valid certificate for your Turbot Host
    turbot_host_certificate_verification = True

    # Set to your Turbot Host URL
    turbot_host = turbotutils.get_turbot_host()

    turbot_user_id = turbotutils.get_turbot_user()

    # Get the access and secret key pairs
    (turbot_api_access_key, turbot_api_secret_key) = turbotutils.get_turbot_access_keys()
    accounts = turbotutils.get_turbot_account_ids(turbot_api_access_key, turbot_api_secret_key,
                                                  turbot_host_certificate_verification, turbot_host)

    cluster_id = get_cluster_id(turbot_host, turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification)

    options = get_option_list(turbot_host, turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, cluster_id)

    for set_option in options:
        print('checking %s' % set_option)
        get_set_option(turbot_host, turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, cluster_id, set_option)