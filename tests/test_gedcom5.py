from os.path import dirname, join

import pytest

from gedcom5.gedcom import GEDCOM, InvalidGEDCOM
from gedcom5.parser import GEDCOM5Parser
from gedcom5.tag import Tag, AddressStructure, UnexpectedTag, AssociationStructure, ChangeDate, ChildToFamilyLink, \
    SpouseToFamilyLink, PlaceStructure, PLAC, MultimediaLink, NoteStructure, SourceCitation, EventDetail, \
    PersonalNameStructure, IndividualEventStructure, IndividualAttributeStructure, LDSIndividualOrdinance, \
    FamilyEventStructure, LDSSpouseSealing, SourceRepositoryCitation, HEAD, PAGE, VERS, DATE, COPR, CONT, CONC, DEST, \
    TIME, FILE, GEDC, FORM, CHAR, LANG, ANCE, DESC, NOTE, RESN, HUSB, WIFE, CHIL, REFN, TYPE, RIN, SEX, ALIA, ANCI, \
    DESI, RFN, AFN, AGNC, AUTH, ABBR, PUBL, TEXT, FAMF, TEMP, ORDI, ADDR, ADR1, ADR2, ADR3, CITY, STAE, CTRY, POST, \
    PHON, EMAIL, FAX, WWW, ASSO, RELA, CHAN, FAMC, PEDI, STAT, CAUS, AGE, BAPL, CONL, ENDL, SLGC, MEDI, NPFX, GIVN, \
    NICK, SPFX, SURN, NSFX, MAP, LATI, LONG, ROLE, QUAY, CALN


