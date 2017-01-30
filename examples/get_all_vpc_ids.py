#!/usr/bin/env python

import turbotutils
import turbotutils.network

if __name__ == '__main__':
    # Set to False if you do not have a valid certificate for your Turbot Host
    turbot_host_certificate_verification = True

    # Set to your Turbot Host URL
    turbot_host = turbotutils.get_turbot_host()

    # Get the access and secret key pairs
    (turbot_api_access_key,turbot_api_secret_key) = turbotutils.get_turbot_access_keys()

    # Get the turbot account numbers
    turbotutils.network.get_all_vpcs_ids(turbot_api_access_key,turbot_api_secret_key, turbot_host_certificate_verification, turbot_host )