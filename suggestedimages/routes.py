from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
import urllib

import wd
from wd.util import StrInLanguage
from wd.locales import Locale, DEFAULT_LOCALE

bp = Blueprint('main', __name__)

@bp.route('/', methods=('GET',))
def index():
    title = request.args.get('title')
    if not title:
        return render_template('index.html', results=[], locale=DEFAULT_LOCALE)

    wikt = request.args.get('wikt')
    locale = Locale(wikt) if wikt else DEFAULT_LOCALE
    lang = request.args.get('lang') or locale.language
    lang_str = StrInLanguage(title, lang=lang)
    encoded_title = urllib.parse.quote(title.replace(' ', '_'), safe='/', encoding=None, errors=None)
    edit_url = f"https://{wikt}.wiktionary.org/w/index.php?title={encoded_title}&action=edit" if wikt else None
    view_url = f"https://{wikt}.wiktionary.org/wiki/{encoded_title}" if wikt else None


    return render_template('index.html',
                           results=wd.get_images_for_search(lang_str, locale),
                           edit_url=edit_url,
                           view_url=view_url,
                           locale=locale)
