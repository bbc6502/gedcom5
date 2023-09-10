from gedcom5.parser import GEDCOM5Parser
from tests.structures import note_structure, change_date, multimedia_link, \
    source_repository_citation


class TestCase:

    def test_sour(self):
        parser = GEDCOM5Parser()
        msg = '\n'.join([
            '0 SOUR',
            '1 CONT',
            '1 CONC',
            '1 DATA',
            '2 EVEN',
            '3 DATE',
            '3 PLAC',
            '2 EVEN',
            '3 DATE',
            '3 PLAC',
            '2 AGNC',
            *note_structure(2),
            *note_structure(2),
            '1 AUTH',
            '2 CONC',
            '2 CONT',
            '2 CONC',
            '1 TITL',
            '2 CONC',
            '2 CONT',
            '2 CONC',
            '1 ABBR',
            '1 PUBL',
            '2 CONC',
            '2 CONT',
            '2 CONC',
            '1 TEXT',
            '2 CONC',
            '2 CONT',
            '2 CONC',
            *source_repository_citation(1),
            *source_repository_citation(1),
            '1 REFN',
            '2 TYPE',
            '1 REFN',
            '2 TYPE',
            '1 RIN',
            *change_date(1),
            *note_structure(1),
            *note_structure(1),
            *multimedia_link(1),
            *multimedia_link(1),
        ])
        gedcom = parser.parse_string(msg, strict=True)
        assert gedcom[0].as_text() == msg
