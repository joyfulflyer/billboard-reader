import sys
sys.stdout.flush()
print('importing billboard')
import billboard
print('importing sqlite3')
import sqlite3

sys.stdout.flush()

print('connecting to db')
sys.stdout.flush()
conn = sqlite3.connect('charts.db')

print('creating cursor')
sys.stdout.flush()
c = conn.cursor()

print('dropping table')
c.execute(''' DROP TABLE IF EXISTS songs''')
sys.stdout.flush()

print("creating table")
c.execute(''' CREATE TABLE IF NOT EXISTS songs
				(place integer, name text, artist text) ''')
sys.stdout.flush()

print("getting chart")
chart = billboard.ChartData('hot-100', date='2018-10-13', fetch=True, timeout=30)
sys.stdout.flush()


print("starting save loop")
while chart.previousDate and "2010" not in chart.date:
	print('Saving date ' + chart.date)
	sys.stdout.flush()
	for i, song in enumerate(chart.entries):
		c.execute(''' INSERT INTO songs VALUES (?, ?, ?) ''', (i, song.title, song.artist))
	print('getting new chart')
	sys.stdout.flush()
	chart = billboard.ChartData('hot-100', chart.previousDate)

conn.commit()

conn.close()

print("all done")