from gedcom5.parser import GEDCOM5Parser
from tests.structures import note_structure, source_citation, change_date, address_structure


class TestCase:

    def test_repo(self):
        parser = GEDCOM5Parser()
        msg = '\n'.join([
            '0 REPO',
            '1 CALN',
            '2 MEDI',
            '1 NAME',
            *address_structure(1),
            *note_structure(1),
            *note_structure(1),
            '1 REFN',
            '2 TYPE',
            '1 REFN',
            '2 TYPE',
            '1 RIN',
            *change_date(1),
        ])
        gedcom = parser.parse_string(msg, strict=True)
        assert gedcom[0].as_text() == msg
