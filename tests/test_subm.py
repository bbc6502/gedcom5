from gedcom5.parser import GEDCOM5Parser
from tests.structures import note_structure, change_date, multimedia_link, \
    source_repository_citation, address_structure


class TestCase:

    def test_subm(self):
        parser = GEDCOM5Parser()
        msg = '\n'.join([
            '0 SUBM',
            '1 NAME',
            *address_structure(1),
            *multimedia_link(1),
            *multimedia_link(1),
            '1 LANG',
            '1 RFN',
            '1 RIN',
            *note_structure(1),
            *note_structure(1),
            *change_date(1),
        ])
        gedcom = parser.parse_string(msg, strict=True)
        assert gedcom[0].as_text() == msg
