import functools
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from . flask_db import get_db
import json

bp = Blueprint('/search', __name__, url_prefix='/')


@bp.route('/', methods=("GET", "POST"))
def search():
    if 'search' in request.args:
        return redirect(url_for('/search.search_results'))
    return render_template('search.html')


@bp.route('/search_results', methods=("GET",))
def search_results():
    if 'name' not in request.args:
        abort(400, "Bad request, very bad")

    name = request.args['name']
    name = convertToSpaces(name)
#    artist = request.args['artist']
#    artist = convertToSpaces(artist)

    songs = get_songs_with_name(name)

    return json.dumps(convert_rows_to_dict(songs))


@bp.route('/partialSong/<input>', methods=("GET",))
@bp.route('/partialSong')
def partial_song(input):
    print("raw input " + input)
    converted = convertToSpaces(input)
    print("converted = " + converted)
    songs = get_songs_with_name(converted)

    return json.dumps(convert_rows_to_dict(songs))


def get_songs_with_name(song_name):
    print(song_name)
    whereClause = '%' + song_name + '%'
    print("where clause: {}".format(whereClause))
    songs = get_db().execute('''
        SELECT * FROM entries
        WHERE UPPER(name) LIKE UPPER(?)
        GROUP BY name, artist
        ORDER BY name
        LIMIT 15
        ''', (whereClause,)).fetchall()
    return songs


def convert_rows_to_dict(rows):
    return [dict(r) for r in rows]


@bp.route('/songnames', methods=("GET",))
def get_all_song_names():
    all_songs = get_db().execute('''
                                 SELECT * FROM entries GROUP BY name, artist
                                 ''').fetchall()
    r = convert_rows_to_dict(all_songs)
    return json.dumps(r)


def convertToSpaces(input):
    return " ".join(input.split('_'))
