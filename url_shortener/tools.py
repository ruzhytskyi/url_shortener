from hashlib import md5

def make_hash(string):
    """
    Returns 8-symbols hash of string. Symbols can be [a-z][0-9]
    """  
    return md5(string).hexdigest()[:8]

def make_short_url(host, port, url_hash):
    """
    Returns an url composed from domain name and hash
    """
    return "http://%s:%s/%s" % (host, port, url_hash)
