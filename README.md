# GEDCOM v5

Parser for GEDCOM v5 files

## Specifications

https://www.gedcom.org/gedcom.html

## Samples

https://www.gedcom.org/samples.html

## Usage Example

    from gedcom5.parser import GEDCOM5Parser

    msg = '\n'.join([
        '0 @I1@ INDI',
        '1 NAME Bob /BROWN/',
        '2 FAMC @F1@',
        '0 @F1@ FAM',
        '1 HUSB @I2@',
        '1 WIFE @I3@',
        '0 @I2@ INDI',
        '1 NAME Bob /BROWN/'
        '0 @I3@ INDI',
        '1 NAME Mary /SMITH/'
    ])
    parser = GEDCOM5Parser()
    gedcom = parser.parse_string(msg)
    gedcom.indi[0].name.value == 'Bob /BROWN/'
    for indi in gedcom.indi:
        print(f'{indi.name.value}')
