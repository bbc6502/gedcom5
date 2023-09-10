from datetime import datetime
from typing import List, Optional, Union, Dict


class UnexpectedTag(RuntimeError):
    def __init__(self, tag, parent):
        super().__init__(f'Unexpected tag {tag} in {parent}')
        self.tag = tag
        self.parent = parent


class Tag:
    """Base GEDCOM Tag representation"""

    def __init__(self, level: Optional[int] = 0, parent: Optional['Tag'] = None, xref_id: str = None, tag: str = None, value: str = None):
        self.level = level
        self.parent = parent
        self.xref_id = xref_id
        self.tag = tag
        self.ref: Optional[Union[str, 'Tag']] = None
        if value is not None:
            if value.startswith('@') and value.endswith('@'):
                self.ref = value
        self.value = value
        self._items: List['Tag'] = []

    def __str__(self):
        out = f'{self.level}'
        if self.xref_id is not None:
            out = out + f' {self.xref_id}'
        out = out + f' {self.tag}'
        if self.value is not None:
            out = out + f' {self.value}'
        return out

    def __repr__(self):
        return str(self)

    def as_text(self):
        out = [str(self)]
        for item in self._items:
            out.append(item.as_text())
        return '\n'.join(out)

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return self._items.__iter__()

    def __getitem__(self, item: int) -> 'Tag':
        return self._items[item]

    def __setitem__(self, key: int, value: 'Tag'):
        self._items[key] = value

    def append(self, item: 'Tag'):
        self._items.append(item)

    def find(self, tags: str) -> List['Tag']:
        nodes = [self]
        for tag in tags.split('.'):
            nodes = [item for node in nodes for item in node._items if item.tag == tag]
        return nodes

    def find_first(self, tags:str, default=None) -> Optional['Tag']:
        nodes = self.find(tags)
        if len(nodes) > 0:
            return nodes[0]
        return default


class AddressStructure:
    def __init__(self):
        self.addr: Optional[ADDR] = None
        self.phon: List[PHON] = []
        self.email: List[EMAIL] = []
        self.fax: List[FAX] = []
        self.www: List[WWW] = []

    def append(self, item: Tag, strict=False):
        if isinstance(item, ADDR):
            self.addr = item
            return True
        elif isinstance(item, PHON):
            self.phon.append(item)
            return True
        elif isinstance(item, EMAIL):
            self.email.append(item)
            return True
        elif isinstance(item, FAX):
            self.fax.append(item)
            return True
        elif isinstance(item, WWW):
            self.www.append(item)
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class AssociationStructure:
    def __init__(self):
        self.asso: Optional[ASSO] = None

    def append(self, item: Tag, strict=False):
        if isinstance(item, ASSO):
            self.asso = item
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class ChangeDate:
    def __init__(self):
        self.chan: Optional[CHAN] = None

    def append(self, item: Tag, strict=False):
        if isinstance(item, CHAN):
            self.chan = item
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class ChildToFamilyLink:
    def __init__(self):
        self.famc: List[FAMC] = []

    def append(self, item: Tag, strict=False):
        if isinstance(item, FAMC):
            self.famc.append(item)
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class SpouseToFamilyLink:
    def __init__(self):
        self.fams: List[FAMS] = []

    def append(self, item: Tag, strict=False):
        if isinstance(item, FAMS):
            self.fams.append(item)
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class PlaceStructure:
    def __init__(self):
        self.plac: Optional[PLAC] = None

    def append(self, item: Tag, strict=False):
        if isinstance(item, PLAC):
            self.plac = item
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class MultimediaLink:
    def __init__(self):
        self.obje: List[OBJE] = []

    def append(self, item: Tag, strict=False):
        if isinstance(item, OBJE):
            self.obje.append(item)
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class NoteStructure:
    def __init__(self):
        self.note: List[NOTE] = []

    def append(self, item: Tag, strict=False):
        if isinstance(item, NOTE):
            self.note.append(item)
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class SourceCitation:
    def __init__(self):
        self.sour: List[SOUR] = []

    def append(self, item: Tag, strict=False):
        if isinstance(item, SOUR):
            self.sour.append(item)
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class EventDetail(PlaceStructure, AddressStructure, NoteStructure, SourceCitation, MultimediaLink):
    def __init__(self):
        PlaceStructure.__init__(self)
        AddressStructure.__init__(self)
        NoteStructure.__init__(self)
        SourceCitation.__init__(self)
        MultimediaLink.__init__(self)
        self.type: Optional[TYPE] = None
        self.date: Optional[DATE] = None
        self.agnc: Optional[AGNC] = None
        self.reli: Optional[RELI] = None
        self.caus: Optional[CAUS] = None
        self.resn: Optional[RESN] = None

    def append(self, item: Tag, strict=False):
        if isinstance(item, TYPE):
            self.type = item
            return True
        elif isinstance(item, DATE):
            self.date = item
            return True
        elif isinstance(item, AGNC):
            self.agnc = item
            return True
        elif isinstance(item, RELI):
            self.reli = item
            return True
        elif isinstance(item, CAUS):
            self.caus = item
            return True
        elif isinstance(item, RESN):
            self.resn = item
            return True
        else:
            if PlaceStructure.append(self, item):
                return True
            if AddressStructure.append(self, item):
                return True
            if NoteStructure.append(self, item):
                return True
            if SourceCitation.append(self, item):
                return True
            return MultimediaLink.append(self, item, strict)


class IndividualEventDetail(EventDetail):
    def __init__(self):
        EventDetail.__init__(self)
        self.age: Optional[AGE] = None

    def append(self, item: Tag, strict=False):
        if isinstance(item, AGE):
            self.age = item
            return True
        else:
            return EventDetail.append(self, item, strict)


