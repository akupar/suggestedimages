import re
from typing import *

import pywikibot
from pywikibot import pagegenerators

from ..constants import *
from ..localization import Locale
from ..util import StrInLanguage, StrInLanguages
from .result import Result, CommonsResult, ImageResult, WDEntry, NoImage
from . import queries

from ..external_apis import external_apis_by_language


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
        queries.label_or_alias_capitalized_or_not(searched),
        site=site.data_repository()
    )

def yield_external_results(searched) -> Iterator:
    for handler in external_apis_by_language.get(searched.language, []):
        results = handler.get(searched.text)
        values = [result.ref.value for result in results]
        if not values:
            continue

        return pagegenerators.WikidataSPARQLPageGenerator(
            queries.property_has_any_of_values(handler.wikidata_property, values),
            site=site.data_repository()
        )

    return []


def get_entry_description(entry: Iterator, searched: StrInLanguage, locale: Locale) -> WDEntry:
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

    for entry in generator:
        entry_info = get_entry_description(entry, searched, locale)

        count = 0
        for image_info in yield_image_descriptions(entry, searched.text.capitalize()):
            yield image_info, entry_info
            count += 1

        if count == 0:
            yield NoImage, entry_info


        # Property P373 = Commons category
        if (prop := entry.claims.get('P373')) and len(prop) > 0:
            yield CommonsResult('Category:' + prop[0].getTarget(), 'category'), entry_info

        # Property P935 = Commons gallery page
        if (prop := entry.claims.get('P935')) and len(prop) > 0:
            yield CommonsResult(prop[0].getTarget(), 'gallery'), entry_info


def get_images_for_word(searched: StrInLanguage, locale: Locale) -> list[tuple[Result, WDEntry]]:
    wikidata_entries_generator = remove_duplicate_entries(
        yield_label_or_alias_results(searched),
        yield_external_results(searched)
    )

    return list(yield_image_pages(wikidata_entries_generator, searched, locale))


def remove_duplicate_entries(*generators):
    seen = set()
    for generator in generators:
        for entry in generator:
            if entry.id not in seen:
                yield entry
                seen.add(entry.id)
