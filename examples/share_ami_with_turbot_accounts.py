#!/usr/bin/env python

import turbotutils
import turbotutils.cluster
import boto3


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

    # Setup the aws connection to the source account
    client = boto3.client('ec2')

    for account in accounts:
        try:
            # Note: ami-809a8097 is a marketplace AMI, so it will not share correctly, however if you replace it with your
            # custom ami it will start sharing it out.
            response = client.modify_image_attribute(ImageId='ami-809a8097', LaunchPermission={'Add': [
                {
                    'UserId': str(account),
                    'Group': 'all'
                }]})
        except:
            print('Failed on account %s ' % account)