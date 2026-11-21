"""Unit tests for the FastestVPN Android app API module."""
import json
from pathlib import Path

import pytest

from fetch_app_servers import parse_servers

FIXTURE_PATH = Path(__file__).parent / 'fixtures' / 'servers_response.json'


@pytest.fixture(scope='module')
def payload():
    return json.loads(FIXTURE_PATH.read_text())


class TestParseServers:
    """Test suite for parse_servers function."""

    def test_should_keep_only_enabled_wireguard_rows(self, payload):
        """Should keep only enabled WireGuard rows."""
        # Given: a live-shaped API payload with every protocol and enable flag
        # When: parsing the payload
        servers = parse_servers(payload)

        # Then: only enabled WireGuard rows should remain
        assert len(servers) == 61

    def test_should_exclude_disabled_wireguard_rows(self, payload):
        """Should exclude disabled WireGuard rows."""
        # Given: a payload containing a WireGuard row with enable == 0
        # When: parsing the payload
        hostnames = {server['hostname'] for server in parse_servers(payload)}

        # Then: the disabled server should be absent
        assert 'ch-02.jumptoserver.com' not in hostnames

    def test_should_exclude_non_wireguard_protocols(self, payload):
        """Should exclude non WireGuard protocols."""
        # Given: a payload containing UDP, TCP, IKEv2 and OCP rows
        # When: parsing the payload
        hostnames = {server['hostname'] for server in parse_servers(payload)}

        # Then: hostnames only used by non-WireGuard protocols should be absent
        assert 'us-ny.jumptoserver.com' not in hostnames
        assert 'mx2.jumptoserver.com' not in hostnames

    def test_should_keep_repeated_entries_across_groups(self, payload):
        """Should keep repeated entries across groups."""
        # Given: server id 1655, listed in both the Servers and P2P groups
        # When: parsing the payload
        entries = [server for server in parse_servers(payload) if server['id'] == 1655]

        # Then: both group rows should be kept (no deduplication)
        assert len(entries) == 2
        assert {entry['group'] for entry in entries} == {'Servers', 'P2P'}

    def test_should_keep_distinct_entries_sharing_a_hostname(self, payload):
        """Should keep distinct entries sharing a hostname."""
        # Given: Lisbon and Portugal P2P, which share pt.jumptoserver.com
        # When: parsing the payload
        shared = [
            server for server in parse_servers(payload)
            if server['hostname'] == 'pt.jumptoserver.com'
        ]

        # Then: every listed entry should survive
        assert len(shared) == 3
        assert {server['name'] for server in shared} == {'Lisbon', 'Portugal P2P'}

    def test_should_normalize_row_fields(self, payload):
        """Should normalize row fields."""
        # Given: the Zurich 1 entry in the main Servers group
        # When: parsing the payload
        server = next(
            server for server in parse_servers(payload)
            if server['hostname'] == 'ch-01.jumptoserver.com'
            and server['group'] == 'Servers'
        )

        # Then: the row should expose the normalized field set
        assert set(server) == {
            'id', 'group', 'country', 'city',
            'name', 'server_name', 'hostname', 'port',
        }
        assert server['country'] == 'Switzerland'
        assert server['server_name'] == 'Zurich 1'

    def test_should_use_app_wireguard_port_not_api_row_port(self, payload):
        """Should use app WireGuard port not API row port."""
        # Given: fixture rows that carry the OpenVPN port 4443
        # When: parsing the payload
        servers = parse_servers(payload)

        # Then: every entry should use the app's WireGuard port instead
        assert {server['port'] for server in servers} == {51820}

    def test_should_return_empty_list_when_payload_has_no_data(self):
        """Should return empty list when payload has no data."""
        # Given: payloads without a data array
        # When: parsing the payloads
        # Then: the result should be empty
        assert parse_servers({}) == []
        assert parse_servers({'data': []}) == []
