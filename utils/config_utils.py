import re

def generate_config(template_content, server):
    """Generate a config file by replacing the Endpoint line."""
    # Replace the Endpoint line with the new hostname
    # The endpoint format is: hostname:51820
    new_endpoint = f"Endpoint = {server['hostname']}:51820"

    # Replace the existing Endpoint line
    config = re.sub(
        r'Endpoint = .*',
        new_endpoint,
        template_content
    )

    return config
