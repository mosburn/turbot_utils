import requests
import json
import urllib.parse


def get_notifications_for_account(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, turbot_account):
    """ This returns the tick items notification stream from an account not the guardrail notifications"""
    api_method = "GET"
    api_url = "/api/v1/resources/%s/notifications?deep=true" % (turbot_account)
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

    return(responseObj['items'])


def get_guardrails_for_account(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, turbot_account):
    """ This returns the tick items notification stream from an account not the guardrail notifications"""
    api_method = "GET"
    api_url = "/api/v1/resources/%s/guardrails" % (turbot_account)
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


def get_guardrail_violation(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, turbot_account, alarm_urn):
    """ This returns the tick items notification stream from an account not the guardrail notifications"""
    api_method = "GET"
    api_url = "/api/v1/resources/%s/guardrails/%s/notifications" % (turbot_account, alarm_urn)
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


if __name__ == '__main__':
    import turbotutils
    turbot_host_certificate_verification = True

    # Set to your Turbot Host URL
    turbot_host = turbotutils.get_turbot_host()

    turbot_user_id = turbotutils.get_turbot_user()

    # Get the access and secret key pairs
    (turbot_api_access_key, turbot_api_secret_key) = turbotutils.get_turbot_access_keys()
    turbot_account = 'urn:turbot:mosburn:aaz'

    items = get_guardrails_for_account(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, turbot_account)

    for item in items:

        notification = get_guardrail_violation(turbot_api_access_key, turbot_api_access_key, turbot_host_certificate_verification, turbot_host, turbot_account,item['alarmUrn'])
        print(notification)
