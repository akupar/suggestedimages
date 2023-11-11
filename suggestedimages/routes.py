from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

import wd
from wd.util import StrInLanguage
from . import formatters

bp = Blueprint('main', __name__)

@bp.route('/', methods=('GET',))
def index():
    title = request.args.get('title')
    wikt = request.args.get('wikt')
    lang = request.args.get('lang') or wikt

    return render_template('index.html',
                           images=wd.get_images_for_search(StrInLanguage(title, lang=lang), wikt) if title else [],
                           format=formatters.get_formatter(wikt))
