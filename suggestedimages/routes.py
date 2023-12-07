from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
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
    locale = Locale(wikt) if wikt else Locale()
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
