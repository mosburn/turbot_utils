#!/usr/bin/env python

import turbotutils
import turbotutils.account
import turbotutils.cluster
import boto3


def main(akey, skey, token):
    session = boto3.Session(aws_access_key_id=akey, aws_secret_access_key=skey, aws_session_token=token)
    client = session.client('iam', region_name='us-east-1')

    response = client.list_users()

    print(response)


if __name__ == '__main__':
    # Set to False if you do not have a valid certificate for your Turbot Host
    turbot_host_certificate_verification = True

    # Set to your Turbot Host URL
    turbot_host = turbotutils.get_turbot_host()

    turbot_user_id = turbotutils.get_turbot_user()

    # Get the access and secret key pairs
    (turbot_api_access_key, turbot_api_secret_key) = turbotutils.get_turbot_access_keys()
    accounts = turbotutils.cluster.get_turbot_account_ids(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host)

    for account in accounts:
        turbot_account = account
        print("Checking %s" % turbot_account)

        (akey, skey, token) = turbotutils.account.get_aws_access_key(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, turbot_account, turbot_user_id)

        main(akey,skey,token)
