import uuid

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, jsonify
)
import urllib.parse
from collections import namedtuple
from werkzeug.local import LocalProxy
from flask import current_app

from .constants import *
from . import search
from .util import StrInLanguage
from .localization import Locale

logger = LocalProxy(lambda: current_app.logger)


bp = Blueprint('main', __name__)

LanguageOption = namedtuple("LanguageOption", "value label")


def list_language_options(locale):
    return [
        LanguageOption(
            value = lang,
            label = locale.language_names[lang] + f' [{lang}]'
        ) for lang in locale.language_names.keys()
    ]


def wikiencode_title(title):
    return urllib.parse.quote(title.replace(' ', '_'), safe='/', encoding=None, errors=None)


def get_edit_url(wikt, title):
    if not wikt:
        return None

    encoded_title = wikiencode_title(title)
    return f"https://{wikt}.wiktionary.org/w/index.php?title={encoded_title}&action=edit"


def get_view_url(wikt, title):
    if not wikt:
        return None

    encoded_title = wikiencode_title(title)
    return f"https://{wikt}.wiktionary.org/wiki/{encoded_title}"


def make_query_params(wikt, item_id, title):
    return urllib.parse.urlencode({
        'wikt': wikt,
        'item': item_id,
        'title': title
    })


def get_locale(wikt):
    try:
        return Locale(wikt) if wikt else Locale(), False
    except:
        return Locale(), True


@bp.route('/', methods=('GET',))
def index():
    title = request.args.get('title')
    wikt = request.args.get('wikt')
    locale = Locale(wikt)
    lang = request.args.get('lang') or locale.language

    if not title:
        return render_template('index.html',
                               results = [],
                               locale = locale,
                               list_locales = Locale.list_locales,
                               language_options = list_language_options(locale),
                               show_localization_blurb = not locale.is_localized)

    title_with_language = StrInLanguage(title, lang=lang)


    image_template = locale.format_image("$FILE", title.capitalize())

    return render_template('index.html',
                           edit_url = get_edit_url(wikt, title),
                           view_url = get_view_url(wikt, title),
                           locale = locale,
                           image_template = image_template,
                           list_locales = Locale.list_locales,
                           language_options = list_language_options(locale),
                           make_query_params = make_query_params,
                           show_localization_blurb = not locale.is_localized)


@bp.route('/help.html', methods=('GET',))
def help():
    return render_template('help.html')


@bp.route('/more-images', methods=('GET',))
def more_images():
    item = request.args.get('item')
    title = request.args.get('title')
    wikt = request.args.get('wikt')

    locale = Locale(wikt if wikt != '' else None)

    logger.debug(f'more-images_init: item: {item}, title: {title}, wikt: {wikt}, language: {locale.language}')

    image_template = locale.format_image("$FILE", title.capitalize())

    return render_template('more-images.html',
                           results = [],
                           item_id = item,
                           locale = locale,
                           wikt = wikt,
                           title = title,
                           image_template = image_template,
                           get_color_class = search.GetColorClass())


@bp.route('/api/item-results', methods=('GET',))
def api_item_results():
    title = request.args.get('title')
    wikt = request.args.get('wikt')
    locale = Locale(wikt if wikt != '' else None)
    lang = request.args.get('lang') or locale.language

    if not title:
        return { 'error': "Parametre 'title' missing" }, 400

    title_with_language = StrInLanguage(title, lang=lang)

    get_color_class = search.GetColorClass()

    results = search.get_images_for_word_ranked(title_with_language, locale)
    results_json = [
        (
            vars(image),
            {
                "id": entry.id,
                "url": entry.url,
                "text": entry.text,
                "colorClass": get_color_class(entry.id)
            }
        ) for image, entry in results
    ]

    return jsonify(results_json)


@bp.route('/api/structured-data', methods=('GET',))
def api_structured_data():
    item = request.args.get('item')
    offset = request.args.get('offset')
    title = request.args.get('title')
    wikt = request.args.get('wikt')
    locale = Locale(wikt if wikt != '' else None)

    logger.debug(f'api_structured_data: item: {item}, offset: {offset}')

    batch = search.get_chunk_of_images_for_item(item, title, locale, N_RESULTS_IN_BATCH, int(offset))

    logger.debug(f'api_structured_data: batch: offset: {offset}, length: {len(batch)}')

    return jsonify({
        'offset': (int(offset) + N_RESULTS_IN_BATCH) if len(batch) == N_RESULTS_IN_BATCH else None,
        'imagesData': [(vars(item), None) for item in batch]
    })
