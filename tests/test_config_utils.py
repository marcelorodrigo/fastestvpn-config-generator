"""Unit tests for config_utils module."""
import pytest
from utils.config_utils import generate_config


class TestGenerateConfig:
    """Test suite for generate_config function."""

    @pytest.fixture
    def template_content(self):
        """Provide a sample WireGuard configuration template."""
        return """[Interface]
PrivateKey = your-private-key
Address = 172.16.2254.254/32
DNS = 10.8.8.8

[Peer]
PublicKey = your-public-key
AllowedIPs = 0.0.0.0/0
Endpoint = ca-01.jumptoserver.com:51820"""

    @pytest.fixture
    def server_us(self):
        """Provide a US server dictionary."""
        return {
            'hostname': 'us-01.jumptoserver.com',
            'country': 'United States',
            'protocol': 'WireGuard'
        }

    @pytest.fixture
    def server_uk(self):
        """Provide a UK server dictionary."""
        return {
            'hostname': 'uk-london-01.jumptoserver.com',
            'country': 'United Kingdom',
            'protocol': 'WireGuard'
        }

    def test_should_replace_endpoint_hostname_when_server_provided(
        self, template_content, server_us
    ):
        """Should replace endpoint hostname when server is provided."""
        # Given: a template with a default endpoint
        # When: generating config with a US server
        result = generate_config(template_content, server_us)

        # Then: the endpoint should be replaced with the new hostname
        assert 'Endpoint = us-01.jumptoserver.com:51820' in result
        assert 'Endpoint = ca-01.jumptoserver.com:51820' not in result

    def test_should_preserve_port_51820_when_generating_config(
        self, template_content, server_us
    ):
        """Should preserve port 51820 when generating config."""
        # Given: a template with port 51820
        # When: generating config
        result = generate_config(template_content, server_us)

        # Then: the port should remain 51820
        assert ':51820' in result

    def test_should_preserve_interface_section_when_generating_config(
        self, template_content, server_uk
    ):
        """Should preserve interface section when generating config."""
        # Given: a template with Interface section
        # When: generating config
        result = generate_config(template_content, server_uk)

        # Then: all Interface fields should be preserved
        assert '[Interface]' in result
        assert 'PrivateKey = your-private-key' in result
        assert 'Address = 172.16.2254.254/32' in result
        assert 'DNS = 10.8.8.8' in result

    def test_should_preserve_peer_section_when_generating_config(
        self, template_content, server_uk
    ):
        """Should preserve peer section when generating config."""
        # Given: a template with Peer section
        # When: generating config
        result = generate_config(template_content, server_uk)

        # Then: all Peer fields except Endpoint should be preserved
        assert '[Peer]' in result
        assert 'PublicKey = your-public-key' in result
        assert 'AllowedIPs = 0.0.0.0/0' in result

    def test_should_handle_hostname_with_hyphens_when_generating_config(
        self, template_content, server_uk
    ):
        """Should handle hostname with hyphens when generating config."""
        # Given: a server with hyphens in hostname
        # When: generating config
        result = generate_config(template_content, server_uk)

        # Then: the full hostname with hyphens should be preserved
        assert 'Endpoint = uk-london-01.jumptoserver.com:51820' in result

    @pytest.mark.parametrize("hostname,expected_endpoint", [
        ('us-01.jumptoserver.com', 'Endpoint = us-01.jumptoserver.com:51820'),
        ('uk-london-01.jumptoserver.com', 'Endpoint = uk-london-01.jumptoserver.com:51820'),
        ('de-frankfurt-01.example.com', 'Endpoint = de-frankfurt-01.example.com:51820'),
        ('jp-tokyo-02.vpn.net', 'Endpoint = jp-tokyo-02.vpn.net:51820'),
        ('au-sydney.server.io', 'Endpoint = au-sydney.server.io:51820'),
    ])
    def test_should_generate_correct_endpoint_for_various_hostnames(
        self, template_content, hostname, expected_endpoint
    ):
        """Should generate correct endpoint for various hostnames."""
        # Given: a server with specific hostname
        server = {'hostname': hostname}

        # When: generating config
        result = generate_config(template_content, server)

        # Then: the correct endpoint should be in the result
        assert expected_endpoint in result

    def test_should_replace_only_endpoint_line_when_multiple_equals_signs_present(
        self, server_us
    ):
        """Should replace only endpoint line when multiple equals signs present."""
        # Given: a template with multiple lines containing '='
        template = """[Interface]
PrivateKey = some-key-with=equals=signs
Address = 172.16.2254.254/32
DNS = 10.8.8.8

[Peer]
PublicKey = another-key=with=equals
AllowedIPs = 0.0.0.0/0
Endpoint = old-server.com:51820"""

        # When: generating config
        result = generate_config(template, server_us)

        # Then: only the Endpoint line should be modified
        assert 'PrivateKey = some-key-with=equals=signs' in result
        assert 'PublicKey = another-key=with=equals' in result
        assert 'Endpoint = us-01.jumptoserver.com:51820' in result
        assert 'Endpoint = old-server.com:51820' not in result

    def test_should_return_string_when_generating_config(
        self, template_content, server_us
    ):
        """Should return string when generating config."""
        # Given: a valid template and server
        # When: generating config
        result = generate_config(template_content, server_us)

        # Then: result should be a string
        assert isinstance(result, str)

    def test_should_maintain_line_structure_when_generating_config(
        self, template_content, server_us
    ):
        """Should maintain line structure when generating config."""
        # Given: a template with specific line count
        original_line_count = len(template_content.split('\n'))

        # When: generating config
        result = generate_config(template_content, server_us)
        result_line_count = len(result.split('\n'))

        # Then: line count should remain the same
        assert result_line_count == original_line_count
# Test package

