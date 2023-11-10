from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

import wd


bp = Blueprint('main', __name__)

@bp.route('/', methods=('GET',))
def index():
    title = request.args.get('title')
    wikt = request.args.get('wikt')

    return render_template('index.html',
                           images=wd.get_images_for_search(title, wikt) if title else [])
