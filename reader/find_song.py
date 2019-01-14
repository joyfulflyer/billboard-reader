import functools
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from . flask_db import get_db
import json

bp = Blueprint('/search', __name__, url_prefix='/')


@bp.route('/search', methods=("GET", "POST"))
def search():
    if request.method == 'POST':
        return redirect(url_for('search_results'))
    return render_template('search.html')


@bp.route('/search_results', methods=("GET",))
def search_results():
    name = request.args['name']
    name = convertToSpaces(name)
    artist = request.args['artist']
    artist = convertToSpaces(artist)

    songs = get_db().execute('''
            SELECT * FROM songs WHERE name=? AND artist=?
                             ''', (name, artist)).fetchall()
    dicts = []
    for s in songs:
        dicts.append({
                     "position": s[0],
                     "name": s[1],
                     "artist": s[2],
                     "date": s[3]
                     })

    return json.dumps(dicts)


@bp.route('/partialSong/<input>', methods=("GET",))
def partial_song(input):
    print("raw input " + input)
    converted = convertToSpaces(input)
    print("converted = " + converted)
    songs = get_db().execute('''
            SELECT DISTINCT name, artist FROM songs
            WHERE UPPER(name) LIKE UPPER(?)
            ''', ('%' + converted + '%',)).fetchall()
    return str(songs)


def convertToSpaces(input):
    return " ".join(input.split('_'))
