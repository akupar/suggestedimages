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
    """Base class for external api handlers.

    To add a new handler, subclass this and implement `get` method and
    Return `ExternalResult` with relevant information.
    """

    def get(self, word: str) -> list[ExternalResult]:
        raise NotImplementedError
