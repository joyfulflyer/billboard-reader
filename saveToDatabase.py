import sys
import billboard
import sqlite3

def connect():
	print('connecting to db')
	sys.stdout.flush()
	conn = sqlite3.connect('charts.db')

	return conn

def getCursor(conn)	:
	print('creating cursor')
	sys.stdout.flush()
	c = conn.cursor()
	return c

def dropTables(c):
	print('dropping table')
	c.execute(''' DROP TABLE IF EXISTS songs''')
	c.execute(''' DROP TABLE IF EXISTS charts ''')
	sys.stdout.flush()

def createTables(c):
	print("creating table")
	c.execute(''' CREATE TABLE IF NOT EXISTS songs
					(id not null integer primary key, place integer, name text, artist text, dateString not null text) ''')
	c.execute(''' CREATE TABLE IF NOT EXISTS charts 
					(id integer primary key, type text, dateString text unique) ''')
	sys.stdout.flush()

def getInitialChart():
	print("getting chart")
	chart = billboard.ChartData('hot-100', date='2018-10-13', fetch=True, timeout=30)
	sys.stdout.flush()
	return chart

def scrapeDataFromChartIntoConnection(chart, conn):
	print("starting save loop")
	while chart.previousDate and "2017" not in chart.date:
		saveChart(chart, conn)
		chart = billboard.ChartData('hot-100', chart.previousDate)

def saveChart(chart, conn):
	print('Saving date ' + chart.date)
	sys.stdout.flush()
	print('saving chart')
	c = conn.cursor()
	c.execute(''' INSERT INTO charts VALUES (?, ?) ''', ("hot-100", chart.date))
	for i, song in enumerate(chart.entries):
		c.execute(''' INSERT INTO songs VALUES (?, ?, ?, ?) ''', (i, song.title, song.artist, chart.date))
	print('getting new chart')
	sys.stdout.flush()
	conn.commit()

def scrapeDataForYear(year):
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