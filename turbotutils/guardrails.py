import requests
import json
import urllib.parse


def get_guardrail_list(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, turbot_account_urn):
    """ Gets the list of guardrails

    :returns: Returns a list of the guardrails"""

    api_method = "GET"
    api_url = "/api/v1/resources/%s/options" % (turbot_account_urn)
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


def get_guardrail(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, turbot_account_urn, guardrail):
    """ Gets a guardrail

    :returns: returns a guardrail setting """

    api_method = "GET"
    api_url = "/api/v1/resources/%s/options/%s" % (turbot_account_urn, guardrail)

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
    print(responseObj['value'])
    return responseObj['value']

