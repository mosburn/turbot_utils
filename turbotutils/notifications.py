import requests
import json
import urllib.parse


def get_notifications_for_account(turbot_host, turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, namespace, api_version):
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
    api_url = "/api/%s/resources/%s/controls" % (api_version, namespace)
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


def get_guardrails_for_account(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, turbot_account, api_version):
    """ This returns the tick items notification stream from an account not the guardrail notifications"""
    api_method = "GET"
    api_url = "/api/%s/resources/%s/guardrails" % (api_version, turbot_account)
    response = requests.request(
        api_method,
        urllib.parse.urljoin(turbot_host, api_url),
        auth=(turbot_api_access_key, turbot_api_secret_key),
        verify=turbot_host_certificate_verification,
        headers={
            'content-type': "application/json",
            'cache-control': "no-cache"
        },

    )

    responseObj = json.loads(response.text)

    return (responseObj['items'])


def get_guardrail_violation(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, turbot_account, alarm_urn, api_version):
    """ This returns the tick items notification stream from an account not the guardrail notifications"""
    api_method = "GET"
    api_url = "/api/%s/resources/%s/guardrails/%s/notifications" % (api_version, turbot_account, alarm_urn)
    response = requests.request(
        api_method,
        urllib.parse.urljoin(turbot_host, api_url),
        auth=(turbot_api_access_key, turbot_api_secret_key),
        verify=turbot_host_certificate_verification,
        headers={
            'content-type': "application/json",
            'cache-control': "no-cache"
        },

    )

    responseObj = json.loads(response.text)

    return (responseObj)


