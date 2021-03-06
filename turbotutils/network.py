
import requests
import json
import urllib.parse


def get_turbot_vpc_subnets(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, turbot_account, api_version):
    """ Gets the current turbot vpc configuration for an account

    :return: Returns the current turbot VPC configuration
    """
    api_method = "GET"
    api_url = "/api/%s/accounts/%s/vpcs" % (api_version, turbot_account)
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


def get_all_vpcs_ids(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, api_version):
    """ Gets a list of the turbot VPCs

    :return: Returns a list of turbot VPCS"""

    # Set to the required API request type and location
    api_method = "GET"
    api_url = "/api/%s/accounts" % (api_version)

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

    return responseObj['items']
