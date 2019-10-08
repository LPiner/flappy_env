from enum import Enum

from attr import attrs, attrib


class Actions(Enum):
    JUMP = "JUMP"
    NOTHING = "NOTHING"