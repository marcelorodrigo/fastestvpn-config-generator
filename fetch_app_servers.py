"""Fetch the WireGuard server list from the FastestVPN Android app API."""
import json

import requests

API_URL = 'https://api.fastestvpn.com/v2/servers'


def parse_servers(payload):
    """Return the enabled WireGuard entries from an API response payload.

    Every row is kept, including the same entry repeated across groups and
    distinct entries that share a hostname, because that mirrors what the app
    shows to the user.
    """
    servers = []
    for group in payload.get('data', []):
        for row in group.get('servers', []):
            if row.get('protocol') != 'WG' or row.get('enable') != 1:
                continue
            servers.append({
                'id': row.get('id'),
                'group': group.get('name'),
                'country': row.get('country'),
                'city': row.get('city'),
                'name': row.get('name'),
                'server_name': row.get('server_name'),
                'hostname': row.get('dns'),
                'port': row.get('port'),
            })
    return servers


def fetch_wireguard_servers(url=API_URL):
    """Fetch and parse the enabled WireGuard entries from the app API."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return parse_servers(response.json())


if __name__ == '__main__':
    entries = fetch_wireguard_servers()
    print(json.dumps(entries, indent=2))
    print(f"Total WireGuard entries: {len(entries)}")
