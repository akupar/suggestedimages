import uuid
import json

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, jsonify
)
import urllib.parse
from collections import namedtuple


from . import search
from .util import StrInLanguage, GeneratorCache
from .localization import Locale

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


@bp.route('/', methods=('GET',))
def index():
    title = request.args.get('title')
    wikt = request.args.get('wikt')
    try:
        locale = Locale(wikt) if wikt else Locale()
    except:
        locale = Locale()
    lang = request.args.get('lang') or locale.language

    if not title:
        return render_template('index.html',
                               results = [],
                               locale = locale,
                               list_locales = Locale.list_locales,
                               language_options = list_language_options(locale))

    title_with_language = StrInLanguage(title, lang=lang)


    image_template = locale.format_image("$FILE", title.capitalize())

    return render_template('index.html',
                           edit_url = get_edit_url(wikt, title),
                           view_url = get_view_url(wikt, title),
                           locale = locale,
                           image_template = image_template,
                           list_locales = Locale.list_locales,
                           language_options = list_language_options(locale),
                           make_query_params = make_query_params)


@bp.route('/help.html', methods=('GET',))
def help():
    return render_template('help.html')


@bp.route('/more-images', methods=('GET',))
def more_images():
    item = request.args.get('item')
    title = request.args.get('title')
    wikt = request.args.get('wikt')
    id = hash((request.cookies.get('remember_token'), item))

    try:
        locale = Locale(wikt) if wikt else Locale()
    except:
        locale = Locale()


    generator = search.get_chunk_of_images_for_item(item, title, locale, 10)
    generators[id] = generator

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
    locale = Locale(wikt)
    lang = request.args.get('lang') or locale.language

    if not title or not wikt or not lang:
        return "Parametre 'title', 'wikt', or 'lang' missing", 400

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
    id = hash((request.cookies.get('remember_token'), item))
    if not id in generators:
        return "No result stream found", 110

    generator = generators[id]

    try:
        batch = next(generator)
    except StopIteration:
        batch = []

    return jsonify([(vars(item), None) for item in batch])
