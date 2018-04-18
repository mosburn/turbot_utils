#!/usr/bin/env python

import turbotutils
import turbotutils.account
import requests
import json
import urllib
import operator
from pprint import pprint


def get_notifications(turbot_host, turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, namespace, api_version):
    """ Gets the turbot notification for account
    
    :param turbot_host: turbot host
    :param turbot_api_access_key: turbot access key
    :param turbot_api_secret_key: turbot secret key
    :param turbot_host_certificate_verification: should be true
    :param namespace: the turbot namespace to look for alarms
    :param api_version: api version
    :return: Returns notification_list of all active notifications
    """
    api_method = "GET"
    api_url = "/api/%s/resources/%s/controls?filter=state:alarm,error" % (api_version, namespace)
    notification_list = []
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
    for notification in responseObj['items']:
        notification_list.append(notification['alarmUrn'])
    return notification_list


if __name__ == '__main__':
    # Set to False if you do not have a valid certificate for your Turbot Host
    turbot_host_certificate_verification = True

    # Set to your Turbot Host URL
    turbot_host = turbotutils.get_turbot_host()

    # Get the access and secret key pairs
    (turbot_api_access_key,turbot_api_secret_key) = turbotutils.get_turbot_access_keys()

    # Get the turbot version
    api_version = turbotutils.get_api_version()

    # Get the turbot account numbers
    cluster_id = turbotutils.cluster.get_cluster_id(turbot_host, turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, api_version)

    accounts = turbotutils.cluster.get_turbot_account_ids(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, api_version)

    top_level = 'urn:turbot'
    notification_list = []
    notification_count = {}
    for account_id in accounts:
        namespace = cluster_id + ":" + account_id
        for notification in get_notifications(turbot_host, turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, namespace, api_version):
            if notification in notification_count:
                notification_count[notification] += 1
            else:
                notification_count[notification] = 1

    sorted_dict = sorted(notification_count.items(), key=operator.itemgetter(1), reverse=True)

    pprint(sorted_dict)