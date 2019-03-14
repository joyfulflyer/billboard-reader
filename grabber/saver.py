from reader.models.chart import Chart
from reader.models.entry import Entry
import sqlite3


def save_chart(chart, Session):
    session = Session()
    db_chart = Chart(type="hot-100", date_string=chart.date)
    session.add(db_chart)
    try:
        session.commit()
    except sqlite3.IntegrityError:
        return
    except Exception as err:
        print("caught a integrety error {0}".format(err))
        return

    rowId = db_chart.id
    for entry in chart.entries:
        e = Entry(name=entry.title,
                  artist=entry.artist,
                  place=entry.rank,
                  peak_position=entry.peakPos,
                  last_position=entry.lastPos,
                  weeks_on_chart=entry.weeks,
                  chart_id=rowId)
        session.add(e)
    session.commit()
