#!/usr/bin/env python
''' Adds a user to an arbituary account with the specified grants,
    Requires the executor to have permissions to do the same
'''

import turbotutils.cluster
import configparser
import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Adds a user to turbot account with specified grants')
    parser.add_argument('account', help='Turbot account_id')
    parser.add_argument('user_name', help='Turbot Username')
    parser.add_argument('grant', help="Grant to add for a user")
    args = parser.parse_args()

    config = configparser.ConfigParser()
    conf_file = os.path.expanduser('~/.aws/credentials')
    config.read(conf_file)
    # Set to False if you do not have a valid certificate for your Turbot Host
    turbot_host_certificate_verification = True

    # Set to your Turbot Host URL
    turbot_host = turbotutils.get_turbot_host()

    turbot_user_id = turbotutils.get_turbot_user()

    # Get the access and secret key pairs
    (turbot_api_access_key, turbot_api_secret_key) = turbotutils.get_turbot_access_keys()

    cluster_id = turbotutils.cluster.get_cluster_id(turbot_host, turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification)

    account = turbotutils.cluster.validate_account(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, args.account)
    urn =  cluster_id + ':' + account

    userarn = cluster_id + '::user:' + args.user_name
    permissions = args.grant
    turbotutils.account.add_user_to_account(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host,
                        userarn, permissions, urn)
