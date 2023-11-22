from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
import urllib
from collections import namedtuple


from . import search
from .util import StrInLanguage
from .locales import Locale

LangOption = namedtuple("LangOption", "value label")

bp = Blueprint('main', __name__)

@bp.route('/', methods=('GET',))
def index():
    title = request.args.get('title')
    wikt = request.args.get('wikt')
    locale = Locale(wikt) if wikt else Locale()
    lang = request.args.get('lang') or locale.language

    language_options = [
        LangOption(
            value = lang,
            label = locale.language_names[lang] + f' [{lang}]'
        ) for lang in
            locale.language_names.keys()
    ]

    if not title:
        return render_template('index.html',
                               results=[],
                               locale=locale,
                               language_options=language_options)

    title_with_lang = StrInLanguage(title, lang=lang)
    encoded_title = urllib.parse.quote(title.replace(' ', '_'), safe='/', encoding=None, errors=None)
    edit_url = f"https://{wikt}.wiktionary.org/w/index.php?title={encoded_title}&action=edit" if wikt else None
    view_url = f"https://{wikt}.wiktionary.org/wiki/{encoded_title}" if wikt else None

    return render_template('index.html',
                           results=search.get_images_for_word_ranked(title_with_lang, locale),
                           edit_url=edit_url,
                           view_url=view_url,
                           locale=locale,
                           language_options=language_options,
                           get_color_class=search.GetColorClass())
