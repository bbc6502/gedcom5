from typing import BinaryIO, Optional
from gedcom5.gedcom import GEDCOM
from gedcom5.tag import Tag, HEAD, SOUR, VERS, NAME, CORP, DATA, DATE, COPR, CONT, CONC, DEST, TIME, SUBM, SUBN, FILE, \
    GEDC, FORM, CHAR, LANG, PLAC, NOTE, FAM, RESN, HUSB, WIFE, CHIL, NCHI, REFN, TYPE, RIN, INDI, SEX, ALIA, ANCI, DESI, \
    RFN, AFN, OBJE, TITL, REPO, EVEN, AGNC, AUTH, ABBR, PUBL, TEXT, FAMF, TEMP, ORDI, ADDR, ADR1, ADR2, ADR3, CITY, \
    STAE, POST, CTRY, PHON, EMAIL, FAX, WWW, ASSO, RELA, CHAN, FAMC, PEDI, STAT, RELI, CAUS, ANUL, CENS, DIV, DIVF, \
    ENGA, MARB, MARC, MARR, MARL, MARS, CAST, DSCR, EDUC, IDNO, NATI, NMR, OCCU, PROP, RESI, SSN, FACT, AGE, BIRT, CHR, \
    DEAT, BURI, CREM, ADOP, BAPM, BARM, BASM, BLES, CHRA, CONF, FCOM, ORDN, NATU, EMIG, IMMI, PROB, WILL, GRAD, RETI, \
    BAPL, CONL, ENDL, SLGC, SLGS, MEDI, NPFX, GIVN, NICK, SPFX, SURN, NSFX, FONE, ROMN, MAP, LATI, LONG, ROLE, QUAY, \
    CALN, UnexpectedTag, PAGE, FAMS, ANCE, DESC


class UnexpectedLine(RuntimeError):
    def __init__(self, line, line_num, msg):
        RuntimeError.__init__(self, msg)
        self.line = line
        self.line_num = line_num


class ParseError(RuntimeError):
    def __init__(
        self,
        msg,
        line_num: Optional[int] = None,
        line: Optional[str] = None,
        tag: Optional[Tag] = None,
        parent: Optional[Tag] = None
    ):
        RuntimeError.__init__(self, msg)
        self.line_num = line_num
        self.line = line
        self.tag = tag
        self.parent = parent