class FamilyEventDetail(EventDetail):
    def __init__(self):
        EventDetail.__init__(self)
        self.husb: Optional[HUSB] = None
        self.wife: Optional[WIFE] = None

    def append(self, item: Tag, strict=False):
        if isinstance(item, HUSB):
            self.husb = item
            return True
        elif isinstance(item, WIFE):
            self.wife = item
            return True
        else:
            return EventDetail.append(self, item, strict)


class PersonalNamePieces(NoteStructure, SourceCitation):
    def __init__(self):
        NoteStructure.__init__(self)
        SourceCitation.__init__(self)
        self.npfx: Optional[NPFX] = None
        self.givn: Optional[GIVN] = None
        self.nick: Optional[NICK] = None
        self.spfx: Optional[SPFX] = None
        self.surn: Optional[SURN] = None
        self.nsfx: Optional[NSFX] = None

    def append(self, item: Tag, strict=False):
        if isinstance(item, NPFX):
            self.npfx = item
            return True
        elif isinstance(item, GIVN):
            self.givn = item
            return True
        elif isinstance(item, NICK):
            self.nick = item
            return True
        elif isinstance(item, SPFX):
            self.spfx = item
            return True
        elif isinstance(item, SURN):
            self.surn = item
            return True
        elif isinstance(item, NSFX):
            self.nsfx = item
            return True
        else:
            if NoteStructure.append(self, item):
                return True
            return SourceCitation.append(self, item, strict)


