from gedcom5.parser import GEDCOM5Parser
from tests.structures import family_event_structure, lds_spouse_sealing


class TestCase:

    def test_fam_structure(self):
        parser = GEDCOM5Parser()
        msg = '\n'.join([
            '0 FAM',
            '1 RESN',
            *family_event_structure(1),
            '1 HUSB',
            '1 WIFE',
            '1 CHIL',
            '1 CHIL',
            '1 CHIL',
            '1 NCHI',
            '1 SUBM',
            '1 SUBM',
            *lds_spouse_sealing(1),
            '1 REFN',
            '2 TYPE',
            '1 REFN',
            '2 TYPE',
            '1 RIN',
            '1 CHAN',
            '1 NOTE',
            '1 NOTE',
            '1 SOUR',
            '1 SOUR',
            '1 OBJE',
            '1 OBJE',
        ])
        gedcom = parser.parse_string(msg, strict=True)
        p1 = gedcom[0].as_text().split('\n')
        p2 = msg.split('\n')
        for n, (n1, n2) in enumerate(zip(p1, p2)):
            print(f'{n}: {n1} != {n2}')
            assert n1 == n2, f'{n}: {n1} != {n2}'
