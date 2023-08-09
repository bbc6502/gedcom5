from typing import BinaryIO, List, Optional


class Element:
    def __init__(self, level: int):
        self.level = level
        self.items: List['Entry'] = []

    def append(self, item: 'Entry'):
        self.items.append(item)

    def __repr__(self):
        return str(self.items)

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return self.items.__iter__()

    def find(self, tags: str) -> List['Entry']:
        nodes = [self]
        for tag in tags.split('.'):
            nodes = [item for node in nodes for item in node.items if item.tag == tag]
        return nodes

    def find_first(self, tags:str, default: 'Entry' = None) -> Optional['Entry']:
        nodes = self.find(tags)
        if len(nodes) > 0:
            return nodes[0]
        return default

    def __getitem__(self, item):
        return self.items[item]


class Entry(Element):
    def __init__(self, level: int, xref_id: str = None, tag: str = None, value: str = None):
        super().__init__(level=level)
        self.xref_id = xref_id
        self.tag = tag
        self.value = value

    def __repr__(self):
        if self.xref_id:
            if self.value:
                out = f'{self.level} {self.xref_id} {self.tag} {self.value}'
            else:
                out = f'{self.level} {self.xref_id} {self.tag}'
        else:
            if self.value:
                out = f'{self.level} {self.tag} {self.value}'
            else:
                out = f'{self.level} {self.tag}'
        return out

    def __str__(self):
        out = [repr(self)]
        for e in self.items:
            out.append(str(e))
        return '\n'.join(out)


class GEDCOM(Element):
    def __init__(self):
        super().__init__(level=-1)
        self.ref = dict()

    def append(self, item: Entry):
        super().append(item)
        if item.xref_id is not None:
            self.ref[item.xref_id] = item


class GEDCOM5:

    def parse_string(self, doc: str) -> GEDCOM:
        gedcom = GEDCOM()
        stack = [gedcom]
        for line in doc.splitlines():
            if line.startswith('\ufeff'):
                line = line[1:]
            tokens = line.lstrip().split(' ')
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
            entry = Entry(level=level, xref_id=xref_id, tag=tag, value=value)
            stack[-1].append(entry)
            stack.append(entry)
        return gedcom

    def parse_stream(self, fp: BinaryIO) -> GEDCOM:
        doc = fp.read().decode('utf-8')
        return self.parse_string(doc)
