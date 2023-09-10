from gedcom5.parser import GEDCOM5Parser
from gedcom5.tag import INDI
from tests.structures import personal_name_structure, change_date, note_structure, source_citation, multimedia_link, \
    individual_event_structure, individual_attribute_structure, lds_individual_ordinance, child_to_family_link, \
    spouse_to_family_link, association_structure


class TestCase:

    def test_indi(self):
        parser = GEDCOM5Parser()
        msg = '\n'.join([
            '0 INDI',
            '1 RESN',
            *personal_name_structure(1),
            '1 SEX',
            *individual_event_structure(1),
            *individual_attribute_structure(1),
            *lds_individual_ordinance(1),
            *child_to_family_link(1),
            *spouse_to_family_link(1),
            '1 SUBM',
            *association_structure(1),
            '1 ALIA',
            '1 ANCI',
            '1 DESI',
            '1 RFN',
            '1 AFN',
            '1 REFN',
            '2 TYPE',
            '1 RIN',
            *change_date(1),
            *note_structure(1),
            *source_citation(1),
            *multimedia_link(1),
        ])
        gedcom = parser.parse_string(msg, strict=True)
        assert gedcom[0].as_text() == msg

    def test_private_birth(self):
        msg = '\n'.join([
            '0 INDI',
            '1 BIRT',
            '1 BIRT',
            '2 DATE 1969'
        ])
        parser = GEDCOM5Parser()
        gedcom = parser.parse_string(msg)
        indi = gedcom.indi[0]
        assert indi.is_private() is True

    def test_not_private_birth(self):
        msg = '\n'.join([
            '0 INDI',
            '1 BIRT',
            '1 BIRT',
            '2 DATE 1901'
        ])
        parser = GEDCOM5Parser()
        gedcom = parser.parse_string(msg)
        indi = gedcom.indi[0]
        assert indi.is_private() is False

    def test_private_baptism(self):
        msg = '\n'.join([
            '0 INDI',
            '1 BAPM',
            '1 BAPM',
            '2 DATE 1969'
        ])
        parser = GEDCOM5Parser()
        gedcom = parser.parse_string(msg)
        indi = gedcom.indi[0]
        assert indi.is_private() is True

    def test_not_private_baptism(self):
        msg = '\n'.join([
            '0 INDI',
            '1 BAPM',
            '1 BAPM',
            '2 DATE 1910'
        ])
        parser = GEDCOM5Parser()
        gedcom = parser.parse_string(msg)
        indi = gedcom.indi[0]
        assert indi.is_private() is False

    def test_private_christening(self):
        msg = '\n'.join([
            '0 INDI',
            '1 CHR',
            '1 CHR',
            '2 DATE 1969'
        ])
        parser = GEDCOM5Parser()
        gedcom = parser.parse_string(msg)
        indi = gedcom.indi[0]
        assert indi.is_private() is True

    def test_not_private_christening(self):
        msg = '\n'.join([
            '0 INDI',
            '1 CHR',
            '1 CHR',
            '2 DATE 1905'
        ])
        parser = GEDCOM5Parser()
        gedcom = parser.parse_string(msg)
        indi = gedcom.indi[0]
        assert indi.is_private() is False

    def test_private_no_dates(self):
        msg = '\n'.join([
            '0 INDI',
        ])
        parser = GEDCOM5Parser()
        gedcom = parser.parse_string(msg)
        indi = gedcom.indi[0]
        assert indi.is_private() is True

    def test_private_death_date(self):
        msg = '\n'.join([
            '0 INDI',
            '1 DEAT',
            '2 DATE 1969'
        ])
        parser = GEDCOM5Parser()
        gedcom = parser.parse_string(msg)
        indi = gedcom.indi[0]
        assert indi.is_private() is True

    def test_not_private_death_date(self):
        msg = '\n'.join([
            '0 INDI',
            '1 DEAT',
            '1 DEAT',
            '2 DATE 1901'
        ])
        parser = GEDCOM5Parser()
        gedcom = parser.parse_string(msg)
        indi = gedcom.indi[0]
        assert indi.is_private() is False

    def test_not_private_burial_date(self):
        msg = '\n'.join([
            '0 INDI',
            '1 BURI',
            '1 BURI',
            '2 DATE 1901'
        ])
        parser = GEDCOM5Parser()
        gedcom = parser.parse_string(msg)
        indi = gedcom.indi[0]
        assert indi.is_private() is False

    def test_not_private_cremation_date(self):
        msg = '\n'.join([
            '0 INDI',
            '1 CREM',
            '1 CREM',
            '2 DATE 1901'
        ])
        parser = GEDCOM5Parser()
        gedcom = parser.parse_string(msg)
        indi = gedcom.indi[0]
        assert indi.is_private() is False
