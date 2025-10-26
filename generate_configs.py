from pathlib import Path
from fetch_vpn_servers import fetch_vpn_servers
from utils.filename_utils import generate_filename
from utils.config_utils import generate_config

def main():
    # Create output directory if it doesn't exist
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)

    # Read the template file
    template_path = Path('fastestvpn.conf')
    if not template_path.exists():
        print(f"Error: Template file '{template_path}' not found!")
        return

    template_content = template_path.read_text()

    # Fetch VPN servers
    print("Fetching VPN servers...")
    try:
        servers = fetch_vpn_servers()
        print(f"Found {len(servers)} servers")
    except Exception as e:
        print(f"Error fetching servers: {e}")
        return

    # Generate config files
    generated_count = 0
    filename_counter = {}  # Track duplicate filenames

    for server in servers:
        try:
            # Generate the configuration content
            config_content = generate_config(template_content, server)

            # Generate the base filename
            base_filename = generate_filename(server)

            # Handle duplicate filenames by adding a counter
            if base_filename in filename_counter:
                filename_counter[base_filename] += 1
                # Insert counter before .conf extension
                name_without_ext = base_filename[:-5]  # Remove .conf
                filename = f"{name_without_ext}-{filename_counter[base_filename]}.conf"
            else:
                filename_counter[base_filename] = 1
                filename = base_filename

            # Write the config file
            output_path = output_dir / filename
            output_path.write_text(config_content)

            print(f"Generated: {filename} ({server['country']} - {server['city'] or 'N/A'} - {server['hostname']})")
            generated_count += 1

        except Exception as e:
            print(f"Error generating config for {server.get('hostname', 'unknown')}: {e}")

    print(f"\nSuccessfully generated {generated_count} configuration files in '{output_dir}' directory")


if __name__ == "__main__":
    main()
