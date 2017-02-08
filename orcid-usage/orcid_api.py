import requests
import config
import pprint


def get_access_token(scope, sandbox=True):
    headers = {
        'Accept': 'application/json',
    }

    data = {
        'client_id': config.CLIENT_ID_SANDBOX if sandbox else config.CLIENT_ID_PROD,
        'client_secret': config.CLIENT_SECRET_SANDBOX if sandbox else config.CLIENT_SECRET_PROD,
        'scope': scope,
        'grant_type': 'client_credentials',
    }

    url = config.SANDBOX_TOKEN_URL if sandbox else config.PROD_TOKEN_URL
    print '*****' + url

    response = requests.post(url, data=data, headers=headers)

    print data
    pprint.pprint(response.json)
    token = response.json()['access_token']

    return token


def read_public_record(orcid, token, sandbox=True):
    headers = {
        'Accept': 'application/orcid+xml',
        'Authorization': 'Bearer %s' % token,
    }

    url = (config.SANDBOX_ENDPOINT if sandbox else config.PROD_ENDPOINT) + '/v1.2/%s/orcid-profile/' % orcid
    response = requests.get(url, headers=headers)

    return response

def search(token, query, start, rows, sandbox=True):
    headers = {
        'Accept': 'application/orcid+xml',
        'Authorization': 'Bearer %s' % token,
    }
    url = (config.SANDBOX_ENDPOINT if sandbox else config.PROD_ENDPOINT) + '/v1.2/search/orcid-bio/?q=%s&start=%s&rows=%s' % (query,start,rows)
    response = requests.get(url, headers=headers)

    return response

