from gedcom5.parser import GEDCOM5Parser


class TestCase:

    def test_anum(self):
        parser = GEDCOM5Parser()
        msg = '\n'.join(['0 ANUL', '1 HUSB', '2 AGE'])
        gedcom = parser.parse_string(msg)
        assert len(gedcom) == 1
        assert gedcom[0].tag == 'ANUL'
        assert len(gedcom[0]) == 1
        assert gedcom[0][0].tag == 'HUSB'
        assert len(gedcom[0][0]) == 1
        assert gedcom[0][0][0].tag == 'AGE'
        assert gedcom[0].as_text() == msg

    def test_husb(self):
        parser = GEDCOM5Parser()
        msg = '\n'.join(['1 HUSB', '2 AGE'])
        gedcom = parser.parse_string(msg)
        assert len(gedcom) == 1
        assert gedcom[0].tag == 'HUSB'
        assert len(gedcom[0]) == 1
        assert gedcom[0][0].tag == 'AGE'
        assert gedcom[0].as_text() == msg
