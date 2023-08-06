from os.path import dirname, join

from gedcom5 import GEDCOM5


class TestCase:

    def test_parse_from_file(self):
        with open(join(dirname(__file__), '555SAMPLE.GED'), 'rb') as fp:
            gedcom = GEDCOM5().parse_stream(fp)
        assert len(gedcom) == 10
        assert gedcom[1].tag == 'SUBM'
        assert gedcom.find('HEAD.GEDC.VERS')[0].value == '5.5.5'
        head = gedcom.find('HEAD')[0]
        assert head.find('GEDC.VERS')[0].value == '5.5.5'
        assert [item.tag for item in gedcom] == [
            'HEAD', 'SUBM', 'INDI', 'INDI', 'INDI', 'FAM', 'FAM', 'SOUR', 'REPO', 'TRLR'
        ]
