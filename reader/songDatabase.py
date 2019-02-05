import sys
import billboard
import sqlite3
import datetime
import time


def connect():
    print('connecting to db')
    sys.stdout.flush()
    conn = sqlite3.connect('charts.db')

    return conn


def getCursor(conn):
    sys.stdout.flush()
    c = conn.cursor()
    return c


def dropTables(conn):
    c = conn.cursor()
    print('dropping table')
    c.execute(''' DROP TABLE IF EXISTS songs''')
    c.execute(''' DROP TABLE IF EXISTS charts ''')
    c.execute(''' DROP TABLE IF EXISTS entries ''')
    sys.stdout.flush()


def connectAndCreate():
    conn = connect()
    createTables(conn)
    return conn


def createTables(conn):
    c = conn.cursor()
    print("creating table")
    c.execute(''' CREATE TABLE IF NOT EXISTS entries
                    (id integer primary key,
                    name text,
                    artist text,
                    place integer,
                    peak_position integer,
                    last_position integer,
                    weeks_on_chart integer,
                    chart_id integer,
                    song_id integer) ''')
    c.execute(''' CREATE TABLE IF NOT EXISTS charts
                    (id integer primary key,
                    type text,
                    date_string text unique) ''')
    c.execute(''' CREATE TABLE IF NOT EXISTS songs
                    (id integer primary key,
                    name text,
                    artist text)''')
    conn.commit()
    sys.stdout.flush()


def getInitialChart():
    chart = billboard.ChartData('hot-100',
                                fetch=True, timeout=30)
    return chart


def scrapeDataFromChartIntoConnection(chart, conn):
    while chart.previousDate and "2017" not in chart.date:
        saveChart(chart, conn)
        chart = billboard.ChartData('hot-100', chart.previousDate, timeout=45)


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


def crawlEntriesForSongs(cursor):
    songs = []

    # gives me the distinct name/artist combos
    entries = cursor.execute(''' SELECT DISTINCT name, artist FROM entries ''').fetchone()
    entry = cursor.execute(''' SELECT * FROM entries WHERE name = ? AND artist = ? ''', (entries[0], entries[1])).fetchall()
    return entry




def doesDatabaseContainDate(date, conn):
    c = conn.cursor()
    countTuple = c.execute(''' SELECT count(*) from charts
                           WHERE date_string IS ? ''', (date,)).fetchone()
    count = countTuple[0]
    return count > 0


def scrapeDataForYear(year, conn, onYearDone):
    finalDate = getFinalDate(year)
    lastChart = billboard.ChartData('hot-100', date=finalDate,
                                    fetch=True, timeout=30)
    prevYear = getPreviousYear(year)
    chart = lastChart
    while(chart.previousDate and prevYear not in chart.date):
        saveChart(chart, conn)
        onYearDone()
        time.sleep(10)
        chart = billboard.ChartData('hot-100', chart.previousDate, timeout=45)


def getFinalDate(year):
    now = datetime.date.today()
    delt = datetime.timedelta(weeks=1)
    then = now - delt
    if year == now.year:
        finalDate = "{}-{:0>2}-{:0>2}".format(then.year, then.month, then.day)
    else:
        finalDate = str(year) + '-12-31'
    return finalDate


def getPreviousYear(year):
    return str(int(year) - 1)


def hasData(conn):
    c = getCursor(conn)
    c.execute(''' SELECT count(*) FROM songs ''')
    data = c.fetchall()
    return len(list(data)) is not 0


def getSavedSongsFromConnection(conn):
    c = conn.cursor()
    songs = c.execute('SELECT * FROM songs').fetchall()
    return songs


# Grabs all the songs in the database as a list.
# Assumes it's of an ok size to have in memory
def getAllSavedSongs():
    conn = connect()
    c = conn.cursor()
    songs = c.execute('SELECT * FROM songs').fetchall()
    conn.close()
    return songs
