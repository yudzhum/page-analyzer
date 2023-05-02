import requests


def safe_request(url):
    result = None
    try:
        req = requests.get(url)
        if req.status_code == 200:
            return req

    except requests.exceptions.RequestException:
        return result

    else:
        return result
