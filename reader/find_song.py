import functools
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from . flask_db import get_db

bp = Blueprint('/search', __name__, url_prefix='/')


@bp.route('/search', methods=("GET", "POST"))
def search():
    return render_template('search.html')


@bp.route('/partialSong/<input>', methods=("GET",))
def partialSong(imput):
    return "This should be json"
