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

    def test_note_formatting(self):
        parser = GEDCOM5Parser()
        msg = '\n'.join([
            '0 NOTE This is the first line',
            '1 CONC  of the note.',
            '1 CONT This is the second line',
            '1 CONC  of the note.',
        ])
        gedcom = parser.parse_string(msg, strict=True)
        assert gedcom[0].note == [
            'This is the first line of the note.',
            'This is the second line of the note.'
        ]

    def test_note_formatting_no_continuation(self):
        parser = GEDCOM5Parser()
        msg = '\n'.join([
            '0 NOTE This is the first line',
            '1 CONC  of the note.',
        ])
        gedcom = parser.parse_string(msg, strict=True)
        assert gedcom[0].note == [
            'This is the first line of the note.',
        ]

    def test_note_formatting_no_concatenation(self):
        parser = GEDCOM5Parser()
        msg = '\n'.join([
            '0 NOTE This is the first line',
        ])
        gedcom = parser.parse_string(msg, strict=True)
        assert gedcom[0].note == [
            'This is the first line',
        ]

    def test_note_formatting_with_continuation(self):
        parser = GEDCOM5Parser()
        msg = '\n'.join([
            '0 NOTE This is the first line',
            '1 CONT This is the second line',
        ])
        gedcom = parser.parse_string(msg, strict=True)
        assert gedcom[0].note == [
            'This is the first line',
            'This is the second line',
        ]

    def test_note_formatting_with_continuation_2(self):
        parser = GEDCOM5Parser()
        msg = '\n'.join([
            '0 NOTE This is the first line',
            '1 CONT This is the second line',
            '1 CONT This is the third line',
        ])
        gedcom = parser.parse_string(msg, strict=True)
        assert gedcom[0].note == [
            'This is the first line',
            'This is the second line',
            'This is the third line',
        ]

    def test_note_formatting_with_concatenation(self):
        parser = GEDCOM5Parser()
        msg = '\n'.join([
            '0 NOTE This is the first line',
            '1 CONC  of the',
            '1 CONC  note.'
        ])
        gedcom = parser.parse_string(msg, strict=True)
        assert gedcom[0].note == [
            'This is the first line of the note.',
        ]

    def test_blank_note(self):
        parser = GEDCOM5Parser()
        msg = '\n'.join([
            '0 NOTE ',
        ])
        gedcom = parser.parse_string(msg, strict=True)
        assert gedcom[0].note == []
