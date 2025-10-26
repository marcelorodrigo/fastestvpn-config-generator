"""Unit tests for hostname_utils module."""
import pytest
from utils.hostname_utils import extract_number_from_hostname, extract_double_vpn_country


class TestExtractNumberFromHostname:
    """Test suite for extract_number_from_hostname function."""

    def test_should_extract_two_digit_number_when_present(self):
        """Should extract two digit number when present."""
        # Given: hostname with two-digit number
        hostname = 'ca-01.jumptoserver.com'

        # When: extracting number
        result = extract_number_from_hostname(hostname)

        # Then: should return the number
        assert result == '01'

    def test_should_extract_first_number_when_multiple_numbers_present(self):
        """Should extract first number when multiple numbers present."""
        # Given: hostname with multiple numbers
        hostname = 'us-ny-05-stream-02.jumptoserver.com'

        # When: extracting number
        result = extract_number_from_hostname(hostname)

        # Then: should return the first number after hyphen
        assert result == '05'

    def test_should_return_00_when_no_number_present(self):
        """Should return 00 when no number present."""
        # Given: hostname without numbers
        hostname = 'us-dvpn.jumptoserver.com'

        # When: extracting number
        result = extract_number_from_hostname(hostname)

        # Then: should return default '00'
        assert result == '00'

    def test_should_extract_single_digit_number_when_present(self):
        """Should extract single digit number when present."""
        # Given: hostname with single-digit number
        hostname = 'uk-london-5.jumptoserver.com'

        # When: extracting number
        result = extract_number_from_hostname(hostname)

        # Then: should return the single digit
        assert result == '5'

    def test_should_extract_three_digit_number_when_present(self):
        """Should extract three digit number when present."""
        # Given: hostname with three-digit number
        hostname = 'de-frankfurt-123.jumptoserver.com'

        # When: extracting number
        result = extract_number_from_hostname(hostname)

        # Then: should return the three-digit number
        assert result == '123'

    def test_should_handle_hostname_with_leading_number(self):
        """Should handle hostname with leading number."""
        # Given: hostname starting with country code and number
        hostname = 'se-99.jumptoserver.com'

        # When: extracting number
        result = extract_number_from_hostname(hostname)

        # Then: should return the number
        assert result == '99'

    def test_should_return_00_when_empty_hostname(self):
        """Should return 00 when empty hostname."""
        # Given: empty hostname
        hostname = ''

        # When: extracting number
        result = extract_number_from_hostname(hostname)

        # Then: should return default '00'
        assert result == '00'

    def test_should_return_00_when_hostname_without_hyphen(self):
        """Should return 00 when hostname without hyphen."""
        # Given: hostname without hyphen before number
        hostname = 'server123.jumptoserver.com'

        # When: extracting number
        result = extract_number_from_hostname(hostname)

        # Then: should return default '00'
        assert result == '00'

    @pytest.mark.parametrize("hostname,expected", [
        ('us-01.jumptoserver.com', '01'),
        ('uk-london-05.jumptoserver.com', '05'),
        ('de-frankfurt-123.example.com', '123'),
        ('jp-tokyo-7.vpn.net', '7'),
        ('au-sydney-99.server.io', '99'),
        ('fr-paris-001.jumptoserver.com', '001'),
        ('ca-tor.jumptoserver.com', '00'),
        ('nl-dvpn.jumptoserver.com', '00'),
        ('', '00'),
        ('server.com', '00'),
    ])
    def test_should_extract_correct_number_for_various_hostnames(self, hostname, expected):
        """Should extract correct number for various hostnames."""
        # Given: various hostname formats
        # When: extracting number
        result = extract_number_from_hostname(hostname)

        # Then: result should match expected number
        assert result == expected

    def test_should_return_string_type_when_extracting_number(self):
        """Should return string type when extracting number."""
        # Given: any valid hostname
        hostname = 'us-05.jumptoserver.com'

        # When: extracting number
        result = extract_number_from_hostname(hostname)

        # Then: result should be string type
        assert isinstance(result, str)


