"""
Search images by structured data (https://commons.wikimedia.org/wiki/Commons:Structured_data)
"""

from typing import *
import hashlib

import requests
import pywikibot
from pywikibot import pagegenerators
from pywikibot.page import Page

from suggestedimages.localization.locale import Locale
from suggestedimages.util import StrInLanguage, StrInLanguages
from suggestedimages.search.result import ImageResult, WDEntry
from suggestedimages.search import queries
from .wikidata import get_entry_description


site = pywikibot.Site("commons", "commons")
site.login()

wikidata_site = pywikibot.Site("wikidata", "wikidata")


def get_images_for_item_buffered(searched_id: str, title: str, locale: Locale, buffer_len: int) -> list[tuple[ImageResult, WDEntry]]:
    item = pywikibot.ItemPage(wikidata_site.data_repository(), searched_id)
    entry_info = get_entry_description(item, StrInLanguage(title, lang=locale.language), locale)
    media_page_generator = yield_media_depicting_item(entry_info)
    images_generator = yield_images(media_page_generator, entry_info, title, locale)
    buf = []
    for i, image in enumerate(images_generator, start=1):
        buf.append(image)
        if i % buffer_len == 0:
            yield buf
            buf = []

    yield buf


def yield_media_depicting_item(wd_entry: WDEntry) -> Iterator[Page]:

    return pagegenerators.WikidataSPARQLPageGenerator(
        queries.property_depicts_has_given_id(wd_entry.id),
        site = site,
        endpoint = 'https://commons-query.wikimedia.org/sparql',
        entity_url = 'https://commons.wikimedia.org/entity/'
    )


def yield_images(media_page_generator: Iterator, wd_entry: WDEntry, searched_name: str, locale: Locale) \
    -> Iterator[tuple[ImageResult, WDEntry]]:

    ids = [page.id for page in media_page_generator]
    request = site.simple_request(action='wbgetentities', ids=ids)

    raw = request.submit()

    if 'entities' in raw:
        for page_id, page_data in raw['entities'].items():
            if not 'statements' in page_data:
                continue
            for item in page_data['statements']['P180']:
                if not 'mainsnak' in item or not 'datavalue' in item['mainsnak']:
                    continue
                q_id = item['mainsnak']['datavalue']['value']['id']
                if q_id != wd_entry.id:
                    continue
                page_name = page_data['title']
                yield ImageResult(
                    name = page_name,
                    url = f'https://commons.wikimedia.org/wiki/{page_name}',
                    thumb = get_wikimedia_commons_thumb(page_name.removeprefix('File:')),
                    caption = searched_name.capitalize(),
                    facet = ''
                )


def get_wikimedia_commons_thumb(image, width=300):
    image = image.replace(' ', '_')
    m = hashlib.md5()
    m.update(image.encode('utf-8'))
    digest = m.hexdigest()
    return f'https://upload.wikimedia.org/wikipedia/commons/thumb/{digest[0]}/{digest[0:2]}/{image}/{str(width)}px-{image}' \
        + ('.png' if image.endswith('.svg') else '')




if __name__ == "__main__":
    from suggestedimages.util import pretty_print

    pretty_print(get_images_for_item('Q164359', '', Locale()))
