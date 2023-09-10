def note_structure(level):
    if level>5:
        return []
    return [
        f'{level} NOTE',
        f'{level + 1} CONC',
        f'{level + 1} CONT',
        f'{level + 1} CONC',
        f'{level + 1} CONT',
    ]


def place_structure(level):
    return [
        f'{level} PLAC',
        f'{level+1} FORM',
        f'{level+1} FONE',
        f'{level+2} TYPE',
        f'{level+1} ROMN',
        f'{level+2} TYPE',
        f'{level+1} MAP',
        f'{level+2} LATI',
        f'{level+2} LONG',
        *note_structure(level + 1),
        *note_structure(level + 1),
    ]


def address_structure(level):
    return [
        f'{level} ADDR',
        f'{level+1} CONT',
        f'{level+1} ADR1',
        f'{level+1} ADR2',
        f'{level+1} ADR3',
        f'{level+1} CITY',
        f'{level+1} STAE',
        f'{level+1} POST',
        f'{level+1} CTRY',
        f'{level} PHON',
        f'{level} PHON',
        f'{level} PHON',
        f'{level} EMAIL',
        f'{level} EMAIL',
        f'{level} EMAIL',
        f'{level} FAX',
        f'{level} FAX',
        f'{level} FAX',
        f'{level} WWW',
        f'{level} WWW',
        f'{level} WWW',
    ]


def change_date(level):
    if level>5:
        return []
    return [
        f'{level} CHAN',
        f'{level+1} DATE',
        f'{level+2} TIME',
        *note_structure(level + 1),
        *note_structure(level + 1),
    ]


def multimedia_link(level):
    if level>5:
        return []
    return [
        f'{level} OBJE',
        f'{level+1} FILE',
        f'{level+2} FORM',
        f'{level+3} TYPE',
        f'{level+2} TITL',
        f'{level+1} REFN',
        f'{level+2} TYPE',
        f'{level+1} RIN',
        *note_structure(level + 1),
        *note_structure(level + 1),
        *source_citation(level+1),
        *source_citation(level+1),
        *change_date(level + 1),
    ]


def source_citation(level):
    if level>5:
        return []
    return [
        f'{level} SOUR',
        f'{level+1} PAGE',
        f'{level+1} EVEN',
        f'{level+2} ROLE',
        f'{level+1} DATA',
        f'{level+2} DATE',
        f'{level+2} TEXT',
        f'{level+3} CONC',
        f'{level+3} CONT',
        f'{level+3} CONC',
        f'{level+3} CONT',
        *multimedia_link(level + 1),
        *multimedia_link(level + 1),
        *note_structure(level + 1),
        *note_structure(level + 1),
        f'{level+1} QUAY',
    ]


def event_detail(level):
    return [
        f'{level} TYPE',
        f'{level} DATE',
        *place_structure(level),
        *address_structure(level),
        f'{level} AGNC',
        f'{level} RELI',
        f'{level} CAUS',
        f'{level} RESN',
        *note_structure(level),
        *note_structure(level),
        *source_citation(level),
        *source_citation(level),
        *multimedia_link(level),
        *multimedia_link(level),
    ]


def family_event_detail(level):
    return [
        f'{level} HUSB',
        f'{level+1} AGE',
        f'{level} WIFE',
        f'{level+1} AGE',
        *event_detail(level)
    ]


def family_event_structure(level):
    return [
        f'{level} ANUL',
        *family_event_detail(level + 1),
        f'{level} CENS',
        *family_event_detail(level + 1),
        f'{level} DIV',
        *family_event_detail(level + 1),
        f'{level} DIVF',
        *family_event_detail(level + 1),
        f'{level} ENGA',
        *family_event_detail(level + 1),
        f'{level} MARB',
        *family_event_detail(level + 1),
        f'{level} MARC',
        *family_event_detail(level + 1),
        f'{level} MARR',
        *family_event_detail(level + 1),
        f'{level} MARL',
        *family_event_detail(level + 1),
        f'{level} MARS',
        *family_event_detail(level + 1),
        f'{level} RESI',
        *family_event_detail(level + 1),
        f'{level} EVEN',
        *family_event_detail(level + 1),
    ]


def lds_spouse_sealing(level):
    return [
        f'{level} SLGS',
        f'{level+1} DATE',
        f'{level+1} TEMP',
        f'{level+1} PLAC',
        f'{level+1} STAT',
        f'{level+2} DATE',
        *note_structure(level + 1),
        *note_structure(level + 1),
        *source_citation(level + 1),
        *source_citation(level + 1),
    ]


def personal_name_pieces(level):
    return [
        f'{level} NPFX',
        f'{level} GIVN',
        f'{level} NICK',
        f'{level} SPFX',
        f'{level} SURN',
        f'{level} NSFX',
        *note_structure(level),
        *note_structure(level),
        *source_citation(level),
        *source_citation(level),
    ]


def personal_name_structure(level):
    return [
        f'{level} NAME',
        f'{level+1} TYPE',
        *personal_name_pieces(level + 1),
        f'{level+1} FONE',
        f'{level+2} TYPE',
        *personal_name_pieces(level + 2),
        f'{level+1} ROMN',
        f'{level+2} TYPE',
        *personal_name_pieces(level + 2),
    ]


