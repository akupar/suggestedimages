from dataclasses import dataclass
import hashlib
from typing import *

from ..constants import *
from ..util import StrInLanguage


@dataclass
class WDEntry:
    id: str
    label: StrInLanguage
    aliases: list[StrInLanguage]
    description: StrInLanguage
    text: str
    full_url: str

    @property
    def url(self):
        return f'https://www.wikidata.org/wiki/{self.id}'

class Result:
    name: str
    url: str
    facet: str
    type: str

@dataclass
class ImageResult(Result):
    name: str
    url: str
    thumb: str
    caption: str
    facet: str

    type = 'image'

@dataclass
class CommonsResult(Result):
    name: str
    facet: str
    type = 'link'

    @property
    def url(self):
        return f'https://commons.wikimedia.org/wiki/{self.name.replace(" ", "_")}'


NoImage = ImageResult('No Images', None, NO_IMAGE_THUMB, None, None)
