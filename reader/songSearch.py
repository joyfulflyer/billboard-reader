from billboardReader.song import Song


def getSongsFromName(name, conn):
    return conn.cursor().execute('SELECT * FROM entries WHERE name LIKE ?', (name,)).fetchall()


def getSongObjectsFromName(name, conn):
    return convertToSongObjects(getSongsFromName(name, conn))


def convertToSongObjects(list):
    return map(lambda x: Song.fromTuple(x), list)


def getFirstLowestPlaceSong(listOfSongs):
    return min(listOfSongs, byPlace)


def byPlace(songObject):
    return songObject.place


def minWithTuple(song):
    return song[1]


def getTheRestOfTheWeeksSongs(song, conn):
    return conn.cursor().execute('SELECT * FROM entries WHERE dateString = ?', (song.date,)).fetchall()


def sortByPlace(listOfSongs):
    return sorted(listOfSongs, key=byPlace)


def getSongsWithName(listOfSongs, name):
    return filter(lambda song: name.lower() in song.name.lower(), listOfSongs)


def getSongsThatMatchArtist(list, artist):
    return filter(getFunctionToGetArtist(artist), list)


def getFunctionToGetArtist(artistToMatch):
    def theFunctionToCall(song):
        return song.artist == artistToMatch
    return theFunctionToCall


def matchNameAndArtist(song, list):
    def matchesNameAndArtist(itemInList):
        return song.artist == itemInList.artist and song.name == itemInList.name
    return filter(matchNameAndArtist, list)


# Get the lowest chart entries as a list from a song
def getLowestChartEntries(song, songList):
    sameSongs = matchNameAndArtist(song, songList)
    m = getFirstLowestPlaceSong(sameSongs)
    mins = filter(lambda s: s.place == m.place, sameSongs)
    return mins


def getFirstLowestChartEntryForSong(song, songlist):
    sameSongs = matchNameAndArtist(song, songList)
    return getFirstLowestPlaceSong(sameSongs)


def getHot100ForWeekOfSong(song, fullListOfSongs):
    return list(sorted(filter(lambda s: s.date == song.date, fullListOfSongs), key=byPlace))


def removeDupes(songList):
    solo = []
    songList = list(songList)
    for i in range(len(songList)):
        cur = songList[i]
    #   println("cur = " + cur)
        found = False
        for y in range(i+1, len(songList)):
            comp = songList[y]
            if cur == comp:
                found = True
                break
        if not found:
            solo.append(cur)
    return solo
