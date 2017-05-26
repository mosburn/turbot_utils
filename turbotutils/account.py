import requests
import json
import urllib.parse


def get_aws_access_key(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, turbot_account, turbot_user_id):
    """ Gets the federated access keys for a specified account

    :return: Returns the access key, secret key and session token for an account"""
    api_method = "POST"
    api_url = "/api/v1/accounts/%s/users/%s/awsCredentials" % (turbot_account, turbot_user_id)
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

    akey = responseObj['accessKeyId']
    skey = responseObj['secretAccessKey']
    token = responseObj['sessionToken']

    return (akey, skey, token)


def list_user_access_keys(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, turbot_account, turbot_user_id):
    """ Sets user access AKIA key pairs for a specified account

    NOTE: This requires a Cluster role Turbot/Owner or higher in order to work.
    """
    api_method = "GET"
    api_url = "/api/v1/accounts/%s/users/%s/awsAccessKeys" % (turbot_account, turbot_user_id)
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

    if'accessKeyId' in responseObj['items'][0]:

        exists = True
        akey = responseObj['items'][0]['accessKeyId']
    else:
        exists = False
        akey = False
    return (exists, akey)


def delete_user_access_keys(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, turbot_account, turbot_user_id, akey):
    """ Sets user access AKIA key pairs for a specified account

    NOTE: This requires a Cluster role Turbot/Owner or higher in order to work.
    """
    api_method = "DELETE"
    api_url = "/api/v1/accounts/%s/users/%s/awsAccessKeys/%s" % (turbot_account, turbot_user_id, akey)
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


def create_user_access_keys(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, turbot_account, turbot_user_id):
    """ Sets user access AKIA key pairs for a specified account

    NOTE: This requires a Cluster role Turbot/Owner or higher in order to work.
    """
    api_method = "POST"
    api_url = "/api/v1/accounts/%s/users/%s/awsAccessKeys" % (turbot_account, turbot_user_id)
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
    akey = responseObj['accessKeyId']
    skey = responseObj['secretAccessKey']
    return (akey, skey)


def get_account_tags(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, turbot_account):
    """ Sets user access AKIA key pairs for a specified account

    NOTE: This requires a Cluster role Turbot/Owner or higher in order to work.
    """
    api_method = "GET"
    api_url = "/api/v1/accounts/%s/" % (turbot_account)
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

    # If the account does not have tags, return false for an easy way to test later
    if 'tags' in responseObj:
        return responseObj['tags']
    else:
        return False


def create_user_ssh_keys(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, turbot_user_id):
    """ Sets user access AKIA key pairs for a specified account

    NOTE: This requires a Cluster role Turbot/Owner or higher in order to work.
    """
    api_method = "POST"
    api_url = "/api/v1/users/%s/sshKeys" % (turbot_user_id)
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
    return(responseObj['publicKey'])
