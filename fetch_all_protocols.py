import json
from fetch_vpn_servers import fetch_vpn_servers


def fetch_all_protocols():
    """
    Fetch VPN servers for all available protocols (tcp, udp, ikev2)
    and return a deduplicated list based on hostname.
    """
    protocols = ['tcp', 'udp', 'ikev2']
    all_servers = []

    # Fetch servers for each protocol
    for protocol in protocols:
        print(f"Fetching servers for protocol: {protocol}")
        try:
            servers = fetch_vpn_servers(protocol)
            print(f"  Found {len(servers)} servers")
            all_servers.extend(servers)
        except Exception as e:
            print(f"  Error fetching {protocol} servers: {e}")

    # Remove duplicates based on hostname
    seen_hostnames = set()
    unique_servers = []

    for server in all_servers:
        hostname = server['hostname']
        if hostname not in seen_hostnames:
            seen_hostnames.add(hostname)
            unique_servers.append(server)

    return unique_servers


if __name__ == "__main__":
    try:
        print("Fetching VPN servers for all protocols...\n")
        servers = fetch_all_protocols()

        print(f"\nTotal unique servers: {len(servers)}")
        print("\nUnique servers list:")
        print(json.dumps(servers, indent=2))

        # Optionally save to file
        output_file = 'all_unique_servers.json'
        with open(output_file, 'w') as f:
            json.dump(servers, f, indent=2)
        print(f"\nResults saved to {output_file}")

    except Exception as e:
        print(f"Error: {e}")

