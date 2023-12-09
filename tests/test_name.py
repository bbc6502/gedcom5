from gedcom5.parser import GEDCOM5Parser


class TestCase:

    def test_given_name_with_prefix(self):
        msg = '\n'.join([
            '0 @I1@ INDI',
            '1 NAME Bob Gerald /SMITH/',
            '2 GIVN Bob Gerald',
            '2 NPFX Mr',
            '2 SURN SMITH',
        ])
        gedcom = GEDCOM5Parser().parse_string(msg, strict=False)
        assert gedcom.indi[0].name[0].given_names == 'Mr Bob Gerald'

    def test_given_name_without_prefix(self):
        msg = '\n'.join([
            '0 @I1@ INDI',
            '1 NAME Bob Gerald /SMITH/',
            '2 GIVN Bob Gerald',
            '2 SURN SMITH',
        ])
        gedcom = GEDCOM5Parser().parse_string(msg, strict=False)
        assert gedcom.indi[0].name[0].given_names == 'Bob Gerald'

    def test_no_given_name(self):
        msg = '\n'.join([
            '0 @I1@ INDI',
            '1 NAME /SMITH/',
            '2 SURN SMITH',
        ])
        gedcom = GEDCOM5Parser().parse_string(msg, strict=False)
        assert gedcom.indi[0].name[0].given_names is None

    def test_family_name(self):
        msg = '\n'.join([
            '0 @I1@ INDI',
            '1 NAME /SMITH/',
            '2 SURN SMITH',
        ])
        gedcom = GEDCOM5Parser().parse_string(msg, strict=False)
        assert gedcom.indi[0].name[0].family_name == 'SMITH'

    def test_family_name_with_prefix(self):
        msg = '\n'.join([
            '0 @I1@ INDI',
            '1 NAME /SMITH/',
            '2 SURN SMITH',
            '2 SPFX Jr',
        ])
        gedcom = GEDCOM5Parser().parse_string(msg, strict=False)
        assert gedcom.indi[0].name[0].family_name == 'SMITH Jr'

    def test_no_family_name(self):
        msg = '\n'.join([
            '0 @I1@ INDI',
            '1 NAME /SMITH/',
        ])
        gedcom = GEDCOM5Parser().parse_string(msg, strict=False)
        assert gedcom.indi[0].name[0].family_name is None

    def test_full_name(self):
        msg = '\n'.join([
            '0 @I1@ INDI',
            '1 NAME /SMITH/',
            '2 NPFX Hon',
            '2 GIVN John',
            '2 SPFX Jr',
            '2 SURN SMITH',
            '2 NSFX OAM',
        ])
        gedcom = GEDCOM5Parser().parse_string(msg, strict=False)
        assert gedcom.indi[0].name[0].full_name == 'Hon John Jr SMITH OAM'

    def test_full_name_no_prefix(self):
        msg = '\n'.join([
            '0 @I1@ INDI',
            '1 NAME /SMITH/',
            '2 GIVN John',
            '2 SPFX Jr',
            '2 SURN SMITH',
            '2 NSFX OAM',
        ])
        gedcom = GEDCOM5Parser().parse_string(msg, strict=False)
        assert gedcom.indi[0].name[0].full_name == 'John Jr SMITH OAM'

    def test_full_name_no_given(self):
        msg = '\n'.join([
            '0 @I1@ INDI',
            '1 NAME /SMITH/',
            '2 SPFX Jr',
            '2 SURN SMITH',
            '2 NSFX OAM',
        ])
        gedcom = GEDCOM5Parser().parse_string(msg, strict=False)
        assert gedcom.indi[0].name[0].full_name == 'Jr SMITH OAM'

    def test_full_name_no_surname_prefix(self):
        msg = '\n'.join([
            '0 @I1@ INDI',
            '1 NAME /SMITH/',
            '2 SURN SMITH',
            '2 NSFX OAM',
        ])
        gedcom = GEDCOM5Parser().parse_string(msg, strict=False)
        assert gedcom.indi[0].name[0].full_name == 'SMITH OAM'

    def test_full_name_no_surname(self):
        msg = '\n'.join([
            '0 @I1@ INDI',
            '1 NAME /SMITH/',
            '2 NSFX OAM',
        ])
        gedcom = GEDCOM5Parser().parse_string(msg, strict=False)
        assert gedcom.indi[0].name[0].full_name == 'OAM'

    def test_full_name_no_name_suffix(self):
        msg = '\n'.join([
            '0 @I1@ INDI',
            '1 NAME /SMITH/',
            '2 SURN SMITH'
        ])
        gedcom = GEDCOM5Parser().parse_string(msg, strict=False)
        assert gedcom.indi[0].name[0].full_name == 'SMITH'

    def test_full_name_nothing(self):
        msg = '\n'.join([
            '0 @I1@ INDI',
            '1 NAME /SMITH/',
        ])
        gedcom = GEDCOM5Parser().parse_string(msg, strict=False)
        assert gedcom.indi[0].name[0].full_name is None
