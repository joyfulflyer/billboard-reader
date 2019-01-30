from flask import ( Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort

from . flask_db import get_db

bp = Blueprint('/song', __name__, url_prefix='/song')


@bp.route('/<int:selected_id>')
def song_by_id(selected_id):
    entry = get_db().execute('''
                     SELECT * FROM entries WHERE id = ?
                     ''', (selected_id,)).fetchone()
    if entry is None:
        abort(404, "Not found")
    songs = get_db().execute('''
                             SELECT * FROM entries
                             WHERE name = ? AND artist = ?''',
                             (entry["name"], entry["artist"])).fetchall()
  #  id_list = list(map(lambda x: x["chart_id"], songs))
 #   charts = []
    for cur in songs:
        c = get_db().execute('''
                                   SELECT * FROM charts WHERE id = ?
                                   ''', (cur["chart_id"],)).fetchone()

    return render_template('song.html', song=entry, songs=charts)
