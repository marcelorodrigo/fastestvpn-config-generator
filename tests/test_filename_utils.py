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
        text = "São Paulo!@#$%"

        # When: sanitizing filename
        result = sanitize_filename(text)

        # Then: special characters and unicode should be removed
        assert result == "são-paulo"

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
        ("São Paulo", "são-paulo"),
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

        # Then: result should match expected output
        assert result == expected


class TestGenerateFilename:
    """Test suite for generate_filename function."""

    def test_should_generate_standard_filename_when_country_and_city_provided(self):
        """Should generate standard filename when country and city provided."""
        # Given: server with country and city
        server = {
            'country': 'United States',
            'city': 'New York',
            'hostname': 'us-ny-01.jumptoserver.com'
        }

        # When: generating filename
        result = generate_filename(server)

        # Then: filename should use country and city
        assert result == "united-states-new-york.conf"

    def test_should_use_hostname_number_when_city_is_empty(self):
        """Should use hostname number when city is empty."""
        # Given: server with empty city
        server = {
            'country': 'Canada',
            'city': '',
            'hostname': 'ca-01.jumptoserver.com'
        }

        # When: generating filename
        result = generate_filename(server)

        # Then: filename should use extracted number from hostname
        assert result == "canada-01.conf"

    def test_should_generate_streaming_filename_when_stream_in_hostname(self):
        """Should generate streaming filename when stream in hostname."""
        # Given: server with streaming hostname
        server = {
            'country': 'United States',
            'city': 'Los Angeles',
            'hostname': 'us-la-01-stream.jumptoserver.com'
        }

        # When: generating filename
        result = generate_filename(server)

        # Then: filename should include streaming suffix
        assert result == "united-states-los-angeles-streaming.conf"

    def test_should_generate_double_vpn_filename_when_dvpn_in_hostname(self):
        """Should generate double vpn filename when dvpn in hostname."""
        # Given: server with double VPN hostname
        server = {
            'country': 'United States',
            'city': 'New York',
            'hostname': 'uk-dvpn.jumptoserver.com'
        }

        # When: generating filename
        result = generate_filename(server)

        # Then: filename should include via country
        assert result == "united-states-new-york-via-uk.conf"

    def test_should_generate_p2p_filename_when_p2p_in_hostname(self):
        """Should generate p2p filename when p2p in hostname."""
        # Given: server with P2P hostname
        server = {
            'country': 'Netherlands',
            'city': 'Amsterdam',
            'hostname': 'nl-amsterdam-01-p2p.jumptoserver.com'
        }

        # When: generating filename
        result = generate_filename(server)

        # Then: filename should include p2p suffix
        assert result == "netherlands-amsterdam-p2p.conf"

    def test_should_sanitize_country_name_when_generating_filename(self):
        """Should sanitize country name when generating filename."""
        # Given: server with country containing special characters
        server = {
            'country': 'United Kingdom!!!',
            'city': 'London',
            'hostname': 'uk-london-01.jumptoserver.com'
        }

        # When: generating filename
        result = generate_filename(server)

        # Then: country should be sanitized
        assert result == "united-kingdom-london.conf"

    def test_should_sanitize_city_name_when_generating_filename(self):
        """Should sanitize city name when generating filename."""
        # Given: server with city containing special characters
        server = {
            'country': 'Germany',
            'city': 'Frankfurt am Main',
            'hostname': 'de-frankfurt-01.jumptoserver.com'
        }

        # When: generating filename
        result = generate_filename(server)

        # Then: city should be sanitized
        assert result == "germany-frankfurt-am-main.conf"

    def test_should_strip_city_whitespace_when_present(self):
        """Should strip city whitespace when present."""
        # Given: server with city having whitespace
        server = {
            'country': 'Japan',
            'city': '  Tokyo  ',
            'hostname': 'jp-tokyo-01.jumptoserver.com'
        }

        # When: generating filename
        result = generate_filename(server)

        # Then: whitespace should be stripped
        assert result == "japan-tokyo.conf"

    def test_should_prioritize_streaming_over_other_types_when_stream_present(self):
        """Should prioritize streaming over other types when stream present."""
        # Given: server with streaming in hostname
        server = {
            'country': 'United States',
            'city': 'Seattle',
            'hostname': 'us-seattle-01-stream-p2p.jumptoserver.com'
        }

        # When: generating filename
        result = generate_filename(server)

        # Then: streaming should take priority
        assert result == "united-states-seattle-streaming.conf"

    def test_should_handle_hostname_with_city_code_when_city_empty(self):
        """Should handle hostname with city code when city empty."""
        # Given: server with empty city and complex hostname
        server = {
            'country': 'Australia',
            'city': '',
            'hostname': 'au-sydney-05.jumptoserver.com'
        }

        # When: generating filename
        result = generate_filename(server)

        # Then: should extract first number from hostname
        assert result == "australia-05.conf"

    @pytest.mark.parametrize("server,expected", [
        (
            {'country': 'Canada', 'city': 'Toronto', 'hostname': 'ca-tor-01.jumptoserver.com'},
            'canada-toronto.conf'
        ),
        (
            {'country': 'France', 'city': 'Paris', 'hostname': 'fr-paris-01-stream.jumptoserver.com'},
            'france-paris-streaming.conf'
        ),
        (
            {'country': 'Italy', 'city': 'Rome', 'hostname': 'it-rome-01-p2p.jumptoserver.com'},
            'italy-rome-p2p.conf'
        ),
        (
            {'country': 'Spain', 'city': 'Madrid', 'hostname': 'de-dvpn.jumptoserver.com'},
            'spain-madrid-via-de.conf'
        ),
        (
            {'country': 'Sweden', 'city': '', 'hostname': 'se-99.jumptoserver.com'},
            'sweden-99.conf'
        ),
        (
            {'country': 'Switzerland', 'city': 'Zürich', 'hostname': 'ch-zurich-01.jumptoserver.com'},
            'switzerland-zürich.conf'
        ),
    ])
    def test_should_generate_correct_filename_for_various_servers(self, server, expected):
        """Should generate correct filename for various servers."""
        # Given: various server configurations
        # When: generating filename
        result = generate_filename(server)

        # Then: result should match expected filename
        assert result == expected

    def test_should_return_conf_extension_when_generating_filename(self):
        """Should return conf extension when generating filename."""
        # Given: any valid server
        server = {
            'country': 'Test',
            'city': 'City',
            'hostname': 'test-city-01.jumptoserver.com'
        }

        # When: generating filename
        result = generate_filename(server)

        # Then: filename should end with .conf
        assert result.endswith('.conf')

