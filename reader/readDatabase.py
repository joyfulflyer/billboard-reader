import sqlite3

con = sqlite3.connect('charts.db')

conn = sqlite3.connect('charts.db')

c = conn.cursor()

c.execute("select * from songs")

print(c.fetchall())

conn.close()
