"""Unit tests for filename_utils module."""
from itertools import count

import pytest
from utils.filename_utils import (
    sanitize_filename,
    generate_filename,
    assign_unique_filenames,
)

_ENTRY_IDS = count(1)


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

        # Then: underscores should become hyphens
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


def make_server(group, country, server_name, name=None, city=None,
                hostname='xx-01.jumptoserver.com', entry_id=None):
    """Build a normalized server row like fetch_app_servers produces.

    Each call gets a fresh API row id unless ``entry_id`` is given, which
    keeps distinct entries distinct by default.
    """
    if entry_id is None:
        entry_id = next(_ENTRY_IDS)
    return {
        'id': entry_id,
        'group': group,
        'country': country,
        'city': city,
        'name': name if name is not None else server_name,
        'server_name': server_name,
        'hostname': hostname,
        'port': 4443,
    }


class TestGenerateFilename:
    """Test suite for generate_filename function."""

    def test_should_prefix_country_to_main_group_label(self):
        """Should prefix country to main group label."""
        # Given: the Zurich 1 entry in the main Servers group
        server = make_server(
            'Servers', 'Switzerland', 'Zurich 1',
            name='Switzerland 1', city='Zurich',
            hostname='ch-01.jumptoserver.com',
        )

        # When: generating filename
        result = generate_filename(server)

        # Then: filename should read like the app listing
        assert result == "switzerland-zurich-1.conf"

    def test_should_strip_redundant_country_prefix_from_label(self):
        """Should strip redundant country prefix from label."""
        # Given: the Germany P2P 1 entry whose label already starts with the country
        server = make_server(
            'Servers', 'Germany', 'Germany P2P 1',
            city='Dusseldorf', hostname='de-dus1.jumptoserver.com',
        )

        # When: generating filename
        result = generate_filename(server)

        # Then: the country should not repeat
        assert result == "germany-p2p-1.conf"

    def test_should_prefix_country_to_city_label(self):
        """Should prefix country to city label."""
        # Given: the Lisbon entry in the main Servers group
        server = make_server(
            'Servers', 'Portugal', 'Lisbon',
            city='Lisbon', hostname='pt.jumptoserver.com',
        )

        # When: generating filename
        result = generate_filename(server)

        # Then: filename should combine country and label
        assert result == "portugal-lisbon.conf"

    def test_should_use_entry_label_alone_for_p2p_group(self):
        """Should use entry label alone for P2P group."""
        # Given: a Portugal P2P entry
        server = make_server(
            'P2P', 'Portugal', 'Portugal P2P',
            city='Lisbon', hostname='pt.jumptoserver.com',
        )

        # When: generating filename
        result = generate_filename(server)

        # Then: the label should be used as-is
        assert result == "portugal-p2p.conf"

    def test_should_use_entry_label_alone_for_streaming_group(self):
        """Should use entry label alone for Streaming group."""
        # Given: a Korea Streaming entry
        server = make_server(
            'Streaming..', 'South Korea', 'Korea Streaming',
            hostname='kr.jumptoserver.com',
        )

        # When: generating filename
        result = generate_filename(server)

        # Then: the label should be used as-is
        assert result == "korea-streaming.conf"

    def test_should_use_entry_label_alone_for_dvpn_group(self):
        """Should use entry label alone for D-VPN group."""
        # Given: a France Via UK entry
        server = make_server(
            'D-VPN', 'France', 'France Via UK',
            hostname='uk-dbl.jumptoserver.com',
        )

        # When: generating filename
        result = generate_filename(server)

        # Then: the label should be used as-is
        assert result == "france-via-uk.conf"

    def test_should_fall_back_to_city_when_server_name_missing(self):
        """Should fall back to city when server name missing."""
        # Given: a main group row without a server name
        server = make_server(
            'Servers', 'Spain', '',
            name='', city='Barcelona', hostname='es-01.jumptoserver.com',
        )

        # When: generating filename
        result = generate_filename(server)

        # Then: the city should complete the name
        assert result == "spain-barcelona.conf"

    def test_should_fall_back_to_hostname_prefix_when_labels_missing(self):
        """Should fall back to hostname prefix when labels missing."""
        # Given: a row with no country and no labels
        server = make_server(
            'Servers', '', '',
            name='', city='', hostname='auau.jumptoserver.com',
        )

        # When: generating filename
        result = generate_filename(server)

        # Then: the hostname prefix should be used
        assert result == "auau.conf"

    def test_should_return_conf_extension(self):
        """Should return conf extension."""
        # Given: any valid server
        server = make_server(
            'Servers', 'Test', 'City',
            city='City', hostname='test-01.jumptoserver.com',
        )

        # When: generating filename
        result = generate_filename(server)

        # Then: filename should end with .conf
        assert result.endswith('.conf')


