#!/usr/bin/env python

import turbotutils.cluster
import turbotutils.network
import requests
import urllib.parse
import json
import sys

def get_turbot_account_ids(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host):
    """ Gets the current turbot account names

    :return: Returns a list of turbot account names as accounts
    """
    # Set to the required API request type and location
    accounts = []
    api_method = "GET"
    api_url = "/api/v1/accounts"

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

    for obj in responseObj['items']:
        accounts[obj['id']] = obj['awsAccountId']

    return accounts


if __name__ == '__main__':
    # Set to False if you do not have a valid certificate for your Turbot Host
    turbot_host_certificate_verification = True

    # Set to your Turbot Host URL
    turbot_host = turbotutils.get_turbot_host()

    # Get the access and secret key pairs
    (turbot_api_access_key,turbot_api_secret_key) = turbotutils.get_turbot_access_keys()
    cluster_id = turbotutils.cluster.get_cluster_id(turbot_host, turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification)

    # Get the turbot account numbers
    accounts = get_turbot_account_ids(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host)
    for turbot_account,account_number,account_name in accounts.items():

        print("Checking %s-%s-%s" % (account_name, account_number, account_name))
        subnets = turbotutils.network.get_turbot_vpc_subnets(turbot_api_access_key,turbot_api_secret_key,turbot_host_certificate_verification,turbot_host, turbot_account)
        print(subnets)
