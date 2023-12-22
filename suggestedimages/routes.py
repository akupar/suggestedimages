import uuid

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, jsonify
)
import urllib.parse
from collections import namedtuple
from werkzeug.local import LocalProxy
from flask import current_app

from . import search
from .util import StrInLanguage, GeneratorCache
from .localization import Locale

logger = LocalProxy(lambda: current_app.logger)


bp = Blueprint('main', __name__)

LanguageOption = namedtuple("LanguageOption", "value label")

# TODO: might not work on production server
generators = GeneratorCache()



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
    request_id = hash((request.cookies.get('remember_token'), item))

    logger.debug('more-images_init: item: %s, title: %s, wikt: %s, request_id: %x, language: %s'
                 % (item, title, wikt, request_id, locale.language))

    generator = search.get_chunk_of_images_for_item(item, title, locale, 10)
    generators[request_id] = generator

    logger.debug('more-images: create generator[%x] = %x' % (request_id, id(generator)))

    image_template = locale.format_image("$FILE", title.capitalize())

    return render_template('more-images.html',
                           results = [],
                           item_id = item,
                           locale = locale,
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
    request_id = hash((request.cookies.get('remember_token'), item))

    logger.debug('api_structured_data: item: %s, request_id: %x'
                 % (item, request_id))


    if not request_id in generators:
        logger.info('no generator for %x' % (request_id,))
        return { 'error': "No result stream found" }, 110

    generator = generators[request_id]

    logger.debug('api_structured_data: found generator[%x] = %x' % (request_id, id(generator)))

    try:
        batch = next(generator)
    except StopIteration:
        batch = []

    logger.debug('api_structured_data: batch length: %s', (len(batch),))

    return jsonify([(vars(item), None) for item in batch])
