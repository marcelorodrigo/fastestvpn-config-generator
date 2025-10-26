import re

def sanitize_filename(text):
    """Sanitize text to be used as a filename."""
    # Remove or replace invalid filename characters
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text.strip('-')

def generate_filename(server):
    """Generate filename based on hostname prefix.

    Extracts the prefix from hostname (e.g., 'br-cf.jumptoserver.com' -> 'br-cf.conf').
    This ensures compatibility with file systems that have character limits.
    """
    hostname = server['hostname']
    # Extract prefix before .jumptoserver.com
    name = hostname.split('.')[0]

    if "-dbl" in name:
        name = sanitize_filename(server['country']) + "-" + name

    return f"{name}.conf"
