from reader.models.chart import Chart
from reader.models.entry import Entry

def saveChart(chart, Session):
	session = Session()
	c = Chart(type="hot-100", date_string=chart.date)
	session.add(c)

    c = conn.cursor()
    try:
        c.execute(''' INSERT INTO charts(type, date_string)
                  VALUES (?, ?) ''', ("hot-100", chart.date))
    except sqlite3.IntegrityError:
        return
    rowId = c.lastrowid
    for entry in chart.entries:
    	e = Entry(name=entry.title, artist=entry.artist, place=entry.rank, peak_position=entry.peakPos, last_position=entry.lastPos, weeks_on_chart=entry.weeks, chart_id=rowId)

    conn.commit()
