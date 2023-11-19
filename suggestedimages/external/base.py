from dataclasses import dataclass
from collections import namedtuple
from typing import *

Ref = namedtuple("Ref", "property value")

@dataclass
class ExternalResult:
    ref: Ref
    label: str
    aliases: list[str]


class ExternalApi:
    def get(self, word: str) -> list[ExternalResult]:
        raise NotImplementedError
