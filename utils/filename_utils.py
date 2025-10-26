import re

from .hostname_utils import extract_number_from_hostname, extract_double_vpn_country

def sanitize_filename(text):
    """Sanitize text to be used as a filename."""
    # Remove or replace invalid filename characters
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text.strip('-')

def generate_filename(server):
    """Generate filename based on country and city."""
    country = sanitize_filename(server['country'])
    city = server['city'].strip()

    if city:
        city_part = sanitize_filename(city)
    else:
        # If city is missing, extract number from hostname
        city_part = extract_number_from_hostname(server['hostname'])

    # Check if this is a streaming server
    hostname = server['hostname']
    if '-stream' in hostname:
        return f"{country}-{city_part}-streaming.conf"

    # Check if it's a Double VPN server
    if '-dvpn' in hostname:
        second_country = extract_double_vpn_country(hostname)
        return f"{country}-{city_part}-via-{second_country}.conf"

    # Check if this is a P2P server
    if hostname.endswith('-p2p.jumptoserver.com'):
        return f"{country}-{city_part}-p2p.conf"

    return f"{country}-{city_part}.conf"
