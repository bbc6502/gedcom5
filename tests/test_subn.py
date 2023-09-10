from gedcom5.parser import GEDCOM5Parser
from tests.structures import note_structure, change_date, multimedia_link, \
    source_repository_citation


class TestCase:

    def test_subn(self):
        parser = GEDCOM5Parser()
        msg = '\n'.join([
            '0 SUBN',
            '1 SUBM',
            '1 FAMF',
            '1 TEMP',
            '1 ANCE',
            '1 DESC',
            '1 ORDI',
            '1 RIN',
            *note_structure(1),
            *note_structure(1),
            *change_date(1),
        ])
        gedcom = parser.parse_string(msg, strict=True)
        assert gedcom[0].as_text() == msg
