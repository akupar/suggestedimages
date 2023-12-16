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


def get_chunk_of_images_for_item(searched_id: str, title: str, locale: Locale, buffer_len: int) -> list[tuple[ImageResult, WDEntry]]:
    item = pywikibot.ItemPage(wikidata_site.data_repository(), searched_id)
    entry_info = get_entry_description(item, StrInLanguage(title, lang=locale.language), locale)
    media_page_generator = yield_media_depicting_item(entry_info)

    id_chunk_generator = yield_chunk_of_ids(media_page_generator, buffer_len)

    for ids in id_chunk_generator:
        images_generator = yield_images(ids, entry_info, title, locale)
        yield list(images_generator)


def yield_media_depicting_item(wd_entry: WDEntry) -> Iterator[Page]:

    return pagegenerators.WikidataSPARQLPageGenerator(
        queries.property_depicts_has_given_id(wd_entry.id),
        site = site,
        endpoint = 'https://commons-query.wikimedia.org/sparql',
        entity_url = 'https://commons.wikimedia.org/entity/'
    )

def yield_chunk_of_ids(media_page_generator: Iterator[list[str]], buffer_len: int):
    ids_buffer = []
    for i, media_page in enumerate(media_page_generator, start=1):
        ids_buffer.append(media_page.id)

        if i % buffer_len == 0:
            yield ids_buffer
            ids_buffer = []

    yield ids_buffer


def yield_images(ids: list[str], wd_entry: WDEntry, searched_name: str, locale: Locale) \
    -> Iterator[tuple[ImageResult, WDEntry]]:

    request = site.simple_request(action='wbgetentities', ids=ids)

    # Note: site.data_repository() returns wrong datasite (wikidata), so we have to use
    # this in the MediaInfo constructor.
    repo = pywikibot.site.DataSite("commons", "commons")


    raw = request.submit()


    if 'entities' in raw:
        for page_id, page_data in raw['entities'].items():
            if not 'statements' in page_data:
                continue

            mediainfo = pywikibot.MediaInfo(repo, page_id)
            filepage = mediainfo.file
            info = filepage.latest_file_info

            # P180 = depicts
            for item in page_data['statements']['P180']:
                claim = pywikibot.Claim.fromJSON(site, item)
                if claim.target.id != wd_entry.id:
                    continue

                yield ImageResult(
                    name = filepage.title().removeprefix('File:'),
                    url = filepage.full_url(),
                    thumb = filepage.get_file_url(url_width=320),
                    caption = searched_name.capitalize(),
                    facet = '',
                    size = (info['width'], info['height'])
                )


def get_wikimedia_commons_thumb_url(image_name, width=300):
    image_name = image_name.replace(' ', '_')
    m = hashlib.md5()
    m.update(image_name.encode('utf-8'))
    digest = m.hexdigest()
    return f'https://upload.wikimedia.org/wikipedia/commons/thumb/{digest[0]}/{digest[0:2]}/{image_name}/{str(width)}px-{image_name}' \
        + get_thumb_extension(image_name)


def get_thumb_extension(image_name):
    if image_name.endswith('.svg'):
        return '.png'
    if image_name.endswith('.tif'):
        return '.jpg'
    if image_name.endswith('.webm'):
        return '.jpg'
    return ''


if __name__ == "__main__":
    from suggestedimages.util import pretty_print

    pretty_print(get_images_for_item('Q164359', '', Locale()))
