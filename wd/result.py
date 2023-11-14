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
    commonscat: str
    commons_gallery: str

    @property
    def url(self):
        return f'https://www.wikidata.org/wiki/{self.id}'

    @property
    def commonscat_url(self):
        return f'https://commons.wikimedia.org/wiki/File:{self.commonscat}'

    @property
    def commons_gallery_url(self):
        return f'https://commons.wikimedia.org/wiki/File:{self.commons_gallery}'


@dataclass
class Image:
    name: str
    url: str
    thumb: str
    caption: str


NoImage = Image('No Images', None, config.NO_IMAGE_THUMB, None)
