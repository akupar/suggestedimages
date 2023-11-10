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


if __name__ == "__main__":


    img = Image("NGO Nishi Nagono 2-chome 20230208-01.jpg", "", "", None)
    print(img.thumb)

    img = Image("ジブチ大使館は一軒家.jpg", "", "", None)
    print(img.thumb)

    img = Image("SVG icon (letters).svg", "", "", None)
    print(img.thumb)
