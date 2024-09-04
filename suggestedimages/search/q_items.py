import re
from typing import *

import pywikibot
from pywikibot import pagegenerators

from ..constants import *
from ..localization import Locale
from ..util import StrInLanguage
from .result import Result, CommonsResult, ImageResult, WDEntry, NoImagesResult
from . import queries
from .wikidata import get_entry_description

from ..external_apis import external_apis_by_language


site = pywikibot.Site("wikidata", "wikidata")


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


prop_cache = {}
def get_prop_name(locale: Locale, prop):
    if prop not in prop_cache:
        repo = site.data_repository()
        page = pywikibot.Page(repo, prop)
        item = pywikibot.PropertyPage(repo, prop)

        if locale.language in item.labels:
            prop_cache[prop] = item.labels[locale.language]
        elif 'en' in item.labels:
            prop_cache[prop] = item.labels['en']

    return prop_cache[prop]



def yield_image_descriptions(locale: Locale, entry: WDEntry, caption: str) -> Iterator[ImageResult]:
    for prop in entry.claims:
        if prop not in entry.claims:
            continue
        for image_entry in entry.claims[prop]:
            commons_media = image_entry.target

            if isinstance(commons_media, pywikibot.page.FilePage):
                prop_name = get_prop_name(locale, prop)
                info = commons_media.latest_file_info
                if not info['mime'].startswith('image'):
                    continue
                yield ImageResult(
                    name = commons_media.title().removeprefix('File:'),
                    url = commons_media.full_url(),
                    thumb = commons_media.get_file_url(url_width=320),
                    caption = caption,
                    facet = prop_name,
                    size = (info['width'], info['height'])
                )


def yield_image_pages(generator: Iterator, searched: StrInLanguage, locale: Locale) -> Iterator[tuple[Result, WDEntry]]:

    for entry in generator:
        entry_info = get_entry_description(entry, searched, locale)

        count = 0
        for image_info in yield_image_descriptions(locale, entry, searched.text.capitalize()):
            yield image_info, entry_info
            count += 1

        if count == 0:
            yield NoImagesResult(), entry_info


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
