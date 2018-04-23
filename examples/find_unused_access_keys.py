#!/usr/bin/env python


import turbotutils.account
import boto3
import json


def main(account, region):
    session = boto3.Session(profile_name=account)
    client = session.client('iam', region_name=region)
    try:
        response = client.list_users()
        #responseObj = json.loads(response.text)
        for user in response['Users']:
            keys = client.list_access_keys(UserName=user['UserName'])
            if (keys['AccessKeyMetadata'][0]['Status']) == 'Inactive':
                print(keys['AccessKeyMetadata'][0]['UserName'], keys['AccessKeyMetadata'][0]['AccessKeyId'], account)
    except Exception as e:
        print(e, account)

if __name__ == '__main__':

    # Set to False if you do not have a valid certificate for your Turbot Host
    turbot_host_certificate_verification = True

    # Set to your Turbot Host URL
    turbot_host = turbotutils.get_turbot_host()

    turbot_user_id = turbotutils.get_turbot_user()

    # Get the turbot version
    api_version = turbotutils.get_api_version()

    # Get the access and secret key pairs
    (turbot_api_access_key, turbot_api_secret_key) = turbotutils.get_turbot_access_keys()
    region_name='us-east-1'
    accounts = turbotutils.cluster.get_turbot_account_ids(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, api_version)

    for account in accounts:
        turbot_account = account
        main(account, region_name)
