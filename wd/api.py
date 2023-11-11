import re
import random

import pywikibot
from pywikibot import pagegenerators

from .result import Image, WDEntry, NoImage
from .util import pretty_print, StrInLanguage
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

LIMIT 10
'''

    #generator = pagegenerators.PreloadingEntityGenerator(pagegenerators.WikidataSPARQLPageGenerator(QUERY,site=repo))
    return pagegenerators.WikidataSPARQLPageGenerator(QUERY, site=repo)


def spaced(*args):
    return " ".join(str(arg) for arg in args if arg != None)


def get_str_in_language(dictionary, languages, default=None):
    for language in languages:
        if language in dictionary:
            return StrInLanguage(dictionary[language], lang=language)
    return default

def get_str_list_in_language(dictionary, languages, default=None):
    for language in languages:
        if language in dictionary:
            return [ StrInLanguage(item, lang=language) for item in dictionary[language] ]
    return default


def build_tooltip(label, aliases, translation, description):
    return spaced((label if label else None),
                  ((f"({', '.join([str(alias) for alias in aliases])})") if aliases else None),
                  ((f"[= {translation}]") if translation else None)) \
                  + ((f": {description}") if description else None)


def generate_image_pages(generator, searched: StrInLanguage, output_language: str):
    num_start = random.randint(0, config.NUM_COLORS)

    for index, entry in enumerate(generator):
        print("===", entry.id, "===")
        pretty_print(entry.labels)
        label = get_str_in_language(entry.labels, [searched.language])
        print("LABEL", label)

        pretty_print(entry.aliases)
        aliases = get_str_list_in_language(entry.aliases, [searched.language], [])
        print("ALIASES", aliases)

        translation = None
        if output_language != searched.language:
            translation = get_str_in_language(entry.labels, [output_language])
            if not translation and searched.language != 'en':
                translation = get_str_in_language(entry.labels, ['en'])

        print("TRANSLATION", translation)
        pretty_print(entry.descriptions)
        description = get_str_in_language(entry.descriptions, [output_language, 'en', searched.language])

        print("DESCRIPTION", description)
        assert label, "No label"
        tooltip = build_tooltip(label, aliases, translation, description)

        print("TOOLTIP:", tooltip)

        entry_info = WDEntry(
            entry.id,
            label,
            description,
            tooltip,
            entry.full_url(),
            'color-' + str((index + num_start) % config.NUM_COLORS + 1)
        )

        found = False
        for prop in IMAGE_PROPS:
            if prop not in entry.claims:
                continue

            for image_entry in entry.claims[prop]:
                print(type(image_entry), dir(image_entry))
                pretty_print(vars(image_entry))
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


def get_images_for_search(searched: StrInLanguage, output_language: str):
    items = []

    entries_generator = generate_label_or_alias_results(searched)
    for result, referrer in generate_image_pages(entries_generator, searched, output_language):
        items.append((result, referrer))

    return items



if __name__ == "__main__":
    print(get_images_for_search(StrWithLanguage('rautatiesilta', lang='fi'), 'fi'))
