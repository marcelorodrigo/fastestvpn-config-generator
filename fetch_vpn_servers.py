import requests
import json
import argparse
from bs4 import BeautifulSoup

url = 'https://support.fastestvpn.com/wp-admin/admin-ajax.php'
referer_url = 'https://support.fastestvpn.com/vpn-servers/'

def fetch_vpn_servers(protocol='udp'):
    # Validate protocol parameter
    allowed_protocols = ['tcp', 'udp', 'ikev2']
    if protocol not in allowed_protocols:
        raise ValueError(f"Invalid protocol '{protocol}'. Must be one of: {', '.join(allowed_protocols)}")

    session = requests.Session()

    # Visit the referer to obtain necessary cookies
    session.get(referer_url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
        'Priority': 'u=0',
    }, timeout=15)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://support.fastestvpn.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://support.fastestvpn.com/vpn-servers/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'Priority': 'u=0',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }

    data = {
        'action': 'vpn_servers',
        'protocol': protocol
    }

    response = session.post(url, headers=headers, data=data, timeout=15)
    response.raise_for_status()  # Raises HTTPError for bad status codes

    # Use response.text which handles decoding automatically
    data = response.text

    try:
        soup = BeautifulSoup(data, 'html.parser')
        rows = soup.find_all('tr')

        servers = []
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 3:
                server = {
                    'country': cells[0].get_text(strip=True),
                    'city': cells[1].get_text(strip=True),
                    'hostname': cells[2].get_text(strip=True)
                }
                servers.append(server)
        return servers
    except Exception as e:
        raise ValueError(f"Error parsing content: {e}\nRaw response data:\n{data}")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch FastestVPN server list')
    parser.add_argument(
        'protocol',
        nargs='?',
        type=str,
        default='udp',
        choices=['tcp', 'udp', 'ikev2'],
        help='VPN protocol to fetch servers for (default: udp)'
    )

    args = parser.parse_args()

    try:
        servers = fetch_vpn_servers(protocol=args.protocol)
        print(json.dumps(servers, indent=2))
        print(f"Total servers fetched: {len(servers)}")
    except ValueError as e:
        print(e)