"""Unit tests for filename_utils module."""
import pytest
from utils.filename_utils import sanitize_filename, generate_filename


class TestSanitizeFilename:
    """Test suite for sanitize_filename function."""

    def test_should_convert_to_lowercase_when_uppercase_provided(self):
        """Should convert to lowercase when uppercase provided."""
        # Given: text with uppercase letters
        text = "United States"

        # When: sanitizing filename
        result = sanitize_filename(text)

        # Then: result should be lowercase
        assert result == "united-states"

    def test_should_replace_spaces_with_hyphens_when_spaces_present(self):
        """Should replace spaces with hyphens when spaces present."""
        # Given: text with spaces
        text = "New York City"

        # When: sanitizing filename
        result = sanitize_filename(text)

        # Then: spaces should be replaced with hyphens
        assert result == "new-york-city"

    def test_should_remove_special_characters_when_present(self):
        """Should remove special characters when present."""
        # Given: text with special characters
        text = "So Paulo!@#$%"

        # When: sanitizing filename
        result = sanitize_filename(text)

        # Then: special characters and unicode should be removed
        assert result == "so-paulo"

    def test_should_replace_underscores_with_hyphens_when_underscores_present(self):
        """Should replace underscores with hyphens when underscores present."""
        # Given: text with underscores
        text = "test_file_name"

        # When: sanitizing filename
        result = sanitize_filename(text)

        # Then: underscores should be replaced with hyphens
        assert result == "test-file-name"

    def test_should_collapse_multiple_spaces_to_single_hyphen_when_multiple_spaces(self):
        """Should collapse multiple spaces to single hyphen when multiple spaces."""
        # Given: text with multiple consecutive spaces
        text = "New    York"

        # When: sanitizing filename
        result = sanitize_filename(text)

        # Then: multiple spaces should become single hyphen
        assert result == "new-york"

    def test_should_strip_leading_trailing_hyphens_when_present(self):
        """Should strip leading trailing hyphens when present."""
        # Given: text that would result in leading/trailing hyphens
        text = " -test- "

        # When: sanitizing filename
        result = sanitize_filename(text)

        # Then: leading and trailing hyphens should be removed
        assert result == "test"

    def test_should_handle_empty_string_when_provided(self):
        """Should handle empty string when provided."""
        # Given: empty string
        text = ""

        # When: sanitizing filename
        result = sanitize_filename(text)

        # Then: result should be empty
        assert result == ""

    @pytest.mark.parametrize("text,expected", [
        ("United Kingdom", "united-kingdom"),
        ("GERMANY", "germany"),
        ("So Paulo", "so-paulo"),
        ("New-York", "new-york"),
        ("test_123", "test-123"),
        ("Los Angeles!!!", "los-angeles"),
        ("   Paris   ", "paris"),
        ("Hong Kong (SAR)", "hong-kong-sar"),
    ])
    def test_should_sanitize_various_inputs_correctly(self, text, expected):
        """Should sanitize various inputs correctly."""
        # Given: various text inputs
        # When: sanitizing filename
        result = sanitize_filename(text)

        # Then: result should match expected
        assert result == expected


class TestGenerateFilename:
    """Test suite for generate_filename function."""

    def test_should_extract_prefix_from_simple_hostname(self):
        """Should extract prefix from simple hostname."""
        # Given: server with simple hostname
        server = {
            'country': 'Spain',
            'city': 'Barcelona',
            'hostname': 'es-01.jumptoserver.com'
        }

        # When: generating filename
        result = generate_filename(server)

        # Then: filename should use hostname prefix
        assert result == "es-01.conf"

    def test_should_extract_prefix_from_complex_hostname(self):
        """Should extract prefix from complex hostname."""
        # Given: server with complex hostname
        server = {
            'country': 'United States',
            'city': 'New York',
            'hostname': 'us-ny-05.jumptoserver.com'
        }

        # When: generating filename
        result = generate_filename(server)

        # Then: filename should use full prefix
        assert result == "us-ny-05.conf"

    def test_should_handle_streaming_server_hostname(self):
        """Should handle streaming server hostname."""
        # Given: server with streaming in hostname
        server = {
            'country': 'United Kingdom',
            'city': 'London',
            'hostname': 'uk-london-stream.jumptoserver.com'
        }

        # When: generating filename
        result = generate_filename(server)

        # Then: filename should preserve stream in prefix
        assert result == "uk-london-stream.conf"

    def test_should_handle_p2p_server_hostname(self):
        """Should handle P2P server hostname."""
        # Given: server with P2P in hostname
        server = {
            'country': 'Netherlands',
            'city': 'Amsterdam',
            'hostname': 'nl-amsterdam-01-p2p.jumptoserver.com'
        }

        # When: generating filename
        result = generate_filename(server)

        # Then: filename should preserve p2p in prefix
        assert result == "nl-amsterdam-01-p2p.conf"

    def test_should_handle_double_vpn_hostname(self):
        """Should handle double VPN hostname."""
        # Given: server with dvpn in hostname
        server = {
            'country': 'United States',
            'city': 'New York',
            'hostname': 'uk-dvpn.jumptoserver.com'
        }

        # When: generating filename
        result = generate_filename(server)

        # Then: filename should preserve dvpn in prefix
        assert result == "uk-dvpn.conf"

    def test_should_handle_empty_city(self):
        """Should handle empty city."""
        # Given: server with empty city
        server = {
            'country': 'Canada',
            'city': '',
            'hostname': 'ca-01.jumptoserver.com'
        }

        # When: generating filename
        result = generate_filename(server)

        # Then: filename should still use hostname prefix
        assert result == "ca-01.conf"

    def test_should_prepend_country_for_dbl_prefix(self):
        """Should prepend sanitized country for -dbl prefix in hostname."""
        # Given: server with -dbl in hostname
        server = {
            'country': 'Brazil',
            'city': 'Campinas',
            'hostname': 'br-cf-dbl.jumptoserver.com'
        }

        # When: generating filename
        result = generate_filename(server)

        # Then: filename should prepend sanitized country
        assert result == "brazil-br-cf-dbl.conf"

    @pytest.mark.parametrize("country,hostname,expected", [
        ("Brazil", "br-cf-dbl.jumptoserver.com", "brazil-br-cf-dbl.conf"),
        ("United States", "us-dbl.jumptoserver.com", "united-states-us-dbl.conf"),
        ("Germany", "de-berlin-dbl.jumptoserver.com", "germany-de-berlin-dbl.conf"),
        ("South Korea", "kr-seoul-dbl.jumptoserver.com", "south-korea-kr-seoul-dbl.conf"),
        ("France!@#", "fr-paris-dbl.jumptoserver.com", "france-fr-paris-dbl.conf"),
    ])
    def test_should_generate_correct_filename_for_various_dbl_hostnames(self, country, hostname, expected):
        """Should generate correct filename for various -dbl hostnames."""
        # Given: server with specific hostname
        server = {
            'country': country,
            'city': 'Test City',
            'hostname': hostname
        }

        # When: generating filename
        result = generate_filename(server)

        # Then: result should match expected filename
        assert result == expected

    def test_should_return_conf_extension(self):
        """Should return conf extension."""
        # Given: any valid server
        server = {
            'country': 'Test',
            'city': 'City',
            'hostname': 'test-01.jumptoserver.com'
        }

        # When: generating filename
        result = generate_filename(server)

        # Then: filename should end with .conf
        assert result.endswith('.conf')
