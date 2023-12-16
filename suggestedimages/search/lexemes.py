from typing import *

import pywikibot
from pywikibot import pagegenerators
from pywikibot.page import LexemePage, LexemeSense

from ..localization import Locale
from ..util import StrInLanguage, StrInLanguages
from .result import Result, ImageResult, SenseEntry, NoImage
from . import queries


site = pywikibot.Site("wikidata", "wikidata")


def get_images_for_word(searched: StrInLanguage, locale: Locale) -> list[tuple[Result, SenseEntry]]:
    lexemes_generator = yield_matching_lexemes(searched)
    senses_generator = yield_senses(lexemes_generator)
    images_generator = yield_images(senses_generator, searched, locale)

    return list(images_generator)



def yield_matching_lexemes(searched) -> Iterator[LexemePage]:
    return pagegenerators.WikidataSPARQLPageGenerator(
        queries.lexeme(searched),
        site=site.data_repository()
    )


def yield_senses(lexeme_generator: Iterator) -> Iterator[LexemeSense]:
    for lexeme in lexeme_generator:
        for sense in lexeme.senses:
            yield sense




def yield_images(sense_generator: Iterator, searched: StrInLanguage, locale: Locale) \
    -> Iterator[tuple[Result, SenseEntry]]:

    for sense in sense_generator:
        sense_info = get_sense_description(sense, searched, locale)

        count = 0
        for image_info in yield_image_descriptions(sense, searched):
            yield image_info, sense_info
            count += 1

        if count == 0:
            yield NoImage, sense_info



def get_sense_description(entry, searched: StrInLanguage, locale: Locale) -> SenseEntry:
    label = entry.on_lexeme.text['lemmas'].get(searched.language)
    meaning = StrInLanguages(entry.glosses).get(locale.language) or StrInLanguages(entry.glosses).get('en')
    if not meaning and searched.language != 'en':
        meaning = StrInLanguages(entry.glosses).get('en')

    return SenseEntry(
        entry.id,
        label,
        entry.on_lexeme.id,
        text = f'{label}' + (f' ’{meaning}’' if meaning else '')
    )


def yield_image_descriptions(entry: SenseEntry, caption: str) -> Iterator[ImageResult]:
    for image_entry in entry.claims.get('P18', []):
        commons_media = image_entry.target
        if isinstance(commons_media, pywikibot.page.FilePage):
            info = commons_media.latest_file_info
            yield ImageResult(
                name = commons_media.title(),
                url = commons_media.full_url(),
                thumb = commons_media.get_file_url(url_width=320),
                caption = caption,
                facet = None,
                size = (info['width'], info['height'])
            )


if __name__ == "__main__":
    from suggestedimages.util import pretty_print

    pretty_print(get_images_for_word(StrInLanguage('hund', lang='da'), Locale()))
