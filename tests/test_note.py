from gedcom5.parser import GEDCOM5Parser
from tests.structures import note_structure, source_citation, change_date


class TestCase:

    def test_note(self):
        parser = GEDCOM5Parser()
        msg = '\n'.join([
            '0 NOTE',
            '1 CONC',
            '1 CONT',
            '1 CONC',
            '1 CONT',
            '1 REFN',
            '2 TYPE',
            '1 REFN',
            '2 TYPE',
            '1 RIN',
            *source_citation(1),
            *source_citation(1),
            *change_date(1),
        ])
        gedcom = parser.parse_string(msg, strict=True)
        assert gedcom[0].as_text() == msg
