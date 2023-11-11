from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

import wd


bp = Blueprint('main', __name__)

@bp.route('/', methods=('GET',))
def index():
    title = request.args.get('title')
    wikt = request.args.get('wikt')
    lang = request.args.get('lang') or wikt

    return render_template('index.html',
                           format=formatters.get_formatter(wikt))