class PersonalNameStructure:
    def __init__(self):
        self.name: List[NAME] = []

    def append(self, item: Tag, strict=False):
        if isinstance(item, NAME):
            self.name.append(item)
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class IndividualEventStructure:
    def __init__(self):
        self.birt: List[BIRT] = []
        self.chr: List[CHR] = []
        self.deat: List[DEAT] = []
        self.buri: List[BURI] = []
        self.crem: List[CREM] = []
        self.adop: List[ADOP] = []
        self.bapm: List[BAPM] = []
        self.barm: List[BARM] = []
        self.basm: List[BASM] = []
        self.bles: List[BLES] = []
        self.chra: List[CHRA] = []
        self.conf: List[CONF] = []
        self.fcom: List[FCOM] = []
        self.ordn: List[ORDN] = []
        self.natu: List[NATU] = []
        self.emig: List[EMIG] = []
        self.immi: List[IMMI] = []
        self.cens: List[CENS] = []
        self.prob: List[PROB] = []
        self.will: List[WILL] = []
        self.grad: List[GRAD] = []
        self.reti: List[RETI] = []
        self.even: List[EVEN] = []

    def append(self, item: Tag, strict=False):
        if isinstance(item, BIRT):
            self.birt.append(item)
            return True
        elif isinstance(item, CHR):
            self.chr.append(item)
            return True
        elif isinstance(item, DEAT):
            self.deat.append(item)
            return True
        elif isinstance(item, BURI):
            self.buri.append(item)
            return True
        elif isinstance(item, CREM):
            self.crem.append(item)
            return True
        elif isinstance(item, ADOP):
            self.adop.append(item)
            return True
        elif isinstance(item, BAPM):
            self.bapm.append(item)
            return True
        elif isinstance(item, BARM):
            self.barm.append(item)
            return True
        elif isinstance(item, BASM):
            self.basm.append(item)
            return True
        elif isinstance(item, BLES):
            self.bles.append(item)
            return True
        elif isinstance(item, CHRA):
            self.chra.append(item)
            return True
        elif isinstance(item, CONF):
            self.conf.append(item)
            return True
        elif isinstance(item, FCOM):
            self.fcom.append(item)
            return True
        elif isinstance(item, ORDN):
            self.ordn.append(item)
            return True
        elif isinstance(item, NATU):
            self.natu.append(item)
            return True
        elif isinstance(item, EMIG):
            self.emig.append(item)
            return True
        elif isinstance(item, IMMI):
            self.immi.append(item)
            return True
        elif isinstance(item, CENS):
            self.cens.append(item)
            return True
        elif isinstance(item, PROB):
            self.prob.append(item)
            return True
        elif isinstance(item, WILL):
            self.will.append(item)
            return True
        elif isinstance(item, GRAD):
            self.grad.append(item)
            return True
        elif isinstance(item, RETI):
            self.reti.append(item)
            return True
        elif isinstance(item, EVEN):
            self.even.append(item)
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class IndividualAttributeStructure:
    def __init__(self):
        self.cast: List[CAST] = []
        self.dscr: List[DSCR] = []
        self.educ: List[EDUC] = []
        self.idno: List[IDNO] = []
        self.nati: List[NATI] = []
        self.nchi: List[NCHI] = []
        self.nmr: List[NMR] = []
        self.occu: List[OCCU] = []
        self.prop: List[PROP] = []
        self.reli: List[RELI] = []
        self.resi: List[RESI] = []
        self.ssn: List[SSN] = []
        self.titl: List[TITL] = []
        self.fact: List[FACT] = []

    def append(self, item: Tag, strict=False):
        if isinstance(item, CAST):
            self.cast.append(item)
            return True
        elif isinstance(item, DSCR):
            self.dscr.append(item)
            return True
        elif isinstance(item, EDUC):
            self.educ.append(item)
            return True
        elif isinstance(item, IDNO):
            self.idno.append(item)
            return True
        elif isinstance(item, NATI):
            self.nati.append(item)
            return True
        elif isinstance(item, NCHI):
            self.nchi.append(item)
            return True
        elif isinstance(item, NMR):
            self.nmr.append(item)
            return True
        elif isinstance(item, OCCU):
            self.occu.append(item)
            return True
        elif isinstance(item, PROP):
            self.prop.append(item)
            return True
        elif isinstance(item, RELI):
            self.reli.append(item)
            return True
        elif isinstance(item, RESI):
            self.resi.append(item)
            return True
        elif isinstance(item, SSN):
            self.ssn.append(item)
            return True
        elif isinstance(item, TITL):
            self.titl.append(item)
            return True
        elif isinstance(item, FACT):
            self.fact.append(item)
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class LDSIndividualOrdinance:
    def __init__(self):
        self.bapl: List[BAPL] = []
        self.conl: List[CONL] = []
        self.endl: List[ENDL] = []
        self.slgc: List[SLGC] = []

    def append(self, item: Tag, strict=False):
        if isinstance(item, BAPL):
            self.bapl.append(item)
            return True
        elif isinstance(item, CONL):
            self.conl.append(item)
            return True
        elif isinstance(item, ENDL):
            self.endl.append(item)
            return True
        elif isinstance(item, SLGC):
            self.slgc.append(item)
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class FamilyEventStructure:
    def __init__(self):
        self.anul: List[ANUL] = []
        self.cens: List[CENS] = []
        self.div: List[DIV] = []
        self.divf: List[DIVF] = []
        self.enga: List[ENGA] = []
        self.marb: List[MARB] = []
        self.marc: List[MARC] = []
        self.marr: List[MARR] = []
        self.marl: List[MARL] = []
        self.mars: List[MARS] = []
        self.resi: List[RESI] = []
        self.even: List[EVEN] = []

    def append(self, item: Tag, strict=False):
        if isinstance(item, ANUL):
            self.anul.append(item)
            return True
        elif isinstance(item, CENS):
            self.cens.append(item)
            return True
        elif isinstance(item, DIV):
            self.div.append(item)
            return True
        elif isinstance(item, DIVF):
            self.divf.append(item)
            return True
        elif isinstance(item, ENGA):
            self.enga.append(item)
            return True
        elif isinstance(item, MARB):
            self.marb.append(item)
            return True
        elif isinstance(item, MARC):
            self.marc.append(item)
            return True
        elif isinstance(item, MARR):
            self.marr.append(item)
            return True
        elif isinstance(item, MARL):
            self.marl.append(item)
            return True
        elif isinstance(item, MARS):
            self.mars.append(item)
            return True
        elif isinstance(item, RESI):
            self.resi.append(item)
            return True
        elif isinstance(item, EVEN):
            self.even.append(item)
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class LDSSpouseSealing:
    def __init__(self):
        self.seal: List[SLGS] = []

    def append(self, item: Tag, strict=False):
        if isinstance(item, SLGS):
            self.seal.append(item)
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class SourceRepositoryCitation:
    def __init__(self):
        self.repo: List[REPO] = []

    def append(self, item: Tag, strict=False):
        if isinstance(item, REPO):
            self.repo.append(item)
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class HEAD(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.sour: Optional[SOUR] = None
        self.dest: List[DEST] = []
        self.date: Optional[DATE] = None
        self.subm: Optional[SUBM] = None
        self.subn: Optional[SUBN] = None
        self.file: Optional[FILE] = None
        self.copr: Optional[COPR] = None
        self.gedc: Optional[GEDC] = None
        self.char: Optional[CHAR] = None
        self.lang: Optional[LANG] = None
        self.plac: Optional[PLAC] = None
        self.note: Optional[NOTE] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, SOUR):
            self.sour = item
            return True
        elif isinstance(item, DEST):
            self.dest.append(item)
            return True
        elif isinstance(item, DATE):
            self.date = item
            return True
        elif isinstance(item, SUBM):
            self.subm = item
            return True
        elif isinstance(item, SUBN):
            self.subn = item
            return True
        elif isinstance(item, FILE):
            self.file = item
            return True
        elif isinstance(item, COPR):
            self.copr = item
            return True
        elif isinstance(item, GEDC):
            self.gedc = item
            return True
        elif isinstance(item, CHAR):
            self.char = item
            return True
        elif isinstance(item, LANG):
            self.lang = item
            return True
        elif isinstance(item, PLAC):
            self.plac = item
            return True
        elif isinstance(item, NOTE):
            self.note = item
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class SOUR(Tag, SourceRepositoryCitation, ChangeDate, NoteStructure, MultimediaLink):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        SourceRepositoryCitation.__init__(self)
        ChangeDate.__init__(self)
        NoteStructure.__init__(self)
        MultimediaLink.__init__(self)
        self.vers: Optional[VERS] = None
        self.name: Optional[NAME] = None
        self.corp: Optional[CORP] = None
        self.data: Optional[DATA] = None
        self.page: Optional[PAGE] = None
        self.even: Optional[EVEN] = None
        self.quay: Optional[QUAY] = None
        self.lines: List[Union[CONT, CONC]] = []
        self.text: List[TEXT] = []
        self.auth: Optional[AUTH] = None
        self.titl: Optional[TITL] = None
        self.abbr: Optional[ABBR] = None
        self.publ: Optional[PUBL] = None
        self.refn: List[REFN] = []
        self.rin: Optional[RIN] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, VERS):
            self.vers = item
            return True
        elif isinstance(item, NAME):
            self.name = item
            return True
        elif isinstance(item, CORP):
            self.corp = item
            return True
        elif isinstance(item, DATA):
            self.data = item
            return True
        elif isinstance(item, PAGE):
            self.page = item
            return True
        elif isinstance(item, EVEN):
            self.even = item
            return True
        elif isinstance(item, QUAY):
            self.quay = item
            return True
        elif isinstance(item, CONT):
            self.lines.append(item)
            return True
        elif isinstance(item, CONC):
            self.lines.append(item)
            return True
        elif isinstance(item, TEXT):
            self.text.append(item)
            return True
        elif isinstance(item, AUTH):
            self.auth = item
            return True
        elif isinstance(item, TITL):
            self.titl = item
            return True
        elif isinstance(item, ABBR):
            self.abbr = item
            return True
        elif isinstance(item, PUBL):
            self.publ = item
            return True
        elif isinstance(item, REFN):
            self.refn.append(item)
            return True
        elif isinstance(item, RIN):
            self.rin = item
            return True
        else:
            if SourceRepositoryCitation.append(self, item):
                return True
            if ChangeDate.append(self, item):
                return True
            if NoteStructure.append(self, item):
                return True
            return MultimediaLink.append(self, item, strict)