class TestAssignUniqueFilenames:
    """Test suite for assign_unique_filenames function."""

    def test_should_assign_descriptive_names_when_no_conflicts(self):
        """Should assign descriptive names when no conflicts."""
        # Given: servers whose labels are unique
        servers = [
            make_server('Servers', 'Spain', 'Barcelona',
                        city='Barcelona', hostname='es-01.jumptoserver.com'),
            make_server('Servers', 'UK', 'London',
                        city='London', hostname='uk-01.jumptoserver.com'),
        ]

        # When: assigning filenames
        assignments = assign_unique_filenames(servers)

        # Then: names should combine country and label
        assert [filename for _, filename in assignments] == [
            "spain-barcelona.conf",
            "uk-london.conf",
        ]

    def test_should_share_one_file_for_entry_repeated_across_groups(self):
        """Should share one file for entry repeated across groups."""
        # Given: the same Portugal P2P entry listed in Servers and P2P
        servers = [
            make_server('Servers', 'Portugal', 'Portugal P2P',
                        city='Lisbon', hostname='pt.jumptoserver.com',
                        entry_id=1651),
            make_server('P2P', 'Portugal', 'Portugal P2P',
                        city='Lisbon', hostname='pt.jumptoserver.com',
                        entry_id=1651),
        ]

        # When: assigning filenames
        assignments = assign_unique_filenames(servers)

        # Then: every row keeps its assignment and both point at the same file
        assert [filename for _, filename in assignments] == [
            "portugal-p2p.conf",
            "portugal-p2p.conf",
        ]

    def test_should_keep_distinct_entries_that_share_a_hostname(self):
        """Should keep distinct entries that share a hostname."""
        # Given: Lisbon and Portugal P2P, both on pt.jumptoserver.com
        servers = [
            make_server('Servers', 'Portugal', 'Lisbon',
                        city='Lisbon', hostname='pt.jumptoserver.com'),
            make_server('Servers', 'Portugal', 'Portugal P2P',
                        city='Lisbon', hostname='pt.jumptoserver.com'),
        ]

        # When: assigning filenames
        assignments = assign_unique_filenames(servers)

        # Then: both app entries should get their own file
        assert sorted(filename for _, filename in assignments) == [
            "portugal-lisbon.conf",
            "portugal-p2p.conf",
        ]

    def test_should_disambiguate_distinct_servers_with_same_label(self):
        """Should disambiguate distinct servers with same label."""
        # Given: two Frankfurt servers carrying the same label
        servers = [
            make_server('Servers', 'Germany', 'Frankfurt',
                        city='Frankfurt', hostname='de-01.jumptoserver.com'),
            make_server('Servers', 'Germany', 'Frankfurt',
                        city='Frankfurt', hostname='de-02.jumptoserver.com'),
        ]

        # When: assigning filenames
        assignments = assign_unique_filenames(servers)

        # Then: the hostname prefix should disambiguate
        assert sorted(filename for _, filename in assignments) == [
            "germany-frankfurt-de-01.conf",
            "germany-frankfurt-de-02.conf",
        ]

    def test_should_assign_same_names_regardless_of_row_order(self):
        """Should assign same names regardless of row order."""
        # Given: colliding servers in two different orders
        servers = [
            make_server('Servers', 'Canada', 'Montreal',
                        city='Montreal', hostname='ca-01.jumptoserver.com'),
            make_server('Servers', 'Canada', 'Montreal',
                        city='Montreal', hostname='ca-mnt2.jumptoserver.com'),
        ]

        # When: assigning filenames in both orders
        forward = assign_unique_filenames(servers)
        backward = assign_unique_filenames(list(reversed(servers)))

        # Then: the set of names should not depend on order
        assert sorted(filename for _, filename in forward) == sorted(
            filename for _, filename in backward
        )

    def test_should_raise_when_distinct_entries_share_name_and_endpoint(self):
        """Should raise when distinct entries share name and endpoint."""
        # Given: two different app entries with identical labels and endpoints
        servers = [
            make_server('Servers', 'Germany', 'Frankfurt',
                        city='Frankfurt', hostname='de-01.jumptoserver.com'),
            make_server('Servers', 'Germany', 'Frankfurt',
                        city='Frankfurt', hostname='de-01.jumptoserver.com'),
        ]

        # When: assigning filenames
        # Then: they cannot be told apart, so the run should fail loudly
        with pytest.raises(ValueError, match='Cannot generate unique filenames'):
            assign_unique_filenames(servers)

    def test_should_raise_when_prefixes_cannot_disambiguate(self):
        """Should raise when prefixes cannot disambiguate."""
        # Given: two distinct servers with the same label and hostname prefix
        servers = [
            make_server('Servers', 'Germany', 'Frankfurt',
                        city='Frankfurt', hostname='de-01.jumptoserver.com'),
            make_server('Servers', 'Germany', 'Frankfurt',
                        city='Frankfurt', hostname='de-01.example.com'),
        ]

        # When: assigning filenames
        # Then: the unresolvable collision should fail loudly
        with pytest.raises(ValueError, match='Cannot generate unique filenames'):
            assign_unique_filenames(servers)

    def test_should_produce_unique_filenames(self):
        """Should produce unique filenames."""
        # Given: a mixed list with a repeated entry and a conflict
        servers = [
            make_server('Servers', 'Spain', 'Barcelona',
                        city='Barcelona', hostname='es-01.jumptoserver.com',
                        entry_id=1567),
            make_server('Servers', 'Spain', 'Barcelona',
                        city='Barcelona', hostname='es-01.jumptoserver.com',
                        entry_id=1567),
            make_server('Servers', 'Canada', 'Montreal',
                        city='Montreal', hostname='ca-stream.jumptoserver.com'),
            make_server('Servers', 'Canada', 'Montreal',
                        city='Montreal', hostname='ca-01.jumptoserver.com'),
            make_server('Servers', 'Brazil', '',
                        city='', hostname='br-03.jumptoserver.com'),
        ]

        # When: assigning filenames
        assignments = assign_unique_filenames(servers)

        # Then: every row gets an assignment and the repeated entry shares a file
        filenames = [filename for _, filename in assignments]
        assert len(filenames) == 5
        assert len(set(filenames)) == 4
