from urllib.parse import urlsplit, urlunsplit


def url_parse(url):
    """
    Take url,
    return url as scheme+netloc
    """
    scheme, netloc, path, qs, anchor = urlsplit(url)
    path = ''
    qs = ''
    anchor = ''
    return (urlunsplit((scheme, netloc, path, qs, anchor)))
