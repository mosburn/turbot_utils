#!/usr/bin/env python

import turbotutils.cluster
import turbotutils.network
import requests
import urllib.parse
import json
import sys



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

    for account in accounts:

        subnets = turbotutils.network.get_turbot_vpc_subnets(turbot_api_access_key,turbot_api_secret_key,turbot_host_certificate_verification,turbot_host, account)
        print(account + ',' + str(subnets))