class TestExtractDoubleVpnCountry:
    """Test suite for extract_double_vpn_country function."""

    def test_should_extract_country_code_when_dvpn_pattern_present(self):
        """Should extract country code when dvpn pattern present."""
        # Given: hostname with dvpn pattern
        hostname = 'us-dvpn.jumptoserver.com'

        # When: extracting double VPN country
        result = extract_double_vpn_country(hostname)

        # Then: should return the country code
        assert result == 'us'

    def test_should_extract_uk_country_code_when_uk_dvpn(self):
        """Should extract uk country code when uk dvpn."""
        # Given: UK hostname with dvpn pattern
        hostname = 'uk-dvpn.jumptoserver.com'

        # When: extracting double VPN country
        result = extract_double_vpn_country(hostname)

        # Then: should return 'uk'
        assert result == 'uk'

    def test_should_extract_de_country_code_when_de_dvpn(self):
        """Should extract de country code when de dvpn."""
        # Given: German hostname with dvpn pattern
        hostname = 'de-dvpn.jumptoserver.com'

        # When: extracting double VPN country
        result = extract_double_vpn_country(hostname)

        # Then: should return 'de'
        assert result == 'de'

    def test_should_return_unknown_when_no_dvpn_pattern(self):
        """Should return unknown when no dvpn pattern."""
        # Given: hostname without dvpn pattern
        hostname = 'us-ny-01.jumptoserver.com'

        # When: extracting double VPN country
        result = extract_double_vpn_country(hostname)

        # Then: should return 'unknown'
        assert result == 'unknown'

    def test_should_return_unknown_when_dvpn_without_country_code(self):
        """Should return unknown when dvpn without country code."""
        # Given: hostname with dvpn but no proper country code
        hostname = 'dvpn.jumptoserver.com'

        # When: extracting double VPN country
        result = extract_double_vpn_country(hostname)

        # Then: should return 'unknown'
        assert result == 'unknown'

    def test_should_return_unknown_when_country_code_too_long(self):
        """Should return unknown when country code too long."""
        # Given: hostname with three-letter code before dvpn
        hostname = 'usa-dvpn.jumptoserver.com'

        # When: extracting double VPN country
        result = extract_double_vpn_country(hostname)

        # Then: should return 'unknown' (only accepts 2 letters)
        assert result == 'unknown'

    def test_should_return_unknown_when_uppercase_country_code(self):
        """Should return unknown when uppercase country code."""
        # Given: hostname with uppercase country code
        hostname = 'US-dvpn.jumptoserver.com'

        # When: extracting double VPN country
        result = extract_double_vpn_country(hostname)

        # Then: should return 'unknown' (only accepts lowercase)
        assert result == 'unknown'

    def test_should_return_unknown_when_empty_hostname(self):
        """Should return unknown when empty hostname."""
        # Given: empty hostname
        hostname = ''

        # When: extracting double VPN country
        result = extract_double_vpn_country(hostname)

        # Then: should return 'unknown'
        assert result == 'unknown'

    def test_should_match_only_at_start_when_dvpn_in_middle(self):
        """Should match only at start when dvpn in middle."""
        # Given: hostname with dvpn not at start
        hostname = 'server.us-dvpn.jumptoserver.com'

        # When: extracting double VPN country
        result = extract_double_vpn_country(hostname)

        # Then: should return 'unknown' (pattern must be at start)
        assert result == 'unknown'

    def test_should_require_dot_after_dvpn_when_checking_pattern(self):
        """Should require dot after dvpn when checking pattern."""
        # Given: hostname with dvpn but no dot after
        hostname = 'us-dvpn-server.com'

        # When: extracting double VPN country
        result = extract_double_vpn_country(hostname)

        # Then: should return 'unknown' (requires dot after dvpn)
        assert result == 'unknown'

    @pytest.mark.parametrize("hostname,expected", [
        ('us-dvpn.jumptoserver.com', 'us'),
        ('uk-dvpn.jumptoserver.com', 'uk'),
        ('de-dvpn.jumptoserver.com', 'de'),
        ('fr-dvpn.example.com', 'fr'),
        ('nl-dvpn.vpn.net', 'nl'),
        ('ca-dvpn.server.io', 'ca'),
        ('us-ny-01.jumptoserver.com', 'unknown'),
        ('us-stream.jumptoserver.com', 'unknown'),
        ('dvpn.jumptoserver.com', 'unknown'),
        ('usa-dvpn.jumptoserver.com', 'unknown'),
        ('US-dvpn.jumptoserver.com', 'unknown'),
        ('', 'unknown'),
    ])
    def test_should_extract_correct_country_for_various_hostnames(self, hostname, expected):
        """Should extract correct country for various hostnames."""
        # Given: various hostname formats
        # When: extracting double VPN country
        result = extract_double_vpn_country(hostname)

        # Then: result should match expected country code
        assert result == expected

    def test_should_return_string_type_when_extracting_country(self):
        """Should return string type when extracting country."""
        # Given: any valid hostname
        hostname = 'us-dvpn.jumptoserver.com'

        # When: extracting double VPN country
        result = extract_double_vpn_country(hostname)

        # Then: result should be string type
        assert isinstance(result, str)

    def test_should_return_two_character_code_when_valid_pattern(self):
        """Should return two character code when valid pattern."""
        # Given: valid dvpn hostname
        hostname = 'jp-dvpn.jumptoserver.com'

        # When: extracting double VPN country
        result = extract_double_vpn_country(hostname)

        # Then: result should be exactly 2 characters
        assert len(result) == 2
        assert result == 'jp'

