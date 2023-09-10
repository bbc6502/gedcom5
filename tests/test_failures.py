import pytest

from gedcom5.parser import GEDCOM5Parser, ParseError


class TestCase:

    def test_invalid_line(self):
        with pytest.raises(ParseError):
            parser = GEDCOM5Parser()
            msg = '\n'.join([
                'ABC',
            ])
            parser.parse_string(msg, strict=True)

    def test_unexpected_tag(self):
        with pytest.raises(ParseError):
            parser = GEDCOM5Parser()
            msg = '\n'.join([
                '0 HEAD',
                '1 CONT',
            ])
            parser.parse_string(msg, strict=True)

    def test_unknown_tag(self):
        with pytest.raises(ParseError):
            parser = GEDCOM5Parser()
            msg = '\n'.join([
                '0 HEAD',
                '1 XXXX',
            ])
            parser.parse_string(msg, strict=True)

    def test_empty_lines(self):
        with pytest.raises(ParseError):
            parser = GEDCOM5Parser()
            msg = '\n\n\n'
            parser.parse_string(msg, strict=True)
