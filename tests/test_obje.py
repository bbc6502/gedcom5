from gedcom5.parser import GEDCOM5Parser
from tests.structures import note_structure, source_citation, change_date


class TestCase:

    def test_obje(self):
        parser = GEDCOM5Parser()
        msg = '\n'.join([
            '0 OBJE',
            '1 FILE',
            '2 FORM',
            '3 TYPE',
            '3 MEDI',
            '2 TITL',
            '1 REFN',
            '2 TYPE',
            '1 RIN',
            '1 TITL',
            *note_structure(1),
            *note_structure(1),
            *source_citation(1),
            *source_citation(1),
            *change_date(1),
        ])
        gedcom = parser.parse_string(msg, strict=True)
        assert gedcom[0].as_text() == msg
