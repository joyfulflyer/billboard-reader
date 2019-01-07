import sys
import billboard
import sqlite3

def connect():
	print('connecting to db')
	sys.stdout.flush()
	conn = sqlite3.connect('charts.db')

	return conn

def getCursor(conn):
#	print('creating cursor')
	sys.stdout.flush()
	c = conn.cursor()
	return c

def dropTables(conn):
	c = conn.cursor()
	print('dropping table')
	c.execute(''' DROP TABLE IF EXISTS songs''')
	c.execute(''' DROP TABLE IF EXISTS charts ''')
	sys.stdout.flush()

def connectAndCreate():
	conn = connect()
	createTables(conn)
	return conn

def createTables(conn):
	c = conn.cursor()
	print("creating table")
	c.execute(''' CREATE TABLE IF NOT EXISTS songs
					(place integer, name text, artist text, dateString text) ''')
	c.execute(''' CREATE TABLE IF NOT EXISTS charts 
					(type text, dateString text unique) ''')
	conn.commit()
	sys.stdout.flush()

def getInitialChart():
#	print("getting chart")
	chart = billboard.ChartData('hot-100', date='2018-10-13', fetch=True, timeout=30)
#	sys.stdout.flush()
	return chart

def scrapeDataFromChartIntoConnection(chart, conn):
#	print("starting save loop")
	while chart.previousDate and "2017" not in chart.date:
		saveChart(chart, conn)
		chart = billboard.ChartData('hot-100', chart.previousDate)

def saveChart(chart, conn):
#	print('Saving date ' + chart.date)
#	sys.stdout.flush()
#	print('saving chart')
	c = conn.cursor()
	try:
		c.execute(''' INSERT INTO charts(type, dateString) VALUES (?, ?) ''', ("hot-100", chart.date))
	except sqlite3.IntegrityError:
#		print("chart exists")
		return
	for i, song in enumerate(chart.entries):
		c.execute(''' INSERT INTO songs(place, name, artist, dateString) VALUES (?, ?, ?, ?) ''', (i, song.title, song.artist, chart.date))
#	print('getting new chart')
#	sys.stdout.flush()
	conn.commit()

def doesDatabaseContainDate(date, conn):
	c = conn.cursor()
	countTuple = c.execute(''' SELECT count(*) from charts WHERE dateString IS ? ''', (date,)).fetchone()
	count = countTuple[0]
	return count > 0


def scrapeDataForYear(year, conn):
	finalDate = getFinalDate(year)
	lastChart = billboard.ChartData('hot-100', date=finalDate, fetch=True, timeout=30)
	prevYear = getPreviousYear(year)
	chart = lastChart
	while(chart.previousDate and prevYear not in chart.date):
		saveChart(chart, conn)
		chart = billboard.ChartData('hot-100', chart.previousDate)

def getFinalDate(year):
	finalDate = str(year) + '-12-31'
	return finalDate

def getPreviousYear(year):
	return str(int(year)-1)

def hasData(conn):
	c = getCursor(conn)
	c.execute(''' SELECT count(*) FROM songs ''')
	data = c.fetchall()