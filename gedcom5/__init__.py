from typing import BinaryIO


class GEDCOM:
    def __init__(self, level: int = -1):
        self.level = level
        self.items = []

    def append(self, item: 'Entry'):
        self.items.append(item)

    def __repr__(self):
        return f'{self.items}'

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return self.items.__iter__()

    def find(self, tags):
        nodes = [self]
        for tag in tags.split('.'):
            nodes = [item for node in nodes for item in node.items if item.tag == tag]
        return nodes

    def __getitem__(self, item):
        return self.items[item]


class Entry(GEDCOM):
    def __init__(self, level: int, xref_id: str = None, tag: str = None, value: str = None):
        super().__init__(level=level)
        self.level = level
        self.xref_id = xref_id
        self.tag = tag
        self.value = value

    def __repr__(self):
        if self.xref_id:
            if self.value:
                return f'{self.level} {self.xref_id} {self.tag} {self.value}'
            return f'{self.level} {self.xref_id} {self.tag}'
        else:
            if self.value:
                return f'{self.level} {self.tag} {self.value}'
            return f'{self.level} {self.tag}'


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
