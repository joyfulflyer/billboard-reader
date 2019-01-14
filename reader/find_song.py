import functools
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from . flask_db import get_db

bp = Blueprint('/search', __name__, url_prefix='/')


@bp.route('/search', methods=("GET", "POST"))
def search():
    if request.method == 'POST':
        return redirect(url_for('search_results'))
    return render_template('search.html')


@bp.route('/search_results', methods=("GET",))
def search_results():
    return render_template('search_results.html')


@bp.route('/partialSong/<input>', methods=("GET",))
def partial_song(input):
    return "This should be json"
