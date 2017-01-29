
import requests
import json
import urllib.parse


def get_cluster_options(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, turbot_account):
    """ Gets the current turbot vpc configuration for an account

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
