import re
import random
from typing import *

import pywikibot
from pywikibot import pagegenerators

from .result import Image, WDEntry, NoImage
from .util import build_tooltip, StrInLanguage, StrInLanguages
from .locales import Locale
import config


IMAGE_PROPS = [
    'P18', # image
    'P14', # traffic sign
    'P41',
    'P94',
    'P158', # seal image
    'P242',
    'P367', # astronomic symbol image
    'P1943',
    'P2716', # collage image
    'P5775', # image of interior
    'P8592', # aerial view
    'P8972', # icon
]

site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()


def generate_label_or_alias_results(searched):
    if searched.text.find('''"""''') != -1:
        raise Exception(f"Invalid search string: {searched}")

    if not re.match(r'^[a-z-]+$', searched.language):
        raise Exception(f"Invalid language code: {searched.language}")

    QUERY = '''
SELECT distinct ?item ?itemLabel ?itemDescription WHERE{
  VALUES ?prefLabel {
    """''' + searched.text + '''"""@''' + searched.language + '''
   """''' + searched.text.capitalize() + '''"""@''' + searched.language + '''
  }

  ?item rdfs:label|skos:altLabel ?prefLabel
}

LIMIT 50
'''

    #generator = pagegenerators.PreloadingEntityGenerator(pagegenerators.WikidataSPARQLPageGenerator(QUERY,site=repo))
    return pagegenerators.WikidataSPARQLPageGenerator(QUERY, site=repo)



def generate_image_pages(generator, searched: StrInLanguage, locale: Locale) -> Iterator[tuple[Image, WDEntry]]:

    for color_num, entry in enumerate(generator, start=random.randint(0, config.NUM_COLORS)):

        label = StrInLanguages(entry.labels).get(searched.language) or locale["[no label]"]
        aliases = StrInLanguages(entry.aliases).get(searched.language)

        translation = None
        if locale.language != searched.language:
            translation = StrInLanguages(entry.labels).get(locale.language)
            if not translation and searched.language != 'en':
                translation = StrInLanguages(entry.labels).get('en')

        description = StrInLanguages(entry.descriptions).get(locale.language, 'en', searched.language)

        tooltip = build_tooltip(label, aliases, translation, description)

        entry_info = WDEntry(
            entry.id,
            label,
            description,
            tooltip,
            entry.full_url(),
            'color-' + str(color_num % config.NUM_COLORS + 1)
        )

        found = False
        for prop in IMAGE_PROPS:
            if prop not in entry.claims:
                continue

            for image_entry in entry.claims[prop]:
                commons_media = image_entry.target
                yield Image(
                    name = commons_media.title(),
                    url = commons_media.full_url(),
                    thumb = commons_media.get_file_url(url_width=320),
                    caption = searched.text.capitalize(),
                ), entry_info
                found = True

        if not found:
            yield NoImage, entry_info


def get_images_for_search(searched: StrInLanguage, locale: Locale) -> list[tuple[Image, WDEntry]]:
    entries_generator = generate_label_or_alias_results(searched)

    return list(generate_image_pages(entries_generator, searched, locale))




if __name__ == "__main__":
    print(get_images_for_search(StrInLanguage('rautatiesilta', lang='fi'), 'fi'))
