from dataclasses import dataclass
import hashlib

import config


@dataclass
class WDEntry:
    id: str
    label: str
    description: str
    text: str
    full_url: str
    color_class: str

    @property
    def url(self):
        return f'https://www.wikidata.org/wiki/{self.id}'


@dataclass
class Image:
    name: str
    url: str
    thumb: str
    caption: str


NoImage = Image('No Images', None, config.NO_IMAGE_THUMB, None)
