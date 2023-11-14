from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

import wd
from wd.util import StrInLanguage
from wd.locales import Locale, DEFAULT_LOCALE

bp = Blueprint('main', __name__)

@bp.route('/', methods=('GET',))
def index():
    title = request.args.get('title')
    if not title:
        return render_template('index.html', images=[], locale=DEFAULT_LOCALE)

    wikt = request.args.get('wikt')
    locale = Locale(wikt) if wikt else DEFAULT_LOCALE
    lang = request.args.get('lang') or locale.language
    lang_str = StrInLanguage(title, lang=lang)

    return render_template('index.html',
                           images=wd.get_images_for_search(lang_str, locale),
                           locale=locale)
