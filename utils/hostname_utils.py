import re

def extract_number_from_hostname(hostname):
    """Extract number from hostname like 'ca-01.jumptoserver.com'."""
    match = re.search(r'-(\d+)', hostname)
    return match.group(1) if match else '00'

def extract_double_vpn_country(hostname):
    """
    Extract the country code before '-dvpn' in the hostname.
    Example: 'us-dvpn.jumptoserver.com' -> 'us'
    """
    match = re.match(r'([a-z]{2})-dvpn\.', hostname)
    return match.group(1) if match else 'unknown'

def extract_prefix(hostname):
    """Extract the first label of a hostname.

    Example: 'ca-mnt2.jumptoserver.com' -> 'ca-mnt2'
    """
    return hostname.split('.')[0]

def extract_tail(hostname):
    """Extract the distinguishing part of a hostname prefix.

    Strips a leading two-letter country code and its separator, if present.
    Examples: 'ca-mnt2.jumptoserver.com' -> 'mnt2', 'auau.jumptoserver.com' -> 'auau'
    """
    prefix = extract_prefix(hostname)
    match = re.match(r'^[a-z]{2}-(.+)$', prefix)
    return match.group(1) if match else prefix
