import re


def generate_config(template_content, server):
    """Generate a config file by replacing the Endpoint line.

    Everything else in the template is copied verbatim, so the private key
    never passes through application logic.
    """
    # The endpoint format is: hostname:port, with the port coming from the
    # server row (fetch_app_servers normalizes WireGuard to UDP 51820, the
    # same port the app appends when it builds its tunnel).
    new_endpoint = f"Endpoint = {server['hostname']}:{server['port']}"

    # Replace the existing Endpoint line
    config = re.sub(
        r'Endpoint = .*',
        new_endpoint,
        template_content
    )

    return config
