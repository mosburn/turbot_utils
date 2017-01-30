#!/usr/bin/env python

import turbotutils
import turbotutils.network
import boto3
import boto.vpc
import sys


def turbot_main():
    # Set to False if you do not have a valid certificate for your Turbot Host
    turbot_host_certificate_verification = True

    # Set to your Turbot Host URL
    turbot_host = turbotutils.get_turbot_host()

    # Get the access and secret key pairs
    (turbot_api_access_key,turbot_api_secret_key) = turbotutils.get_turbot_access_keys()

    # Get the turbot account numbers
    accounts = turbotutils.get_turbot_account_ids(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host)
    for account in accounts:
        print("Checking %s" % account)
        #peers =
        resposne = turbotutils.query_yes_no("Do you want to break this peering?")


if __name__ == '__main__':
    profile = 'aay'
    region = 'us-east-1'
    mgmt_id = 'aac'
    connection = boto.vpc.connect_to_region(region_name=region, profile_name = profile)
    peers = connection.get_all_vpc_peering_connections()

    # First lets clean out all the peers but the management peer
    for peer in peers:

        tags = peer.tags
        if mgmt_id in tags['Name']:
            print(peer.id)
            print(peer.status_code)

        else:
            if peer.status_code == 'active':
                print('Deleting Peer named ' + peer.tags['Name'])
                connection.delete_vpc_peering_connection(peer.id)

    rt = connection.get_all_route_tables()

    for routes in rt:
        for route in routes.routes:
            if route.state == 'blackhole':
                print('Deleting blackholed route on table ' + routes.id)
                print(route.destination_cidr_block)
                connection.delete_route(route_table_id=routes.id, destination_cidr_block=route.destination_cidr_block)

        print(routes.tags)
