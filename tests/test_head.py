from gedcom5.parser import GEDCOM5Parser


class TestCase:

    def test_head_structure(self):
        parser = GEDCOM5Parser()
        msg = '\n'.join([
            '0 @H1@ HEAD Header',
            '1 SOUR',
            '2 VERS',
            '2 NAME',
            '2 CORP',
            '3 ADDR',
            '4 CONT',
            '4 CONT',
            '4 ADR1',
            '4 ADR2',
            '4 ADR3',
            '4 CITY',
            '4 STAE',
            '4 POST',
            '4 CTRY',
            '3 PHON',
            '3 PHON',
            '3 PHON',
            '3 EMAIL',
            '3 EMAIL',
            '3 EMAIL',
            '3 FAX',
            '3 FAX',
            '3 FAX',
            '3 WWW',
            '3 WWW',
            '3 WWW',
            '2 DATA',
            '3 DATE',
            '3 COPR',
            '4 CONC',
            '4 CONT',
            '4 CONC',
            '4 CONT',
            '1 DEST',
            '1 DATE',
            '2 TIME',
            '1 SUBM',
            '1 SUBN',
            '1 FILE',
            '1 COPR',
            '1 GEDC',
            '2 VERS',
            '2 FORM',
            '1 CHAR',
            '2 VERS',
            '1 LANG',
            '1 PLAC',
            '2 FORM',
            '1 NOTE',
            '2 CONC',
            '2 CONT',
            '2 CONC',
            '2 CONT',
        ])
        gedcom = parser.parse_string(msg, strict=True)
        assert gedcom[0].as_text() == msg
        assert len(gedcom) == 1
        assert len(gedcom[0]) == 12
        assert len(gedcom[0][0]) == 4
        assert gedcom[0].tag == 'HEAD'
        assert gedcom[0][0].tag == 'SOUR'
        assert gedcom[0][0][0].tag == 'VERS'
        assert gedcom[0][0][1].tag == 'NAME'
        assert gedcom[0][1].tag == 'DEST'
        assert gedcom[0][2].tag == 'DATE'
        assert gedcom[0][2][0].tag == 'TIME'
