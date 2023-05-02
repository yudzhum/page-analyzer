import requests


def safe_request(url):
    result = None
    try:
        req = requests.get(url)

    except requests.exceptions.RequestException:
        return result

    else:
        return req
