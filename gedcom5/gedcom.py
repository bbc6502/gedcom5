from typing import List, Optional
from gedcom5.tag import Tag, UnexpectedTag, INDI, FAM, HEAD, OBJE, NOTE, REPO, SOUR, SUBN, SUBM


class InvalidGEDCOM(RuntimeError):
    def __init__(self, reason):
        super().__init__(f'Invalid GEDCOM: {reason}')


class GEDCOM:

    def __init__(self):
        self.level = -1
        self._items: List[Tag] = []
        self._xref = dict()
        self._to_resolve = []
        self.head: List[HEAD] = []
        self.fam: List[FAM] = []
        self.indi: List[INDI] = []
        self.obje: List[OBJE] = []
        self.note: List[NOTE] = []
        self.repo: List[REPO] = []
        self.sour: List[SOUR] = []
        self.subn: List[SUBN] = []
        self.subm: List[SUBM] = []

    def __len__(self):
        return len(self._items)

    def __getitem__(self, item: int) -> Tag:
        return self._items[item]

    def __iter__(self):
        return self._items.__iter__()

    def register(self, item: Tag):
        if item.ref is not None:
            self._to_resolve.append(item)

    def resolve(self, strict=False):
        for item in self._to_resolve:
            if item.ref in self._xref:
                item.ref = self._xref[item.ref]
            elif strict:
                raise InvalidGEDCOM(f'Missing {item.ref} in gedcom')

    def append(self, item: Tag, strict=False):
        self._items.append(item)
        if item.xref_id is not None:
            self._xref[item.xref_id] = item
        if isinstance(item, HEAD):
            self.head.append(item)
        elif isinstance(item, FAM):
            self.fam.append(item)
        elif isinstance(item, INDI):
            self.indi.append(item)
        elif isinstance(item, OBJE):
            self.obje.append(item)
        elif isinstance(item, NOTE):
            self.note.append(item)
        elif isinstance(item, REPO):
            self.repo.append(item)
        elif isinstance(item, SOUR):
            self.sour.append(item)
        elif isinstance(item, SUBN):
            self.subn.append(item)
        elif isinstance(item, SUBM):
            self.subm.append(item)
        if item.tag in ('HEAD', 'FAM', 'INDI', 'OBJE', 'NOTE', 'REPO', 'SOUR', 'SUBN', 'SUBM'):
            return True
        elif strict:
            raise UnexpectedTag(item, self)
        return False

    def find(self, tags: str) -> List[Tag]:
        nodes = [self]
        for tag in tags.split('.'):
            nodes = [item for node in nodes for item in node._items if item.tag == tag]
        return nodes

    def find_first(self, tags:str, default=None) -> Optional['Tag']:
        nodes = self.find(tags)
        if len(nodes) > 0:
            return nodes[0]
        return default
