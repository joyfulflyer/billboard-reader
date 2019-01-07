import sqlite3

class Song:
	def __init__(self, place, name, artist, date):
		self.place = place
		self.name = name
		self.artist = artist
		self.date = date

	def __repr__(self):
		return repr((self.place, self.name, self.artist, self.date))

	def __str__(self):
		return "'%s' by '%s' Place: %s on: %s" % (self.name, self.artist, self.place, self.date)

	@classmethod
	def fromTuple(cls, tuple):
		return cls(tuple[1], tuple[2], tuple[3], tuple[4])

