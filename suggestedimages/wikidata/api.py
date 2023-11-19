import re
import random
from typing import *

import pywikibot
from pywikibot import pagegenerators

from ..constants import *
from ..locales import Locale
from ..util import StrInLanguage, StrInLanguages
from .result import Result, CommonsResult, ImageResult, WDEntry, NoImage
from . import queries



site = pywikibot.Site("wikidata", "wikidata")


def spaced(*args):
    return " ".join(str(arg) for arg in args if arg != None)

def build_composite_description(label, aliases, translation, description):
    """Combines descriptive texts into one text.
    """
    return spaced((label if label else None),
                  ((f"({', '.join([str(alias) for alias in aliases])})") if aliases else None),
                  ((f"[= {translation}]") if translation else None)) \
                  + ((f": {description}") if description else "")

def yield_label_or_alias_results(searched) -> Iterator:
    return pagegenerators.WikidataSPARQLPageGenerator(
        queries.label_or_alias_capitalized_or_not(searched.text, searched.language),
        site=site.data_repository()
    )

def get_entry_description(entry: Iterator, color_num: int, searched: StrInLanguage, locale: Locale) -> WDEntry:
    label = StrInLanguages(entry.labels).get(searched.language) or locale["[no label]"]
    aliases = StrInLanguages(entry.aliases).get(searched.language)

    translation = None
    if locale.language != searched.language:
        translation = StrInLanguages(entry.labels).get(locale.language)
        if not translation and searched.language != 'en':
            translation = StrInLanguages(entry.labels).get('en')

    description = StrInLanguages(entry.descriptions).get(locale.language, 'en', searched.language)

    tooltip = build_composite_description(label, aliases, translation, description)

    return WDEntry(
        entry.id,
        label,
        aliases or [],
        description,
        tooltip,
        entry.full_url(),
        'color-' + str(color_num % NUM_COLORS + 1),
    )


def yield_image_descriptions(entry: WDEntry, caption: str) -> Iterator[ImageResult]:
    for (prop, name) in IMAGE_PROPS:
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


def yield_image_pages(generator: Iterator, searched: StrInLanguage, locale: Locale) -> Iterator[tuple[Result, WDEntry]]:

    for color_num, entry in enumerate(generator, start=random.randint(0, NUM_COLORS)):
        entry_info = get_entry_description(entry, color_num, searched, locale)

        count = 0
        for image_info in yield_image_descriptions(entry, searched.text.capitalize()):
            yield image_info, entry_info
            count += 1

        if count == 0:
            yield NoImage, entry_info


        if (prop := entry.claims.get('P373')) and len(prop) > 0:
            yield CommonsResult('Category:' + prop[0].getTarget(), 'category'), entry_info

        if (prop := entry.claims.get('P935')) and len(prop) > 0:
            yield CommonsResult(prop[0].getTarget(), 'gallery'), entry_info


def get_images_for_word(searched: StrInLanguage, locale: Locale) -> list[tuple[Result, WDEntry]]:
    entries_generator = yield_label_or_alias_results(searched)

    result_tuples = list(yield_image_pages(entries_generator, searched, locale))
    ranks = get_ranks_for_entries(result_tuples, searched)

    return sorted(
        result_tuples,
        key = lambda pair: ranks[pair[1].id],
        reverse = True,
    )



def get_ranks_for_entries(results: list[tuple[Result, WDEntry]], searched: StrInLanguage):
    entry_ranks = {}

    for result_info, entry_info in results:
        if entry_info.id not in entry_ranks:
            entry_ranks[entry_info.id] = (False, True, False)

        exact_case_match = (entry_info.label == searched or searched in entry_info.aliases)
        no_images = (result_info == NoImage)
        gallery_found = (isinstance(result_info, CommonsResult))

        prev_rank = entry_ranks[entry_info.id]
        entry_ranks[entry_info.id] = (
            prev_rank[0] or exact_case_match,
            prev_rank[1] and not no_images,
            prev_rank[2] or gallery_found
        )

    return entry_ranks


if __name__ == "__main__":
    print(get_images_for_word(StrInLanguage('rautatiesilta', lang='fi'), 'fi'))