class PAGE(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class VERS(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class NAME(Tag, PersonalNamePieces):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        PersonalNamePieces.__init__(self)
        self.type: Optional[TYPE] = None
        self.fone: List[FONE] = []
        self.romn: List[ROMN] = []

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, TYPE):
            self.type = item
            return True
        elif isinstance(item, FONE):
            self.fone.append(item)
            return True
        elif isinstance(item, ROMN):
            self.romn.append(item)
            return True
        else:
            return PersonalNamePieces.append(self, item, strict)


class CORP(Tag, AddressStructure):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        AddressStructure.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return AddressStructure.append(self, item, strict)


class DATA(Tag, NoteStructure):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        NoteStructure.__init__(self)
        self.date: Optional[DATE] = None
        self.copr: Optional[COPR] = None
        self.text: List[TEXT] = []
        self.even: List[EVEN] = []
        self.agnc: Optional[AGNC] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, DATE):
            self.date = item
            return True
        elif isinstance(item, COPR):
            self.copr = item
            return True
        elif isinstance(item, TEXT):
            self.text.append(item)
            return True
        elif isinstance(item, EVEN):
            self.even.append(item)
            return True
        elif isinstance(item, AGNC):
            self.agnc = item
            return True
        else:
            return NoteStructure.append(self, item, strict)


