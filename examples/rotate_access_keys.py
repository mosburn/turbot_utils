#!/usr/bin/env python

import turbotutils.account
import turbotutils.cluster
import time
import configparser
import os


def rotate_keys():
    """ Simple function to rotate aws access keys"""
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

    # Get the turbot version
    api_version = turbotutils.get_api_version()

    accounts = turbotutils.cluster.get_turbot_account_ids(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, api_version)

    for account in accounts:
        turbot_account = account
        print("Checking %s" % turbot_account)
        key_exists = False
        try:

            (key_exists,akey) = turbotutils.account.list_user_access_keys(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, turbot_account, turbot_user_id, api_version)
            if key_exists:
                print('Access Key already exists, deleting %s' % akey)
                turbotutils.account.delete_user_access_keys(turbot_api_access_key, turbot_api_secret_key,
                                                            turbot_host_certificate_verification, turbot_host,
                                                            turbot_account, turbot_user_id, akey, api_version)
                time.sleep(1)

            (akey, skey) = turbotutils.account.create_user_access_keys(turbot_api_access_key, turbot_api_secret_key,
                                                                       turbot_host_certificate_verification,
                                                                       turbot_host, turbot_account, turbot_user_id, api_version)
            if not config.has_section(account):
                config.add_section(account)
            config[account]['aws_access_key_id'] = akey
            config[account]['aws_secret_access_key'] = skey
        except Exception as e:
            # TODO: Figure out what to do with 'e' later
            error = e


    with open(conf_file, 'w') as configfile:

        config.write(configfile)


if __name__ == '__main__':
    rotate_keys()
