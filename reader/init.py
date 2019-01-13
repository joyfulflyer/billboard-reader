import songDatabase as db
import songSearch as search

allSongs = list(search.convertToSongObjects(db.getAllSavedSongs()))