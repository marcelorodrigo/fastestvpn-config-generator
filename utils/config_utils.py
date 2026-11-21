import re


def generate_config(template_content, server):
    """Generate a config file by replacing the Endpoint line.

    Everything else in the template is copied verbatim, so the private key
    never passes through application logic.
    """
    # The endpoint format is: hostname:port, with the port coming from the
    # server row (the app API lists WireGuard on port 4443).
    new_endpoint = f"Endpoint = {server['hostname']}:{server['port']}"

    # Replace the existing Endpoint line
    config = re.sub(
        r'Endpoint = .*',
        new_endpoint,
        template_content
    )

    return config
