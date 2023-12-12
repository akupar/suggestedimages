from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, jsonify
)
import urllib
from collections import namedtuple


from . import search
from .util import StrInLanguage
from .localization import Locale

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

    return render_template('index.html',
                           results = search.get_images_for_word_ranked(title_with_language, locale),
                           edit_url = get_edit_url(wikt, title),
                           view_url = get_view_url(wikt, title),
                           locale = locale,
                           list_locales = Locale.list_locales,
                           language_options = list_language_options(locale),
                           get_color_class = search.GetColorClass())


@bp.route('/help.html', methods=('GET',))
def help():
    return render_template('help.html')

generator = None

@bp.route('/more-images', methods=('GET',))
def more_images():
    global generator
    item = request.args.get('item')
    title = request.args.get('title')
    wikt = request.args.get('wikt')
    try:
        locale = Locale(wikt) if wikt else Locale()
    except:
        locale = Locale()

    generator = search.get_chunk_of_images_for_item(item, title, locale, 10)

    image_template = locale.format_image("$FILE", title.capitalize())

    return render_template('more-images.html',
                           results = [],
                           locale = locale,
                           image_template = image_template,
                           get_color_class = search.GetColorClass())



@bp.route('/api/structured-data', methods=('GET',))
def api_structured_data():
    try:
        batch = next(generator)
    except StopIteration:
        batch = []
    return jsonify([vars(item) for item in batch])