class GEDCOM5Parser:

    _tags = {
        'HEAD': HEAD,
        'SOUR': SOUR,
        'VERS': VERS,
        'NAME': NAME,
        'CORP': CORP,
        'DATA': DATA,
        'DATE': DATE,
        'COPR': COPR,
        'CONT': CONT,
        'CONC': CONC,
        'DEST': DEST,
        'TIME': TIME,
        'SUBM': SUBM,
        'SUBN': SUBN,
        'FILE': FILE,
        'GEDC': GEDC,
        'FORM': FORM,
        'CHAR': CHAR,
        'LANG': LANG,
        'PLAC': PLAC,
        'NOTE': NOTE,
        'FAM': FAM,
        'RESN': RESN,
        'HUSB': HUSB,
        'WIFE': WIFE,
        'CHIL': CHIL,
        'NCHI': NCHI,
        'REFN': REFN,
        'TYPE': TYPE,
        'RIN': RIN,
        'INDI': INDI,
        'SEX': SEX,
        'ALIA': ALIA,
        'ANCI': ANCI,
        'DESI': DESI,
        'RFN': RFN,
        'AFN': AFN,
        'OBJE': OBJE,
        'TITL': TITL,
        'REPO': REPO,
        'EVEN': EVEN,
        'AGNC': AGNC,
        'AUTH': AUTH,
        'ABBR': ABBR,
        'PUBL': PUBL,
        'TEXT': TEXT,
        'FAMF': FAMF,
        'TEMP': TEMP,
        'ORDI': ORDI,
        'ADDR': ADDR,
        'ADR1': ADR1,
        'ADR2': ADR2,
        'ADR3': ADR3,
        'CITY': CITY,
        'STAE': STAE,
        'POST': POST,
        'CTRY': CTRY,
        'PHON': PHON,
        'EMAIL': EMAIL,
        'FAX': FAX,
        'WWW': WWW,
        'ASSO': ASSO,
        'RELA': RELA,
        'CHAN': CHAN,
        'FAMC': FAMC,
        'PEDI': PEDI,
        'STAT': STAT,
        'RELI': RELI,
        'CAUS': CAUS,
        'ANUL': ANUL,
        'CENS': CENS,
        'DIV': DIV,
        'DIVF': DIVF,
        'ENGA': ENGA,
        'MARB': MARB,
        'MARC': MARC,
        'MARR': MARR,
        'MARL': MARL,
        'MARS': MARS,
        'CAST': CAST,
        'DSCR': DSCR,
        'EDUC': EDUC,
        'IDNO': IDNO,
        'NATI': NATI,
        'NMR': NMR,
        'OCCU': OCCU,
        'PROP': PROP,
        'RESI': RESI,
        'SSN': SSN,
        'FACT': FACT,
        'AGE': AGE,
        'BIRT': BIRT,
        'CHR': CHR,
        'DEAT': DEAT,
        'BURI': BURI,
        'CREM': CREM,
        'ADOP': ADOP,
        'BAPM': BAPM,
        'BARM': BARM,
        'BASM': BASM,
        'BLES': BLES,
        'CHRA': CHRA,
        'CONF': CONF,
        'FCOM': FCOM,
        'ORDN': ORDN,
        'NATU': NATU,
        'EMIG': EMIG,
        'IMMI': IMMI,
        'PROB': PROB,
        'WILL': WILL,
        'GRAD': GRAD,
        'RETI': RETI,
        'BAPL': BAPL,
        'CONL': CONL,
        'ENDL': ENDL,
        'SLGC': SLGC,
        'SLGS': SLGS,
        'MEDI': MEDI,
        'NPFX': NPFX,
        'GIVN': GIVN,
        'NICK': NICK,
        'SPFX': SPFX,
        'SURN': SURN,
        'NSFX': NSFX,
        'FONE': FONE,
        'ROMN': ROMN,
        'MAP': MAP,
        'LATI': LATI,
        'LONG': LONG,
        'ROLE': ROLE,
        'QUAY': QUAY,
        'CALN': CALN,
        'PAGE': PAGE,
        'FAMS': FAMS,
        'ANCE': ANCE,
        'DESC': DESC,
    }

    def parse_string(self, doc: str, strict=False) -> GEDCOM:
        line_num = 0
        try:
            gedcom = GEDCOM()
            stack = [gedcom]
            for line in doc.splitlines():
                line_num += 1
                if line.startswith('\ufeff'):
                    line = line[1:]
                tokens = line.lstrip().split(' ')
                if not tokens[0].isdigit():
                    raise UnexpectedLine(line, line_num, 'First field is not a number')
                level = int(tokens[0])
                tokens = tokens[1:]
                xref_id = tokens[0] if tokens[0].startswith('@') and tokens[0].endswith('@') else None
                if xref_id:
                    tokens = tokens[1:]
                tag = tokens[0]
                tokens = tokens[1:]
                value = ' '.join(tokens) if tokens else None
                while stack[-1].level >= level:
                    stack.pop()
                if tag in self._tags:
                    entry = self._tags[tag](level=level, parent=stack[-1], xref_id=xref_id, value=value)
                elif strict:
                    raise UnexpectedLine(line, line_num, 'Unknown tag')
                else:
                    entry = Tag(level=level, parent=stack[-1], xref_id=xref_id, tag=tag, value=value)
                stack[-1].append(entry, strict)
                stack.append(entry)
                gedcom.register(entry)
            gedcom.resolve(strict=strict)
            return gedcom
        except UnexpectedLine as ex:
            msg = f'Error at line {line_num}.\n{ex.line}\n{str(ex)}'
            raise ParseError(msg, line_num=line_num, line=ex.line)
        except UnexpectedTag as ex:
            msg = f'Error at line {line_num}.\nUnexpected tag {ex.tag} in {ex.parent}'
            raise ParseError(msg, line_num=line_num, tag=ex.tag, parent=ex.parent)

    def parse_stream(self, fp: BinaryIO, strict=False) -> GEDCOM:
        doc = fp.read().decode('utf-8')
        return self.parse_string(doc, strict)

    def parse_path(self, path: str, strict=False) -> GEDCOM:
        with open(path, 'rb') as fp:
            return self.parse_stream(fp, strict)