class TestCase:

    def test_repr(self):
        assert repr(Tag(level=1, tag='HEAD')) == '1 HEAD'

    def test_iter(self):
        msg = '\n'.join([
            '0 HEAD',
            '0 INDI',
        ])
        gedcom = GEDCOM5Parser().parse_string(msg)
        for child, name in zip(gedcom, ['HEAD', 'INDI']):
            assert child.tag == name

    def test_replace(self):
        msg = '\n'.join([
            '0 HEAD',
            '1 SOUR',
        ])
        gedcom = GEDCOM5Parser().parse_string(msg)
        gedcom[0][0] = Tag(1, tag='XXXX')
        for child, name in zip(gedcom[0], ['XXXX']):
            assert child.tag == name

    def test_find_first(self):
        msg = '\n'.join([
            '0 FAM',
            '1 NOTE',
            '2 CONT Abc',
            '1 NOTE',
            '2 CONT',
        ])
        gedcom = GEDCOM5Parser().parse_string(msg)
        assert gedcom[0].find_first('NOTE.CONT').value == 'Abc'

    def test_find_first_gedcom(self):
        msg = '\n'.join([
            '0 FAM',
            '1 NOTE ABCDEF',
            '0 FAM',
            '1 NOTE',
        ])
        gedcom = GEDCOM5Parser().parse_string(msg)
        assert gedcom.find_first('FAM.NOTE').value == 'ABCDEF'

    def test_find_first_gedcom_default(self):
        msg = '\n'.join([
            '0 FAM',
            '0 FAM',
        ])
        gedcom = GEDCOM5Parser().parse_string(msg)
        assert gedcom.find_first('FAM.NOTE', 'ABCDEF') == 'ABCDEF'

    def test_find_first_default(self):
        msg = '\n'.join([
            '0 FAM',
            '1 NOTE',
            '2 CONT Abc',
            '1 NOTE',
            '2 CONT',
        ])
        gedcom = GEDCOM5Parser().parse_string(msg)
        assert gedcom[0].find_first('NOTE.CONC', default='Xyz') == 'Xyz'

    def test_address_structure_strict(self):
        with pytest.raises(UnexpectedTag):
            uut = AddressStructure()
            uut.append(Tag(1,tag='XXXX'), strict=True)

    def test_association_structure_strict(self):
        with pytest.raises(UnexpectedTag):
            uut = AssociationStructure()
            uut.append(Tag(1,tag='XXXX'), strict=True)

    def test_change_date(self):
        with pytest.raises(UnexpectedTag):
            uut = ChangeDate()
            uut.append(Tag(1,tag='XXXX'), strict=True)

    def test_child_to_family_link(self):
        with pytest.raises(UnexpectedTag):
            uut = ChildToFamilyLink()
            uut.append(Tag(1,tag='XXXX'), strict=True)

    def test_spouse_to_family_link(self):
        with pytest.raises(UnexpectedTag):
            uut = SpouseToFamilyLink()
            uut.append(Tag(1,tag='XXXX'), strict=True)

    def test_place_structure(self):
        uut = PlaceStructure()
        assert uut.append(PLAC(1, Tag(0))) == True

    def test_place_structure_strict(self):
        uut = PlaceStructure()
        with pytest.raises(UnexpectedTag):
            uut.append(Tag(1, Tag(0)), strict=True)

    def test_multimedia_link_strict(self):
        uut = MultimediaLink()
        with pytest.raises(UnexpectedTag):
            uut.append(Tag(1,tag='XXXX'), strict=True)

    def test_note_structure_strict(self):
        uut = NoteStructure()
        with pytest.raises(UnexpectedTag):
            uut.append(Tag(1,tag='XXXX'), strict=True)

    def test_source_citation_strict(self):
        uut = SourceCitation()
        with pytest.raises(UnexpectedTag):
            uut.append(Tag(1,tag='XXXX'), strict=True)

    def test_event_detail_place(self):
        uut = EventDetail()
        assert uut.append(PLAC(1, Tag(0))) is True

    def test_personal_name_structure(self):
        uut = PersonalNameStructure()
        with pytest.raises(UnexpectedTag):
            uut.append(Tag(1,tag='XXXX'), strict=True)

    def test_individual_event_structure(self):
        uut = IndividualEventStructure()
        with pytest.raises(UnexpectedTag):
            uut.append(Tag(1,tag='XXXX'), strict=True)

    def test_individual_attribute_structure(self):
        uut = IndividualAttributeStructure()
        with pytest.raises(UnexpectedTag):
            uut.append(Tag(1,tag='XXXX'), strict=True)

    def test_lds_individual_ordinance(self):
        uut = LDSIndividualOrdinance()
        with pytest.raises(UnexpectedTag):
            uut.append(Tag(1,tag='XXXX'), strict=True)

    def test_family_event_structure(self):
        uut = FamilyEventStructure()
        with pytest.raises(UnexpectedTag):
            uut.append(Tag(1,tag='XXXX'), strict=True)

    def test_lds_spouse_sealing(self):
        uut = LDSSpouseSealing()
        with pytest.raises(UnexpectedTag):
            uut.append(Tag(1,tag='XXXX'), strict=True)

    def test_source_repository_citation(self):
        uut = SourceRepositoryCitation()
        with pytest.raises(UnexpectedTag):
            uut.append(Tag(1,tag='XXXX'), strict=True)

    tags = [
        HEAD, PAGE, VERS, DATE, COPR, CONT, CONC, DEST, TIME, FILE, GEDC, FORM, CHAR, LANG, ANCE,
        DESC, NOTE, RESN, HUSB, WIFE, CHIL, REFN, TYPE, RIN, SEX, ALIA, ANCI, DESI, RFN, AFN,
        AGNC, AUTH, ABBR, PUBL, TEXT, FAMF, TEMP, ORDI, ADDR, ADR1, ADR2, ADR3, CITY, STAE,
        CTRY, POST, PHON, EMAIL, FAX, WWW, ASSO, RELA, CHAN, FAMC, PEDI, STAT, CAUS, AGE, BAPL,
        CONL, ENDL, SLGC, MEDI, NPFX, GIVN, NICK, SPFX, SURN, NSFX, MAP, LATI, LONG, ROLE, QUAY,
        CALN
    ]

    @pytest.mark.parametrize('tag', tags)
    def test_strict(self, tag):
        uut = tag(1, Tag(0))
        with pytest.raises(UnexpectedTag):
            uut.append(Tag(1,tag='XXXX'), strict=True)

    @pytest.mark.parametrize('tag', tags)
    def test_non_strict(self, tag):
        uut = tag(1, Tag(0))
        assert uut.append(Tag(1, tag='XXXX')) is False

    def test_gedcom_strict(self):
        uut = GEDCOM()
        with pytest.raises(UnexpectedTag):
            uut.append(Tag(1,tag='XXXX'), strict=True)

    def test_gedcom_non_strict(self):
        uut = GEDCOM()
        assert uut.append(Tag(1, tag='XXXX')) is False

    def test_parse_from_file(self):
        gedcom = GEDCOM5Parser().parse_path(join(dirname(__file__), '555SAMPLE.GED'))
        assert len(gedcom) == 10
        assert gedcom[1].tag == 'SUBM'
        assert gedcom.find('HEAD.GEDC.VERS')[0].value == '5.5.5'
        head = gedcom.find('HEAD')[0]
        assert head.find('GEDC.VERS')[0].value == '5.5.5'
        assert [item.tag for item in gedcom] == [
            'HEAD', 'SUBM', 'INDI', 'INDI', 'INDI', 'FAM', 'FAM', 'SOUR', 'REPO', 'TRLR'
        ]

    def test_resolve_references(self):
        msg = '\n'.join([
            '0 @I1@ INDI',
            '1 NAME Bob',
            '1 FAMC @F1@',
            '0 @F1@ FAM',
        ])
        gedcom = GEDCOM5Parser().parse_string(msg, strict=True)
        assert gedcom.fam[0].xref_id == '@F1@'
        assert gedcom.indi[0].famc[0].value == '@F1@'
        assert gedcom.indi[0].famc[0].ref == gedcom.fam[0]

    def test_unresolved_references(self):
        msg = '\n'.join([
            '0 @I1@ INDI',
            '1 NAME Bob',
            '1 FAMC @F2@',
            '0 @F1@ FAM',
        ])
        with pytest.raises(InvalidGEDCOM):
            GEDCOM5Parser().parse_string(msg, strict=True)

    def test_unresolved_references_not_strict(self):
        msg = '\n'.join([
            '0 @I1@ INDI',
            '1 NAME Bob',
            '1 FAMC @F2@',
            '0 @F1@ FAM',
        ])
        gedcom = GEDCOM5Parser().parse_string(msg, strict=False)
        assert gedcom.indi[0].famc[0].ref == '@F2@'
        assert gedcom.indi[0].is_private() is True

    def test_resolved_references_is_private_father(self):
        msg = '\n'.join([
            '0 @I1@ INDI',
            '1 NAME Bob',
            '1 FAMC @F1@',
            '0 @F1@ FAM',
            '1 HUSB @I2@',
            '0 @I2@ INDI',
            '1 BIRT',
            '2 DATE 01 MAR 1995'
        ])
        gedcom = GEDCOM5Parser().parse_string(msg, strict=False)
        assert gedcom.indi[0].famc[0].ref == gedcom.fam[0]
        assert gedcom.indi[0].is_private() is True

    def test_resolved_references_is_private_mother(self):
        msg = '\n'.join([
            '0 @I1@ INDI',
            '1 NAME Bob',
            '1 FAMC @F1@',
            '0 @F1@ FAM',
            '1 WIFE @I2@',
            '0 @I2@ INDI',
            '1 BIRT',
            '2 DATE 01 MAR 1995'
        ])
        gedcom = GEDCOM5Parser().parse_string(msg, strict=False)
        assert gedcom.indi[0].famc[0].ref == gedcom.fam[0]
        assert gedcom.indi[0].is_private() is True

    def test_fathers_birth_more_than_140_years_ago(self):
        msg = '\n'.join([
            '0 @I1@ INDI',
            '1 NAME Bob',
            '1 FAMC @F1@',
            '0 @F1@ FAM',
            '1 HUSB @I2@',
            '0 @I2@ INDI',
            '1 BIRT',
            '2 DATE 01 MAR 1795'
        ])
        gedcom = GEDCOM5Parser().parse_string(msg, strict=False)
        assert gedcom.indi[0].famc[0].ref == gedcom.fam[0]
        assert gedcom.indi[0].is_private() is False

    def test_fathers_birth_more_than_100_years_less_than_140_years_ago(self):
        msg = '\n'.join([
            '0 @I1@ INDI',
            '1 NAME Bob',
            '1 FAMC @F1@',
            '0 @F1@ FAM',
            '1 HUSB @I2@',
            '0 @I2@ INDI',
            '1 BIRT',
            '2 DATE 01 MAR 1900'
        ])
        gedcom = GEDCOM5Parser().parse_string(msg, strict=False)
        assert gedcom.indi[0].famc[0].ref == gedcom.fam[0]
        assert gedcom.indi[0].is_private() is True

    def test_mothers_birth_more_than_140_years_ago(self):
        msg = '\n'.join([
            '0 @I1@ INDI',
            '1 NAME Bob',
            '1 FAMC @F1@',
            '0 @F1@ FAM',
            '1 WIFE @I2@',
            '0 @I2@ INDI',
            '1 BIRT',
            '2 DATE 01 MAR 1795'
        ])
        gedcom = GEDCOM5Parser().parse_string(msg, strict=False)
        assert gedcom.indi[0].famc[0].ref == gedcom.fam[0]
        assert gedcom.indi[0].is_private() is False

    def test_mothers_birth_more_than_100_years_less_than_140_years_ago(self):
        msg = '\n'.join([
            '0 @I1@ INDI',
            '1 NAME Bob',
            '1 FAMC @F1@',
            '0 @F1@ FAM',
            '1 WIFE @I2@',
            '0 @I2@ INDI',
            '1 BIRT',
            '2 DATE 01 MAR 1900'
        ])
        gedcom = GEDCOM5Parser().parse_string(msg, strict=False)
        assert gedcom.indi[0].famc[0].ref == gedcom.fam[0]
        assert gedcom.indi[0].is_private() is True

    def test_fathers_death_more_than_100_years_ago(self):
        msg = '\n'.join([
            '0 @I1@ INDI',
            '1 NAME Bob',
            '1 FAMC @F1@',
            '0 @F1@ FAM',
            '1 HUSB @I2@',
            '0 @I2@ INDI',
            '1 DEAT',
            '2 DATE 01 MAR 1795'
        ])
        gedcom = GEDCOM5Parser().parse_string(msg, strict=False)
        assert gedcom.indi[0].famc[0].ref == gedcom.fam[0]
        assert gedcom.indi[0].is_private() is False

    def test_mothers_death_more_than_100_years_ago(self):
        msg = '\n'.join([
            '0 @I1@ INDI',
            '1 NAME Bob',
            '1 FAMC @F1@',
            '0 @F1@ FAM',
            '1 WIFE @I2@',
            '0 @I2@ INDI',
            '1 DEAT',
            '2 DATE 01 MAR 1795'
        ])
        gedcom = GEDCOM5Parser().parse_string(msg, strict=False)
        assert gedcom.indi[0].is_private() is False
