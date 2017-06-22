#!/usr/bin/env python

import turbotutils.cluster
import turbotutils.network
import requests
import urllib.parse
import json
import sys


def get_grants(turbot_host, turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, namespace, cluster_id=False):
    account_list = []
    api_method = "GET"
    api_url = "/api/v1/resources/%s/grants" % namespace

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
        if 'user' in obj:
            common_name = obj['user']['displayName']
        else:
            # Not all accounts have user displayname, most commonly nathan@turbot's
            dummy, common_name = obj['identityUrn'].split('::user:')

        if '_DELETED' in common_name:
            print('Former employee %s found in account %s' % (common_name, namespace))
        account_list.append(common_name)
    return account_list


if __name__ == '__main__':
    # Set to False if you do not have a valid certificate for your Turbot Host
    turbot_host_certificate_verification = True

    # Set to your Turbot Host URL
    turbot_host = turbotutils.get_turbot_host()

    # Get the access and secret key pairs
    (turbot_api_access_key,turbot_api_secret_key) = turbotutils.get_turbot_access_keys()
    cluster_id = turbotutils.cluster.get_cluster_id(turbot_host, turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification)

    # Get the turbot account numbers
    accounts = turbotutils.cluster.get_turbot_account_ids(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host)
    cluster_id = turbotutils.cluster.get_cluster_id(turbot_host, turbot_api_access_key, turbot_api_secret_key,
                                                    turbot_host_certificate_verification)
    top_level = 'urn:turbot'
    turbot_account_list = get_grants(turbot_host, turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, top_level)

    cluster_id = turbotutils.cluster.get_cluster_id(turbot_host, turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification)

    cluster_account_list = get_grants(turbot_host, turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, cluster_id)
    for account_id in cluster_account_list:
        if account_id not in turbot_account_list:
            turbot_account_list.append(account_id)
    for turbot_account in accounts:
        account_urn =  cluster_id + ':' + turbot_account
        account_list = get_grants(turbot_host, turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, account_urn, cluster_id)
        for account_id in account_list:
            if account_id not in turbot_account_list:
                turbot_account_list.append(account_id)

    turbot_account_list = sorted(set(turbot_account_list))

    for id in turbot_account_list:
        print(id)
