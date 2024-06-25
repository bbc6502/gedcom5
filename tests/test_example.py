from gedcom5.parser import GEDCOM5Parser


def test_example():
    msg = '\n'.join([
        '0 @I1@ INDI',
        '1 NAME Bob /BROWN/',
        '2 FAMC @F1@',
        '0 @F1@ FAM',
        '1 HUSB @I2@',
        '1 WIFE @I3@',
        '0 @I2@ INDI',
        '1 NAME Mary /BROWN/',
        '1 NAME Mary /MARTIN/',
        '0 @I3@ INDI',
        '1 NAME Mary /SMITH/',
    ])
    parser = GEDCOM5Parser()
    gedcom = parser.parse_string(msg)
    assert gedcom.indi[0].name[0].value == 'Bob /BROWN/'
    expected = ['1 NAME Bob /BROWN/', '1 NAME Mary /BROWN/', '1 NAME Mary /SMITH/']
    for index, indi in enumerate(gedcom.indi):
        assert f'{indi.name[0]}' == expected[index]
    assert f'{gedcom.indi[1].name[1]}' == '1 NAME Mary /MARTIN/'
    assert gedcom.indi[1].name[1].value == 'Mary /MARTIN/'
