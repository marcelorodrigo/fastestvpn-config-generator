import re
from collections import defaultdict

from utils.hostname_utils import extract_prefix

CONFIG_EXTENSION = '.conf'

#: The API group holding the regular country/city server listing.
MAIN_GROUP = 'Servers'


def sanitize_filename(text):
    """Sanitize text to be used as a filename."""
    # Remove or replace invalid filename characters
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text.strip('-')


def _main_group_label(server):
    """Return the app entry label for a regular server row.

    The app lists entries under their country with labels such as
    'Zurich 1' or 'Lisbon', falling back to the city, then the country
    name when those are missing.
    """
    label = sanitize_filename(server.get('server_name') or '')
    if label:
        return label
    label = sanitize_filename(server.get('city') or '')
    if label:
        return label
    return sanitize_filename(server.get('name') or '')


def _special_group_label(server):
    """Return the app entry label for a streaming, P2P or D-VPN row.

    Those labels are already fully qualified, e.g. 'Portugal P2P' or
    'France Via UK'.
    """
    return (
        sanitize_filename(server.get('name') or '')
        or sanitize_filename(server.get('server_name') or '')
    )


def generate_filename(server):
    """Generate a descriptive base filename mirroring the app listing.

    Regular Servers rows become 'country-label' (e.g. 'switzerland-zurich-1'),
    with a redundant country prefix stripped from the label so the same entry
    keeps one predictable name across groups. Streaming, P2P and D-VPN rows
    use their own label (e.g. 'portugal-p2p'). The hostname prefix is the last
    resort when no label is available.
    """
    country = sanitize_filename(server.get('country') or '')
    group = server.get('group') or MAIN_GROUP

    if group == MAIN_GROUP:
        label = _main_group_label(server)
        if country and label and label.startswith(f"{country}-"):
            return f"{label}{CONFIG_EXTENSION}"
        stem = '-'.join(part for part in (country, label) if part)
        if stem:
            return f"{stem}{CONFIG_EXTENSION}"
    else:
        label = _special_group_label(server)
        if label:
            return f"{label}{CONFIG_EXTENSION}"

    return f"{extract_prefix(server['hostname'])}{CONFIG_EXTENSION}"


def _entry_id(server):
    """Return the app's identity for a server entry: its API row id."""
    return server.get('id')


def assign_unique_filenames(servers):
    """Assign a filename to every app entry, without deduplicating entries.

    Every row gets an assignment. Two rows are the same app entry only when
    they carry the same API row id, so a row repeated across groups keeps its
    filename and lands on the same file with identical content. Distinct
    entries that share a hostname keep their own file, exactly like the app
    lists them. When distinct entries collide on a filename, the hostname
    prefix disambiguates them; if that still collides, the run fails loudly.

    Returns a list of (server, filename) pairs.
    """
    assignments = [(server, generate_filename(server)) for server in servers]

    entry_ids_by_filename = defaultdict(set)
    for server, filename in assignments:
        entry_ids_by_filename[filename].add(_entry_id(server))

    resolved = []
    for server, filename in assignments:
        if len(entry_ids_by_filename[filename]) > 1:
            stem = filename.removesuffix(CONFIG_EXTENSION)
            prefix = sanitize_filename(extract_prefix(server['hostname']))
            filename = f"{stem}-{prefix}{CONFIG_EXTENSION}"
        resolved.append((server, filename))

    entry_ids_after = defaultdict(set)
    for server, filename in resolved:
        entry_ids_after[filename].add(_entry_id(server))

    collisions = sorted(
        filename
        for filename, entry_ids in entry_ids_after.items()
        if len(entry_ids) > 1
    )
    if collisions:
        raise ValueError(
            f"Cannot generate unique filenames for: {', '.join(collisions)}"
        )

    return resolved
