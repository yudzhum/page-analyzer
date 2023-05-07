from urllib.parse import urlsplit, urlunsplit
from validators.url import url
from page_analyzer.data_parser import get_url_data
import requests


URL_MAX_LEN = 255


def url_validation(url_name):
    """
    Return a dict with data
    whether or not given value
    is a valid URL
    and message for flash messages if invalid.
    """
    result = {}
    if url_name == '':
        result['valid'] = False
        result['message'] = 'URL обязателен'
    elif url(url_name) and len(url_name) <= URL_MAX_LEN:
        result['valid'] = True
    else:
        result['valid'] = False
        result['message'] = 'Некорректный URL'
    return result


def url_parse(url_name):
    """
    Take url,
    return normalized url as scheme+netloc
    """
    scheme, netloc, path, qs, anchor = urlsplit(url_name)
    path = ''
    qs = ''
    anchor = ''
    return (urlunsplit((scheme, netloc, path, qs, anchor)))


def make_check(url_name):
    """
    Check url, if code status is 200 return request_data,
    otherwise return None
    """
    neg_result = None
    try:
        req_result = requests.get(url_name)
        req_result.raise_for_status()
        data = get_url_data(req_result.text)
        data['status_code'] = req_result.status_code

    except requests.exceptions.RequestException:
        return neg_result
    return data
