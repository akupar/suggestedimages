import re
import random

import pywikibot
from pywikibot import pagegenerators

from .result import Image, WDEntry, NoImage
from .util import uppercase_first, pretty_print
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


def generate_label_or_alias_results(search, language):
    if search.find('''"""''') != -1:
        raise Exception(f"Invalid search string: {search}")

    if not re.match(r'^[a-z-]+$', language):
        raise Exception(f"Invalid language code: {language}")

    QUERY = '''
SELECT distinct ?item ?itemLabel ?itemDescription WHERE{
  VALUES ?prefLabel { """''' + search + '''"""@''' + language + ''' """''' + uppercase_first(search) + '''"""@''' + language + ''' }
        ?item rdfs:label|skos:altLabel ?prefLabel
}

LIMIT 10
'''

    #generator = pagegenerators.PreloadingEntityGenerator(pagegenerators.WikidataSPARQLPageGenerator(QUERY,site=repo))
    return pagegenerators.WikidataSPARQLPageGenerator(QUERY, site=repo)


def generate_image_pages(generator, search_string, language):
    num_start = random.randint(0, config.NUM_COLORS)

    for index, entry in enumerate(generator):
        print("===", entry.id, "===")
        pretty_print(entry.labels)
        label = entry.labels[language] \
            if language in entry.labels \
            else entry.labels['en'] \
                 if 'en' in entry.labels \
                 else ''

        aliases = entry.aliases[language] \
            if language in entry.aliases \
            else []

        description = entry.descriptions[language] \
            if language in entry.descriptions \
            else entry.descriptions['en'] \
                 if 'en' in entry.descriptions \
                 else ''

        assert label, "No label"
        tooltip = label + ((" (" + ", ".join(aliases) + ")") \
                        if len(aliases) > 0 else '') \
                           + ": " + description

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
                    caption = uppercase_first(search_string),
                ), entry_info
                found = True

        if not found:
            yield NoImage, entry_info


def get_images_for_search(search_string, language):
    items = []

    entries_generator = generate_label_or_alias_results(search_string, language)
    for result, referrer in generate_image_pages(entries_generator, search_string, language):
        items.append((result, referrer))

    return items



if __name__ == "__main__":
    print(get_images_for_search('rautatiesilta', 'fi'))
