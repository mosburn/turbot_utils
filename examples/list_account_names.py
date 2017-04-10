#!/usr/bin/env python

import turbotutils.account
import turbotutils.cluster
import requests
import json
import urllib.parse

""" simple script to use turbot to rotate your access keys"""
if __name__ == '__main__':

    turbot_host_certificate_verification = True

    # Set to your Turbot Host URL
    turbot_host = turbotutils.get_turbot_host()

    turbot_user_id = turbotutils.get_turbot_user()

    # Get the access and secret key pairs
    (turbot_api_access_key, turbot_api_secret_key) = turbotutils.get_turbot_access_keys()
    accounts = []
    api_method = "GET"
    api_url = "/api/v1/accounts"

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
        print(obj['id'], obj['title'])