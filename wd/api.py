import re
import random
from typing import *

import pywikibot
from pywikibot import pagegenerators

from .result import CommonsResult, ImageResult, WDEntry, NoImage
from .util import build_tooltip, StrInLanguage, StrInLanguages
from .locales import Locale
from . import queries
import config


site = pywikibot.Site("wikidata", "wikidata")

def generate_label_or_alias_results(searched):
    return pagegenerators.WikidataSPARQLPageGenerator(
        queries.label_or_alias_capitalized_or_not(searched.text, searched.language),
        site=site.data_repository()
    )

def get_entry_description(entry, color_num: int, searched: StrInLanguage, locale: Locale) -> WDEntry:
    label = StrInLanguages(entry.labels).get(searched.language) or locale["[no label]"]
    aliases = StrInLanguages(entry.aliases).get(searched.language)

    translation = None
    if locale.language != searched.language:
        translation = StrInLanguages(entry.labels).get(locale.language)
        if not translation and searched.language != 'en':
            translation = StrInLanguages(entry.labels).get('en')

    description = StrInLanguages(entry.descriptions).get(locale.language, 'en', searched.language)

    tooltip = build_tooltip(label, aliases, translation, description)

    return WDEntry(
        entry.id,
        label,
        description,
        tooltip,
        entry.full_url(),
        'color-' + str(color_num % config.NUM_COLORS + 1),
    )


def generate_image_descriptions(entry: WDEntry, caption: str) -> Iterator[ImageResult]:
    for (prop, name) in config.IMAGE_PROPS:
        if prop not in entry.claims:
            continue

        for image_entry in entry.claims[prop]:
            commons_media = image_entry.target
            if isinstance(commons_media, pywikibot.page.FilePage):
                yield ImageResult(
                    name = commons_media.title(),
                    url = commons_media.full_url(),
                    thumb = commons_media.get_file_url(url_width=320),
                    caption = caption,
                    facet = name
                )


def generate_image_pages(generator, searched: StrInLanguage, locale: Locale) -> Iterator[tuple[ImageResult, WDEntry]]:

    for color_num, entry in enumerate(generator, start=random.randint(0, config.NUM_COLORS)):
        entry_info = get_entry_description(entry, color_num, searched, locale)

        count = 0
        for image_info in generate_image_descriptions(entry, searched.text.capitalize()):
            yield image_info, entry_info
            count += 1

        if count == 0:
            yield NoImage, entry_info


        if (prop := entry.claims.get('P373')) and len(prop) > 0:
            yield CommonsResult('Category:' + prop[0].getTarget()), entry_info

        if (prop := entry.claims.get('P935')) and len(prop) > 0:
            yield CommonsResult(prop[0].getTarget()), entry_info


def get_images_for_search(searched: StrInLanguage, locale: Locale) -> list[tuple[ImageResult, WDEntry]]:
    entries_generator = generate_label_or_alias_results(searched)

    lst = list(generate_image_pages(entries_generator, searched, locale))
    return lst





if __name__ == "__main__":
    print(get_images_for_search(StrInLanguage('rautatiesilta', lang='fi'), 'fi'))
