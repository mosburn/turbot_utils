
import requests
import json
import urllib.parse


def get_cluster_id(turbot_host, turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification):
    """ Gets the cluster id
    # TODO: put this in cluster.py
    """
    api_method = "GET"
    api_url = "/api/v1/cluster"

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
    urn = responseObj['urn']

    return urn


def get_cluster_options(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, turbot_account):
    """ Gets the current turbot vpc configuration for an account
    TODO: refactor this
    :return: Returns the current turbot VPC configuration
    """
    api_method = "GET"
    api_url = "/api/v1/cluster"
    vpc_list = []

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
        vpc_list.append(obj['subnets'])

    return vpc_list


def get_turbot_account_ids(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host):
    """ Gets the current turbot account names

    :return: Returns a list of turbot account names as accounts
    """
    # Set to the required API request type and location
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
        accounts.append(obj['awsAccountId'])

    return accounts