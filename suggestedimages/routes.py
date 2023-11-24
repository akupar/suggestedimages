from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
import urllib

from . import search
from .util import StrInLanguage
from .locales import Locale

bp = Blueprint('main', __name__)

@bp.route('/', methods=('GET',))
def index():
    title = request.args.get('title')
    if not title:
        return render_template('index.html', results=[], locale=Locale())

    wikt = request.args.get('wikt')
    locale = Locale(wikt) if wikt else Locale()
    lang = request.args.get('lang') or locale.language
    lang_str = StrInLanguage(title, lang=lang)
    encoded_title = urllib.parse.quote(title.replace(' ', '_'), safe='/', encoding=None, errors=None)
    edit_url = f"https://{wikt}.wiktionary.org/w/index.php?title={encoded_title}&action=edit" if wikt else None
    view_url = f"https://{wikt}.wiktionary.org/wiki/{encoded_title}" if wikt else None


    return render_template('index.html',
                           results=search.get_images_for_word_ranked(lang_str, locale),
                           edit_url=edit_url,
                           view_url=view_url,
                           locale=locale,
                           get_color_class=wikidata.GetColorClass())




@bp.route('/help.html', methods=('GET',))
def help():
    return render_template('help.html')
