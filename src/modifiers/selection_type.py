from talon import Context, Module
from dataclasses import dataclass

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.cursorless
"""

SELECTION_TYPE_KEY = "selectionType"


@dataclass
class SelectionType:
    singular: str
    plural: str
    json_name: str
    rank: int

    @property
    def json_repr(self):
        return {SELECTION_TYPE_KEY: self.json_name}


TOKEN = SelectionType("token", "tokens", "token", 0)
LINE = SelectionType("line", "lines", "line", 1)
BLOCK = SelectionType("block", "blocks", "paragraph", 2)
FILE = SelectionType("file", "files", "document", 3)

SELECTION_TYPES = [
    TOKEN,
    LINE,
    BLOCK,
    FILE
]

RANKED_SELECTION_TYPES = {
    selection_type.json_name: selection_type.rank for selection_type in SELECTION_TYPES
}

selection_type_map = {
    selection_type.json_name: selection_type.json_repr for selection_type in SELECTION_TYPES
}

mod.list("cursorless_selection_type", desc="Types of selection_types")
ctx.lists["self.cursorless_selection_type"] = {
    type.singular: type.json_name for type in SELECTION_TYPES
}

@mod.capture(rule="{user.cursorless_selection_type}")
def cursorless_selection_type(m) -> str:
    return selection_type_map[m.cursorless_selection_type]
