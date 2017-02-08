

def get_account_bill(turbot_host, turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, accountId):
    """ Gets the month to date charges for a given account

    """
    import requests
    import json
    import urllib.parse
    api_method = "GET"
    api_url = "/api/v1/accounts/%s/aws/estimatedCharges" % accountId

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

    print(responseObj['charges']['monthToDate'])