def individual_event_detail(level):
    return [
        *event_detail(level),
        f'{level} AGE',
    ]


def individual_event_structure(level):
    return [
        f'{level} BIRT',
        *individual_event_detail(level + 1),
        f'{level+1} FAMC',
        f'{level} CHR',
        *individual_event_detail(level + 1),
        f'{level+1} FAMC',
        f'{level} DEAT',
        *individual_event_detail(level + 1),
        f'{level} BURI',
        *individual_event_detail(level + 1),
        f'{level} CREM',
        *individual_event_detail(level + 1),
        f'{level} ADOP',
        *individual_event_detail(level + 1),
        f'{level+1} FAMC',
        f'{level+2} ADOP',
        f'{level} BAPM',
        *individual_event_detail(level + 1),
        f'{level} BARM',
        *individual_event_detail(level + 1),
        f'{level} BASM',
        *individual_event_detail(level + 1),
        f'{level} BLES',
        *individual_event_detail(level + 1),
        f'{level} CHRA',
        *individual_event_detail(level + 1),
        f'{level} CONF',
        *individual_event_detail(level + 1),
        f'{level} FCOM',
        *individual_event_detail(level + 1),
        f'{level} ORDN',
        *individual_event_detail(level + 1),
        f'{level} NATU',
        *individual_event_detail(level + 1),
        f'{level} EMIG',
        *individual_event_detail(level + 1),
        f'{level} IMMI',
        *individual_event_detail(level + 1),
        f'{level} CENS',
        *individual_event_detail(level + 1),
        f'{level} PROB',
        *individual_event_detail(level + 1),
        f'{level} WILL',
        *individual_event_detail(level + 1),
        f'{level} GRAD',
        *individual_event_detail(level + 1),
        f'{level} RETI',
        *individual_event_detail(level + 1),
        f'{level} EVEN',
        *individual_event_detail(level + 1),
    ]


def individual_attribute_structure(level):
    return [
        f'{level} CAST',
        *individual_event_detail(level+1),
        f'{level} DSCR',
        f'{level+1} CONC',
        f'{level+1} CONT',
        *individual_event_detail(level + 1),
        f'{level} EDUC',
        *individual_event_detail(level + 1),
        f'{level} IDNO',
        *individual_event_detail(level + 1),
        f'{level} NATI',
        *individual_event_detail(level + 1),
        f'{level} NCHI',
        *individual_event_detail(level + 1),
        f'{level} NMR',
        *individual_event_detail(level + 1),
        f'{level} OCCU',
        *individual_event_detail(level + 1),
        f'{level} PROP',
        *individual_event_detail(level + 1),
        f'{level} RELI',
        *individual_event_detail(level + 1),
        f'{level} RESI',
        *individual_event_detail(level + 1),
        f'{level} SSN',
        *individual_event_detail(level + 1),
        f'{level} TITL',
        *individual_event_detail(level + 1),
        f'{level} FACT',
        *individual_event_detail(level + 1),
    ]


def lds_individual_ordinance(level):
    return [
        f'{level} BAPL',
        f'{level+1} DATE',
        f'{level+1} TEMP',
        f'{level+1} PLAC',
        f'{level+1} STAT',
        f'{level+2} DATE',
        *note_structure(level+1),
        *note_structure(level+1),
        *source_citation(level+1),
        *source_citation(level+1),
        f'{level} CONL',
        f'{level+1} DATE',
        f'{level+1} TEMP',
        f'{level+1} PLAC',
        f'{level+1} STAT',
        f'{level+2} DATE',
        *note_structure(level+1),
        *note_structure(level+1),
        *source_citation(level+1),
        *source_citation(level+1),
        f'{level} ENDL',
        f'{level+1} DATE',
        f'{level+1} TEMP',
        f'{level+1} PLAC',
        f'{level+1} STAT',
        f'{level+2} DATE',
        *note_structure(level+1),
        *note_structure(level+1),
        *source_citation(level+1),
        *source_citation(level+1),
        f'{level} SLGC',
        f'{level + 1} DATE',
        f'{level + 1} TEMP',
        f'{level + 1} PLAC',
        f'{level + 1} FAMC',
        f'{level + 1} STAT',
        f'{level + 2} DATE',
        *note_structure(level + 1),
        *note_structure(level + 1),
        *source_citation(level + 1),
        *source_citation(level + 1),
    ]


def child_to_family_link(level):
    return [
        f'{level} FAMC',
        f'{level+1} PEDI',
        f'{level+1} STAT',
        *note_structure(level+1),
        *note_structure(level+1),
    ]


def spouse_to_family_link(level):
    return [
        f'{level} FAMS',
        *note_structure(level+1),
        *note_structure(level+1),
    ]


def association_structure(level):
    return [
        f'{level} ASSO',
        f'{level+1} RELA',
        *source_citation(level+1),
        *source_citation(level+1),
        *note_structure(level+1),
        *note_structure(level+1),
    ]


def source_repository_citation(level):
    return [
        f'{level} REPO',
        *note_structure(level+1),
        *note_structure(level+1),
        f'{level+1} CALN',
        f'{level+2} MEDI',
        f'{level+1} CALN',
        f'{level+2} MEDI',
    ]
