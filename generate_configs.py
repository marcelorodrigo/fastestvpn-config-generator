from collections import Counter
from pathlib import Path

from fetch_app_servers import fetch_wireguard_servers
from utils.filename_utils import assign_unique_filenames
from utils.config_utils import generate_config


def confirm_cleanup(output_dir):
    """Ask before deleting previous configs. Returns False when the user declines."""
    existing_files = [path for path in output_dir.iterdir() if path.is_file()]
    if not existing_files:
        return True

    print(f"'{output_dir}/' contains {len(existing_files)} file(s) from a previous run.")

    try:
        answer = input("Delete them and continue? [y/N]: ").strip().lower()
    except EOFError:
        answer = ''

    if answer not in ('y', 'yes'):
        print("Aborted: no files were deleted.")
        return False

    for path in existing_files:
        path.unlink()
    print(f"Deleted {len(existing_files)} file(s) from '{output_dir}/'")
    return True


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

    # Fetch the WireGuard entries from the same API the Android app uses
    print("Fetching WireGuard servers from the FastestVPN app API...")
    try:
        servers = fetch_wireguard_servers()
        print(f"Found {len(servers)} server entrie(s)")
    except Exception as e:
        print(f"Error fetching servers: {e}")
        return

    for group, count in Counter(server['group'] for server in servers).items():
        print(f"  {group}: {count}")

    # Assign one app-style filename per entry; repeated entries share a file
    assignments = assign_unique_filenames(servers)
    distinct_files = len({filename for _, filename in assignments})
    print(
        f"{len(assignments)} server entries to write "
        f"({distinct_files} distinct files)"
    )

    if not confirm_cleanup(output_dir):
        return

    # Generate config files
    generated_count = 0

    for server, filename in assignments:
        try:
            # Generate the configuration content
            config_content = generate_config(template_content, server)

            # Write the config file
            output_path = output_dir / filename
            output_path.write_text(config_content)

            label = server['server_name'] or server['name'] or 'N/A'
            city = server['city'] or 'N/A'
            print(
                f"Generated: {filename} ({server['group']} - "
                f"{server['country']} / {city} [{label}] - "
                f"{server['hostname']}:{server['port']})"
            )
            generated_count += 1

        except Exception as e:
            print(f"Error generating config for {server.get('hostname', 'unknown')}: {e}")

    print(
        f"\nSuccessfully generated {generated_count} configuration entries "
        f"({distinct_files} files) in '{output_dir}' directory"
    )


if __name__ == "__main__":
    main()
