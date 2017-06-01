#!/usr/bin/env python

import turbotutils.cluster
import requests
import urllib.parse
import json


def delete_fingerprint(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, turbot_user_id, finger):
    api_method = "DELETE"
    api_url = "/api/v1/users/%s/sshKeys/%s" % (turbot_user_id, finger)
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


def get_ssh_fingerprints(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, turbot_user_id):
    """ Sets user access AKIA key pairs for a specified account

    NOTE: This requires a Cluster role Turbot/Owner or higher in order to work.
    """
    fingerprints = []
    api_method = "GET"
    api_url = "/api/v1/users/%s/sshKeys" % (turbot_user_id)
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

    responseObj = json.loads(response.text)

    for item in responseObj['items']:
        fingerprints.append(item['fingerprint'])
    return(fingerprints)


if __name__ == '__main__':
    # Set to False if you do not have a valid certificate for your Turbot Host
    turbot_host_certificate_verification = True

    # Set to your Turbot Host URL
    turbot_host = turbotutils.get_turbot_host()
    turbot_user_id = turbotutils.get_turbot_user()
    # Get the access and secret key pairs
    (turbot_api_access_key,turbot_api_secret_key) = turbotutils.get_turbot_access_keys()
    delete = 'YES'
    turbot_user_id= 'dummy_user'
    cluster_id = turbotutils.cluster.get_cluster_id(turbot_host, turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification)
    fingerprints = get_ssh_fingerprints(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, turbot_user_id)

    if not fingerprints:
        if delete == 'YES':
            for finger in fingerprints:
                delete_fingerprint(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, turbot_user_id, finger)