class DATE(Tag):
    def __init__(self, level: int, parent: Optional[Tag] = None, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.time: Optional[TIME] = None
        self.dates: Dict[str, datetime] = {}
        self._date: Optional[datetime] = None
        self._type: Optional[str] = None
        if value is not None:
            self._parse_dates(value)

    def _parse_dates(self, value: str):
        parts = value.upper().split(' ')
        if parts[0] in ('BEF', 'AFT', 'ABT', 'CAL', 'EST'):
            value = ' '.join(parts[1:])
            self._type = parts[0]
            self._date = self._parse_date(value)
            if self._date is not None:
                self.dates[self._type] = self._date
        elif parts[0] == 'FROM':
            ndx = parts.index('TO') if 'TO' in parts else -1
            if ndx > 0:
                value = ' '.join(parts[1:ndx])
                self._type = parts[0]
                self._date = self._parse_date(value)
                if self._date is not None:
                    self.dates[self._type] = self._date
                value = ' '.join(parts[ndx+1:])
                date = self._parse_date(value)
                if date is not None:
                    self.dates[parts[ndx]] = date
        elif parts[0] == 'BET':
            ndx = parts.index('AND') if 'AND' in parts else -1
            if ndx > 0:
                value = ' '.join(parts[1:ndx])
                self._type = parts[0]
                self._date = self._parse_date(value)
                if self._date is not None:
                    self.dates[self._type] = self._date
                value = ' '.join(parts[ndx+1:])
                date = self._parse_date(value)
                if date is not None:
                    self.dates[parts[ndx]] = date
        else:
            self._type = 'ACT'
            self._date = self._parse_date(value)
            if self._date is not None:
                self.dates[self._type] = self._date

    def _parse_date(self, value: str) -> Optional[datetime]:
        for fmt in [
            '%d %b %Y',
            '%d %b %y',
            '%b %Y',
            '%b %y',
            '%Y',
            '%y'
        ]:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                pass
        return None

    @property
    def type(self):
        return self._type

    @property
    def year(self):
        if self._date is None:
            return None
        return self._date.year

    @property
    def month(self):
        if self._date is None:
            return None
        return self._date.month

    @property
    def day(self):
        if self._date is None:
            return None
        return self._date.day

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, TIME):
            self.time = item
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class COPR(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.lines: List[Union[CONT, CONC]] = []

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, CONT):
            self.lines.append(item)
            return True
        elif isinstance(item, CONC):
            self.lines.append(item)
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class CONT(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class CONC(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class DEST(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class TIME(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class SUBM(Tag, AddressStructure, MultimediaLink, NoteStructure, ChangeDate):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        AddressStructure.__init__(self)
        MultimediaLink.__init__(self)
        NoteStructure.__init__(self)
        ChangeDate.__init__(self)
        self.name: Optional[NAME] = None
        self.lang: List[LANG] = []
        self.rfn: Optional[RFN] = None
        self.rin: Optional[RIN] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, NAME):
            self.name = item
            return True
        elif isinstance(item, LANG):
            self.lang.append(item)
            return True
        elif isinstance(item, RFN):
            self.rfn = item
            return True
        elif isinstance(item, RIN):
            self.rin = item
            return True
        else:
            if AddressStructure.append(self, item):
                return True
            if MultimediaLink.append(self, item):
                return True
            if NoteStructure.append(self, item):
                return True
            return ChangeDate.append(self, item, strict)


class SUBN(Tag, NoteStructure, ChangeDate):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        NoteStructure.__init__(self)
        ChangeDate.__init__(self)
        self.subm: Optional[SUBM] = None
        self.famf: Optional[FAMF] = None
        self.temp: Optional[TEMP] = None
        self.ance: Optional[ANCE] = None
        self.desc: Optional[DESC] = None
        self.ordi: Optional[ORDI] = None
        self.rin: Optional[RIN] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, SUBM):
            self.subm = item
            return True
        elif isinstance(item, FAMF):
            self.famf = item
            return True
        elif isinstance(item, TEMP):
            self.temp = item
            return True
        elif isinstance(item, ANCE):
            self.ance = item
            return True
        elif isinstance(item, DESC):
            self.desc = item
            return True
        elif isinstance(item, ORDI):
            self.ordi = item
            return True
        elif isinstance(item, RIN):
            self.rin = item
            return True
        else:
            if NoteStructure.append(self, item):
                return True
            return ChangeDate.append(self, item, strict)


class FILE(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.form: Optional[FORM] = None
        self.titl: Optional[TITL] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, FORM):
            self.form = item
            return True
        elif isinstance(item, TITL):
            self.titl = item
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class GEDC(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.vers: Optional[VERS] = None
        self.form: Optional[FORM] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, VERS):
            self.vers = item
            return True
        elif isinstance(item, FORM):
            self.form = item
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class FORM(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.medi: Optional[MEDI] = None
        self.type: Optional[TYPE] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, MEDI):
            self.medi = item
            return True
        elif isinstance(item, TYPE):
            self.type = item
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class CHAR(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.vers: Optional[VERS] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, VERS):
            self.vers = item
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class LANG(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class ANCE(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class DESC(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class PLAC(Tag, NoteStructure):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        NoteStructure.__init__(self)
        self.form: Optional[FORM] = None
        self.fone: List[FONE] = []
        self.romn: List[ROMN] = []
        self.map: Optional[MAP] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, FORM):
            self.form = item
            return True
        elif isinstance(item, FONE):
            self.fone.append(item)
            return True
        elif isinstance(item, ROMN):
            self.romn.append(item)
            return True
        elif isinstance(item, MAP):
            self.map = item
            return True
        else:
            return NoteStructure.append(self, item, strict)


class NOTE(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.lines: List[Union[CONT, CONC]] = []
        self.refn: List[REFN] = []
        self.rin: Optional[RIN] = None
        self.sour: List[SOUR] = []
        self.chan: Optional[CHAN] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, CONT):
            self.lines.append(item)
            return True
        elif isinstance(item, CONC):
            self.lines.append(item)
            return True
        elif isinstance(item, REFN):
            self.refn.append(item)
            return True
        elif isinstance(item, RIN):
            self.rin = item
            return True
        elif isinstance(item, SOUR):
            self.sour.append(item)
            return True
        elif isinstance(item, CHAN):
            self.chan = item
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class FAM(Tag, FamilyEventStructure, LDSSpouseSealing, ChangeDate, NoteStructure, SourceCitation, MultimediaLink):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        FamilyEventStructure.__init__(self)
        LDSSpouseSealing.__init__(self)
        ChangeDate.__init__(self)
        NoteStructure.__init__(self)
        SourceCitation.__init__(self)
        MultimediaLink.__init__(self)
        self.resn: Optional[RESN] = None
        self.husb: Optional[HUSB] = None
        self.wife: Optional[WIFE] = None
        self.chil: List[CHIL] = []
        self.nchi: Optional[NCHI] = None
        self.subm: List[SUBM] = []
        self.refn: List[REFN] = []
        self.rin: Optional[RIN] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, RESN):
            self.resn = item
            return True
        elif isinstance(item, HUSB):
            self.husb = item
            return True
        elif isinstance(item, WIFE):
            self.wife = item
            return True
        elif isinstance(item, CHIL):
            self.chil.append(item)
            return True
        elif isinstance(item, NCHI):
            self.nchi = item
            return True
        elif isinstance(item, SUBM):
            self.subm.append(item)
            return True
        elif isinstance(item, REFN):
            self.refn.append(item)
            return True
        elif isinstance(item, RIN):
            self.rin = item
            return True
        else:
            if FamilyEventStructure.append(self, item):
                return True
            if LDSSpouseSealing.append(self, item):
                return True
            if ChangeDate.append(self, item):
                return True
            if NoteStructure.append(self, item):
                return True
            if SourceCitation.append(self, item):
                return True
            return MultimediaLink.append(self, item, strict)


class RESN(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class HUSB(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.age: Optional[AGE] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, AGE):
            self.age = item
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class WIFE(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.age: Optional[AGE] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, AGE):
            self.age = item
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class CHIL(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class NCHI(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class REFN(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.type: Optional[TYPE] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, TYPE):
            self.type = item
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class TYPE(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class RIN(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class INDI(Tag, PersonalNameStructure, IndividualEventStructure, IndividualAttributeStructure, LDSIndividualOrdinance, ChildToFamilyLink, SpouseToFamilyLink, AssociationStructure, ChangeDate, NoteStructure, SourceCitation, MultimediaLink):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        PersonalNameStructure.__init__(self)
        IndividualEventStructure.__init__(self)
        IndividualAttributeStructure.__init__(self)
        LDSIndividualOrdinance.__init__(self)
        ChildToFamilyLink.__init__(self)
        SpouseToFamilyLink.__init__(self)
        AssociationStructure.__init__(self)
        ChangeDate.__init__(self)
        NoteStructure.__init__(self)
        SourceCitation.__init__(self)
        MultimediaLink.__init__(self)
        self.resn: Optional[RESN] = None
        self.sex: Optional[SEX] = None
        self.subm: List[SUBM] = []
        self.alia: List[ALIA] = []
        self.anci: List[ANCI] = []
        self.desi: List[DESI] = []
        self.rfn: Optional[RFN] = None
        self.afn: Optional[AFN] = None
        self.refn: List[REFN] = []
        self.rin: Optional[RIN] = None

    def is_private(self):
        year_minus_100 = datetime.now().year - 100
        year_minus_60 = year_minus_100 + 40
        year_minus_140 = year_minus_100 - 40
        if 0 < self.birth_year() <= year_minus_100:
            return False
        if datetime.now().year - 100 < self.birth_year():
            return True
        if 0 < self.death_year() <= year_minus_60:
            return False
        if self.birth_year() == 0 and self.death_year() == 0:
            for famc in self.famc:
                if isinstance(famc.ref, FAM):
                    if famc.ref.husb is not None and isinstance(famc.ref.husb.ref, INDI):
                        if famc.ref.husb.ref.is_private():
                            return True
                        if 0 < famc.ref.husb.ref.birth_year() <= year_minus_140:
                            return False
                        if 0 < famc.ref.husb.ref.death_year() <= year_minus_100:
                            return False
                    if famc.ref.wife is not None and isinstance(famc.ref.wife.ref, INDI):
                        if famc.ref.wife.ref.is_private():
                            return True
                        if 0 < famc.ref.wife.ref.birth_year() <= year_minus_140:
                            return False
                        if 0 < famc.ref.wife.ref.death_year() <= year_minus_100:
                            return False
        return True

    def birth_year(self) -> int:
        for birt in self.birt:
            if birt.date is not None and birt.date.year is not None:
                return birt.date.year
        for bapm in self.bapm:
            if bapm.date is not None and bapm.date.year is not None:
                return bapm.date.year
        for chr in self.chr:
            if chr.date is not None and chr.date.year is not None:
                return chr.date.year
        return 0

    def death_year(self) -> int:
        for deat in self.deat:
            if deat.date is not None and deat.date.year is not None:
                return deat.date.year
        for buri in self.buri:
            if buri.date is not None and buri.date.year is not None:
                return buri.date.year
        for crem in self.crem:
            if crem.date is not None and crem.date.year is not None:
                return crem.date.year
        return 0

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, RESN):
            self.resn = item
            return True
        elif isinstance(item, SEX):
            self.sex = None
            return True
        elif isinstance(item, SUBM):
            self.subm.append(item)
            return True
        elif isinstance(item, ALIA):
            self.alia.append(item)
            return True
        elif isinstance(item, ANCI):
            self.anci.append(item)
            return True
        elif isinstance(item, DESI):
            self.desi.append(item)
            return True
        elif isinstance(item, RFN):
            self.rfn = item
            return True
        elif isinstance(item, AFN):
            self.afn = item
            return True
        elif isinstance(item, REFN):
            self.refn.append(item)
            return True
        elif isinstance(item, RIN):
            self.rin = item
            return True
        else:
            if PersonalNameStructure.append(self, item):
                return True
            if IndividualEventStructure.append(self, item):
                return True
            if IndividualAttributeStructure.append(self, item):
                return True
            if LDSIndividualOrdinance.append(self, item):
                return True
            if ChildToFamilyLink.append(self, item):
                return True
            if SpouseToFamilyLink.append(self, item):
                return True
            if AssociationStructure.append(self, item):
                return True
            if ChangeDate.append(self, item):
                return True
            if NoteStructure.append(self, item):
                return True
            if SourceCitation.append(self, item):
                return True
            return MultimediaLink.append(self, item, strict)


class SEX(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class ALIA(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class ANCI(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class DESI(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class RFN(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class AFN(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class OBJE(Tag, NoteStructure, SourceCitation, ChangeDate):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        NoteStructure.__init__(self)
        SourceCitation.__init__(self)
        ChangeDate.__init__(self)
        self.file: List[FILE] = []
        self.titl: Optional[TITL] = None
        self.refn: List[REFN] = []
        self.rin: Optional[RIN] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, FILE):
            self.file.append(item)
            return True
        elif isinstance(item, TITL):
            self.titl = item
            return True
        elif isinstance(item, REFN):
            self.refn.append(item)
            return True
        elif isinstance(item, RIN):
            self.rin = item
            return True
        else:
            if NoteStructure.append(self, item):
                return True
            if SourceCitation.append(self, item):
                return True
            return ChangeDate.append(self, item, strict)


class TITL(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)
        self.text: List[Union[CONC,CONT]] = []

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, CONC):
            self.text.append(item)
            return True
        elif isinstance(item, CONT):
            self.text.append(item)
            return True
        return IndividualEventDetail.append(self, item, strict)


class REPO(Tag, AddressStructure, NoteStructure, ChangeDate):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        AddressStructure.__init__(self)
        NoteStructure.__init__(self)
        ChangeDate.__init__(self)
        self.name: Optional[NAME] = None
        self.refn: List[REFN] = []
        self.rin: Optional[RIN] = None
        self.chan: Optional[CHAN] = None
        self.caln: Optional[CALN] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, NAME):
            self.name = item
            return True
        elif isinstance(item, REFN):
            self.refn.append(item)
            return True
        elif isinstance(item, RIN):
            self.rin = item
            return True
        elif isinstance(item, CALN):
            self.caln = item
            return True
        else:
            if AddressStructure.append(self, item):
                return True
            if NoteStructure.append(self, item):
                return True
            return ChangeDate.append(self, item, strict)


class EVEN(Tag, FamilyEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        FamilyEventDetail.__init__(self)
        self.role: Optional[ROLE] = None
        self.date: Optional[DATE] = None
        self.plac: Optional[PLAC] = None
        self.age: Optional[AGE] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, ROLE):
            self.role = item
            return True
        elif isinstance(item, DATE):
            self.date = item
            return True
        elif isinstance(item, PLAC):
            self.plac = item
            return True
        elif isinstance(item, AGE):
            self.age = item
            return True
        else:
            return FamilyEventDetail.append(self, item, strict)


class AGNC(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class AUTH(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.text: List[Union[CONC,CONT]] = []

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, CONC):
            self.text.append(item)
            return True
        elif isinstance(item, CONT):
            self.text.append(item)
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class ABBR(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class PUBL(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.text: List[Union[CONC,CONT]] = []

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, CONC):
            self.text.append(item)
            return True
        elif isinstance(item, CONT):
            self.text.append(item)
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class TEXT(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.lines: List[Union[CONT, CONC]] = []

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, CONT):
            self.lines.append(item)
            return True
        elif isinstance(item, CONC):
            self.lines.append(item)
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class FAMF(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class TEMP(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class ORDI(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class ADDR(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.cont: List[CONT] = []
        self.adr1: Optional[ADR1] = None
        self.adr2: Optional[ADR2] = None
        self.adr3: Optional[ADR3] = None
        self.city: Optional[CITY] = None
        self.stae: Optional[STAE] = None
        self.post: Optional[POST] = None
        self.ctry: Optional[CTRY] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, CONT):
            self.cont.append(item)
            return True
        elif isinstance(item, ADR1):
            self.adr1 = item
            return True
        elif isinstance(item, ADR2):
            self.adr2 = item
            return True
        elif isinstance(item, ADR3):
            self.adr3 = item
            return True
        elif isinstance(item, CITY):
            self.city = item
            return True
        elif isinstance(item, STAE):
            self.stae = item
            return True
        elif isinstance(item, POST):
            self.post = item
            return True
        elif isinstance(item, CTRY):
            self.ctry = item
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class ADR1(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class ADR2(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class ADR3(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class CITY(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class STAE(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class POST(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class CTRY(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class PHON(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class EMAIL(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class FAX(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class WWW(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class ASSO(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.rela: Optional[RELA] = None
        self.sour: List[SOUR] = []
        self.note: List[NOTE] = []

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, RELA):
            self.rela = item
            return True
        elif isinstance(item, SOUR):
            self.sour.append(item)
            return True
        elif isinstance(item, NOTE):
            self.note.append(item)
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class RELA(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class CHAN(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.date: Optional[DATE] = None
        self.note: List[NOTE] = []

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, DATE):
            self.date = item
            return True
        elif isinstance(item, NOTE):
            self.note.append(item)
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class FAMC(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.pedi: Optional[PEDI] = None
        self.stat: Optional[STAT] = None
        self.adop: Optional[ADOP] = None
        self.note: List[NOTE] = []

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, PEDI):
            self.pedi = item
            return True
        elif isinstance(item, STAT):
            self.stat = item
            return True
        elif isinstance(item, ADOP):
            self.adop = item
            return True
        elif isinstance(item, NOTE):
            self.note.append(item)
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class FAMS(Tag, NoteStructure):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        NoteStructure.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return NoteStructure.append(self, item, strict)


class PEDI(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class STAT(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.date: Optional[DATE] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, DATE):
            self.date = item
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class CAUS(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class ANUL(Tag, FamilyEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        FamilyEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return FamilyEventDetail.append(self, item, strict)


class CENS(Tag, IndividualEventDetail, FamilyEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)
        FamilyEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if IndividualEventDetail.append(self, item):
            return True
        return FamilyEventDetail.append(self, item, strict)


class DIV(Tag, FamilyEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        FamilyEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return FamilyEventDetail.append(self, item, strict)


class DIVF(Tag, FamilyEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        FamilyEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return FamilyEventDetail.append(self, item, strict)


class ENGA(Tag, FamilyEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        FamilyEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return FamilyEventDetail.append(self, item, strict)


class MARB(Tag, FamilyEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        FamilyEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return FamilyEventDetail.append(self, item, strict)


class MARC(Tag, FamilyEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        FamilyEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return FamilyEventDetail.append(self, item, strict)


class MARR(Tag, FamilyEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        FamilyEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return FamilyEventDetail.append(self, item, strict)


class MARL(Tag, FamilyEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        FamilyEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return FamilyEventDetail.append(self, item, strict)


class MARS(Tag, FamilyEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        FamilyEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return FamilyEventDetail.append(self, item, strict)


class RELI(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class CAST(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class DSCR(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.text: List[Union[CONC,CONT]] = []
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, CONC):
            self.text.append(item)
            return True
        elif isinstance(item, CONT):
            self.text.append(item)
            return True
        return IndividualEventDetail.append(self, item, strict)


class EDUC(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class IDNO(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class NATI(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class NMR(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class OCCU(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class PROP(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class RESI(Tag, IndividualEventDetail, FamilyEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)
        FamilyEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if IndividualEventDetail.append(self, item):
            return True
        return FamilyEventDetail.append(self, item, strict)


class SSN(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class FACT(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class AGE(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class BIRT(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)
        self.famc: Optional[FAMC] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, FAMC):
            self.famc = item
            return True
        else:
            return IndividualEventDetail.append(self, item, strict)


class CHR(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)
        self.famc: Optional[FAMC] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, FAMC):
            self.famc = item
            return True
        else:
            return IndividualEventDetail.append(self, item, strict)


class DEAT(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class BURI(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class CREM(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class ADOP(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)
        self.famc: Optional[FAMC] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, FAMC):
            self.famc = item
            return True
        else:
            return IndividualEventDetail.append(self, item, strict)


class BAPM(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class BARM(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class BASM(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class BLES(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class CHRA(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class CONF(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class FCOM(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class ORDN(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class NATU(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class EMIG(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class IMMI(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class PROB(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class WILL(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)

class GRAD(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)

class RETI(Tag, IndividualEventDetail):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        IndividualEventDetail.__init__(self)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        return IndividualEventDetail.append(self, item, strict)


class BAPL(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.date: Optional[DATE] = None
        self.temp: Optional[TEMP] = None
        self.plac: Optional[PLAC] = None
        self.stat: Optional[STAT] = None
        self.note: List[NOTE] = []
        self.sour: List[SOUR] = []

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, DATE):
            self.date = item
            return True
        elif isinstance(item, TEMP):
            self.temp = item
            return True
        elif isinstance(item, PLAC):
            self.plac = item
            return True
        elif isinstance(item, STAT):
            self.stat = item
            return True
        elif isinstance(item, NOTE):
            self.note.append(item)
            return True
        elif isinstance(item, SOUR):
            self.sour.append(item)
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class CONL(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.date: Optional[DATE] = None
        self.temp: Optional[TEMP] = None
        self.plac: Optional[PLAC] = None
        self.stat: Optional[STAT] = None
        self.note: List[NOTE] = []
        self.sour: List[SOUR] = []

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, DATE):
            self.date = item
            return True
        elif isinstance(item, TEMP):
            self.temp = item
            return True
        elif isinstance(item, PLAC):
            self.plac = item
            return True
        elif isinstance(item, STAT):
            self.stat = item
            return True
        elif isinstance(item, NOTE):
            self.note.append(item)
            return True
        elif isinstance(item, SOUR):
            self.sour.append(item)
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class ENDL(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.date: Optional[DATE] = None
        self.temp: Optional[TEMP] = None
        self.plac: Optional[PLAC] = None
        self.stat: Optional[STAT] = None
        self.note: List[NOTE] = []
        self.sour: List[SOUR] = []

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, DATE):
            self.date = item
            return True
        elif isinstance(item, TEMP):
            self.temp = item
            return True
        elif isinstance(item, PLAC):
            self.plac = item
            return True
        elif isinstance(item, STAT):
            self.stat = item
            return True
        elif isinstance(item, NOTE):
            self.note.append(item)
            return True
        elif isinstance(item, SOUR):
            self.sour.append(item)
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class SLGC(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.date: Optional[DATE] = None
        self.temp: Optional[TEMP] = None
        self.plac: Optional[PLAC] = None
        self.famc: Optional[FAMC] = None
        self.stat: Optional[STAT] = None
        self.note: List[NOTE] = []
        self.sour: List[SOUR] = []

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, DATE):
            self.date = item
            return True
        elif isinstance(item, TEMP):
            self.temp = item
            return True
        elif isinstance(item, PLAC):
            self.plac = item
            return True
        elif isinstance(item, FAMC):
            self.famc = item
            return True
        elif isinstance(item, STAT):
            self.stat = item
            return True
        elif isinstance(item, NOTE):
            self.note.append(item)
            return True
        elif isinstance(item, SOUR):
            self.sour.append(item)
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class SLGS(Tag, NoteStructure, SourceCitation):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        NoteStructure.__init__(self)
        SourceCitation.__init__(self)
        self.date: Optional[DATE] = None
        self.temp: Optional[TEMP] = None
        self.plac: Optional[PLAC] = None
        self.stat: Optional[STAT] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, DATE):
            self.date = item
            return True
        elif isinstance(item, TEMP):
            self.temp = item
            return True
        elif isinstance(item, PLAC):
            self.plac = item
            return True
        elif isinstance(item, STAT):
            self.stat = item
            return True
        elif NoteStructure.append(self, item):
            return True
        else:
            return SourceCitation.append(self, item, strict)


class MEDI(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class NPFX(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class GIVN(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class NICK(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class SPFX(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class SURN(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class NSFX(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class FONE(Tag, PersonalNamePieces):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        PersonalNamePieces.__init__(self)
        self.type: Optional[TYPE] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, TYPE):
            self.type = item
            return True
        else:
            return PersonalNamePieces.append(self, item, strict)


class ROMN(Tag, PersonalNamePieces):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        PersonalNamePieces.__init__(self)
        self.type: Optional[TYPE] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, TYPE):
            self.type = item
            return True
        else:
            return PersonalNamePieces.append(self, item, strict)


class MAP(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.lati: Optional[LATI] = None
        self.long: Optional[LONG] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, LATI):
            self.lati = item
            return True
        elif isinstance(item, LONG):
            self.long = item
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False


class LATI(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class LONG(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class ROLE(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class QUAY(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if strict:
            raise UnexpectedTag(item, self)
        return False


class CALN(Tag):
    def __init__(self, level: int, parent: Tag, xref_id: str = None, value: str = None):
        Tag.__init__(self, level, parent, xref_id, self.__class__.__name__, value)
        self.medi: Optional[MEDI] = None

    def append(self, item: Tag, strict=False):
        Tag.append(self, item)
        if isinstance(item, MEDI):
            self.medi = item
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False
