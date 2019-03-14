

def saveChart(chart, conn):
    c = conn.cursor()
    try:
        c.execute(''' INSERT INTO charts(type, date_string)
                  VALUES (?, ?) ''', ("hot-100", chart.date))
    except sqlite3.IntegrityError:
        return
    rowId = c.lastrowid
    for i, entry in enumerate(chart.entries):
        c.execute(''' INSERT INTO entries(
                  name, artist, place, peak_position,
                  last_position, weeks_on_chart, chart_id)
                  VALUES (?, ?, ?, ?, ?, ?, ?) ''',
                  (entry.title, entry.artist, entry.rank,
                   entry.peakPos, entry.lastPos, entry.weeks,
                   rowId))

    conn.commit()
