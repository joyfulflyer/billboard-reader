from song import Song

def getSongsFromName(name, conn):
	return conn.cursor().execute('SELECT * FROM songs WHERE name LIKE ?', (name,)).fetchall()

def getSongObjectsFromName(name, conn):
	return map(lambda x: Song.fromTuple(x), getSongsFromName(name, conn))

def getLowestPlaceSong(listOfSongs):
	return min(listOfSongs, byPlace)

def byPlace(songObject):
	return songObject.place

def minWithTuple(song):
	return song[1]

def getTheRestOfTheWeeksSongs(song, conn):
	return conn.cursor().execute('SELECT * FROM songs WHERE dateString = ?', (song.date,)).fetchall()

def sortByPlace(listOfSongs):
	return sorted(listOfSongs, byPlace)