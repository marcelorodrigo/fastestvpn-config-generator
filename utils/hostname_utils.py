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
